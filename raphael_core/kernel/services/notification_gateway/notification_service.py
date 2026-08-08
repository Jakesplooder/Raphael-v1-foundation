import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from raphael_core.kernel.event_bus import emit
from .providers.discord_provider import DiscordProvider
from .providers.telegram_provider import TelegramProvider
from .templates.mission_alerts import format_mission_alert, format_mission_failure
from .templates.approval_requests import format_approval_request
from .templates.executive_briefs import format_executive_brief
from .delivery_log import DeliveryLedger

class NotificationPolicy:
    def __init__(self, event: str, severity: str, discord: bool, telegram: bool, bypass_quiet_hours: bool = False, authority_requirement: bool = False):
        self.event = event
        self.severity = severity
        self.discord = discord
        self.telegram = telegram
        self.bypass_quiet_hours = bypass_quiet_hours
        self.authority_requirement = authority_requirement

class NotificationService:
    def __init__(self):
        self.discord = DiscordProvider()
        self.telegram = TelegramProvider()
        self.ledger = DeliveryLedger()
        
        self.notifications_dir = Path(r"C:\RaphaelOS\Notifications")
        self.notifications_dir.mkdir(parents=True, exist_ok=True)
        self.routing_log = self.notifications_dir / "routing_decisions.jsonl"
        
        # telegram quiet hours configuration
        self.quiet_hours = {
            "enabled": True,
            "start": 22,
            "end": 7
        }
        
        self.policies = [
            NotificationPolicy(event="MISSION.FAILURE", severity="critical", discord=True, telegram=True, bypass_quiet_hours=True),
            NotificationPolicy(event="MISSION.FAILURE", severity="warning", discord=True, telegram=False),
            NotificationPolicy(event="APPROVAL.REQUIRED", severity="high", discord=False, telegram=True, bypass_quiet_hours=True, authority_requirement=True),
            NotificationPolicy(event="SYSTEM.DAILY_BRIEF", severity="normal", discord=True, telegram=True, bypass_quiet_hours=False),
            NotificationPolicy(event="MISSION.COMPLETED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="MISSION.CREATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="MISSION.STARTED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="MISSION.RECOVERED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.PATTERN_DISCOVERED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="STRATEGY.HYPOTHESIS_CREATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="STRATEGY.EXPERIMENT_COMPLETED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.TWIN_UPDATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="FINANCE.ROI_CALCULATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="PORTFOLIO.ALLOCATION_CREATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="PORTFOLIO.RESOURCE_GRANTED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="PORTFOLIO.BUSINESS_RANKED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.REGISTERED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.STATE_CHANGED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.ACTIVATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.RETIRED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.PROPOSED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.EVALUATION_STARTED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.EVALUATION_COMPLETED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.INCUBATION_STARTED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.MVP_CREATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="BUSINESS.SCALE_RECOMMENDED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="VENTURE.INVESTMENT_MEMO_CREATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="VENTURE.CAPITAL_ALLOCATED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="VENTURE.VALIDATION_FAILED", severity="normal", discord=True, telegram=True),
            NotificationPolicy(event="VENTURE.APPROVAL_REQUIRED", severity="high", discord=False, telegram=True, bypass_quiet_hours=False, authority_requirement=True),
            NotificationPolicy(event="VENTURE.COMPETITION_STARTED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="VENTURE.RANKED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="VENTURE.ALLOCATION_CHANGED", severity="normal", discord=True, telegram=False),
            NotificationPolicy(event="VENTURE.OUTCOMPETED", severity="normal", discord=True, telegram=False)
        ]

    def _is_quiet_hours(self) -> bool:
        if not self.quiet_hours["enabled"]:
            return False
        current_hour = datetime.now().hour
        if self.quiet_hours["start"] <= self.quiet_hours["end"]:
            return self.quiet_hours["start"] <= current_hour < self.quiet_hours["end"]
        else:
            return current_hour >= self.quiet_hours["start"] or current_hour < self.quiet_hours["end"]

    def _log_routing(self, event_type: str, severity: str, route: str, reason: str):
        record = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "severity": severity,
            "route": route,
            "reason": reason
        }
        with open(self.routing_log, "a") as f:
            f.write(json.dumps(record) + "\n")

    def handle_event(self, event_type: str, source: str, payload: Dict[str, Any]):
        severity = payload.get("priority", "normal")
        
        # Match Policy
        policy = next((p for p in self.policies if p.event == event_type and p.severity == severity), None)
        if not policy:
            # Fallback policy: match event only
            policy = next((p for p in self.policies if p.event == event_type), None)
            
        if not policy:
            return # Unknown event, do not route

        message = self._format_message(event_type, payload)
        
        # Route to Discord (HQ)
        if policy.discord:
            channel_name = "#mission-feed"
            if event_type in ["MISSION.FAILURE"]:
                channel_name = "#incidents"
            elif event_type in ["SYSTEM.DAILY_BRIEF", "FINANCE.ROI_CALCULATED", "BUSINESS.TWIN_UPDATED", "BUSINESS.PATTERN_DISCOVERED"]:
                channel_name = "#analytics"
            elif event_type.startswith("STRATEGY."):
                channel_name = "#strategy-council"
            elif event_type.startswith("PORTFOLIO.ALLOCATION") or event_type == "PORTFOLIO.RESOURCE_GRANTED":
                channel_name = "#resource-allocation"
            elif event_type.startswith("PORTFOLIO."):
                channel_name = "#portfolio-council"
            elif event_type.startswith("BUSINESS.") and event_type not in ["BUSINESS.TWIN_UPDATED", "BUSINESS.PATTERN_DISCOVERED"]:
                channel_name = "#business-registry"
            elif event_type.startswith("VENTURE."):
                channel_name = "#venture-review"
                
            # If domain-specific event (mocked logic), could route to #creator-council etc. based on payload
            domain = payload.get("domain", "").lower()
            if domain in ["creator", "career", "commerce", "agency"]:
                channel_name = f"#{domain}-council"
                
            self.discord.send(message, channel_name)
            self.ledger.log_delivery(event_type, "discord", "DELIVERED")
            self._log_routing(event_type, severity, "discord", "Logged to operations memory")

        # Route to Telegram (CEO Phone)
        if policy.telegram:
            in_quiet_hours = self._is_quiet_hours()
            if in_quiet_hours and not policy.bypass_quiet_hours:
                self._log_routing(event_type, severity, "telegram", "Blocked by quiet hours")
                self.ledger.log_delivery(event_type, "telegram", "BLOCKED_QUIET_HOURS")
            else:
                reason = "Executive interruption required"
                if policy.authority_requirement:
                    reason = "Decision authority required"
                elif in_quiet_hours and policy.bypass_quiet_hours:
                    reason = "Critical override during quiet hours"
                
                self.telegram.send(message)
                self.ledger.log_delivery(event_type, "telegram", "DELIVERED")
                self._log_routing(event_type, severity, "telegram", reason)
                
    def _format_message(self, event_type: str, payload: Dict[str, Any]) -> str:
        if event_type == "MISSION.FAILURE":
            return format_mission_failure(payload)
        elif event_type in ["MISSION.REVIEW_REQUIRED", "APPROVAL.REQUIRED"]:
            return format_approval_request(payload)
        elif event_type == "VENTURE.APPROVAL_REQUIRED":
            return self._format_venture_approval(payload)
        elif event_type == "SYSTEM.DAILY_BRIEF":
            return format_executive_brief(payload)
        else:
            return format_mission_alert(payload)

    def _format_venture_approval(self, payload: Dict[str, Any]) -> str:
        return f"""🚨 Venture Approval Required

Venture:
{payload.get('venture', 'Unknown')}

Council Recommendation:
{payload.get('recommendation', 'UNKNOWN')}

Requested Capital:
${payload.get('requested_budget', 0)}

Expected Validation:
{payload.get('expected_validation_days', 30)} days

Approve?
[YES] [NO]"""

notification_service = NotificationService()
