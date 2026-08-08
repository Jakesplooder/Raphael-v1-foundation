from typing import Dict, Any
import logging
import os
import json
from .intent_router import intent_router, IntentClass
from .planner import planner
from .execution_preview import execution_preview
from .workflow_matcher import workflow_matcher
from .capability_aggregator import capability_aggregator
from .execution_manager import execution_manager

logger = logging.getLogger("operator.chat_controller")

class ChatController:
    """
    Main entry point for Operator Chat.
    Handles the flow: Intent Router -> Capability Match -> Mission Planner -> MissionProposal -> ExecutionManager -> Command Bus
    """
    def __init__(self):
        self.debug_mode = os.environ.get("RAPHAEL_ROUTING_DEBUG", "").lower() == "true"

    def _debug_log(self, title: str, details: Dict[str, Any]):
        if self.debug_mode:
            print(f"\n[CHAT ROUTER] {title}")
            for k, v in details.items():
                print(f"{k}: {v}")
            print()

    def process_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Processes a chat message and returns the response payload for the UI.
        """
        # Route intent
        intent_type, route_info = intent_router.route(message)
        
        self._debug_log("Routing", {
            "Input": message,
            "Intent": intent_type.value,
            "Source": route_info.get("source", "heuristic")
        })
        
        # 1. Approval Logic via ExecutionManager
        if intent_type == IntentClass.APPROVAL:
            try:
                execution = execution_manager.approve_latest(session_id)
                if execution:
                    return {
                        "response": f"**Execution Started**\n\nExecution ID:\n{execution.execution_id}\n\nStatus:\nRunning\n\nProgress:\n0 / 100\n\n[Open Mission Control](javascript:window.RaphaelOperations.openMission(\"{execution.execution_id}\"))",
                        "intent": "execute",
                        "command": execution.workflow_id,
                        "status": "Executing",
                        "confirmation_required": False,
                        "awaiting_confirmation": False
                    }
                else:
                    return {
                        "response": "There is no matching pending command to confirm.",
                        "intent": "error",
                        "command": "",
                        "status": "Failed",
                        "confirmation_required": False,
                        "awaiting_confirmation": False
                    }
            except Exception as e:
                return {
                    "response": f"Approval failed: {str(e)}",
                    "intent": "error",
                    "command": "",
                    "status": "Failed",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }
                
        elif intent_type == IntentClass.REJECTION:
            try:
                mission = execution_manager.reject_latest(session_id)
                if mission:
                    return {
                        "response": f"Execution cancelled. Mission {mission.mission_id} rejected.",
                        "intent": "cancel",
                        "command": "",
                        "status": "Cancelled",
                        "confirmation_required": False,
                        "awaiting_confirmation": False
                    }
                else:
                    return {
                        "response": "There is no pending mission to reject.",
                        "intent": "error",
                        "command": "",
                        "status": "Failed",
                        "confirmation_required": False,
                        "awaiting_confirmation": False
                    }
            except Exception as e:
                return {
                    "response": f"Rejection failed: {str(e)}",
                    "intent": "error",
                    "command": "",
                    "status": "Failed",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }
                
        elif intent_type == IntentClass.STATUS_QUERY:
            execution = None
            message_lower = message.lower()
            
            # Extract keywords from the query
            keywords = [w for w in message_lower.split() if len(w) > 3 and w not in ["status", "what", "how", "show"]]
            
            if keywords:
                all_ex = execution_manager.executions.list()
                session_ex = [e for e in all_ex if e.context.session_id == session_id]
                sorted_ex = sorted(session_ex, key=lambda x: x.started_at, reverse=True)
                for ex in sorted_ex:
                    if any(kw in ex.workflow_id.lower() for kw in keywords):
                        execution = ex
                        break
                            
            if not execution:
                execution = execution_manager.get_latest_execution(session_id)
                
            if execution:
                res = f"**Status**\n\nWorkflow:\n{execution.workflow_id}\n\nStatus:\n{execution.status}\n\n"
                res += f"Started:\n{execution.started_at}\n\nProgress:\n{execution.progress_percent}%"
                return {
                    "response": res,
                    "intent": "status",
                    "command": "",
                    "status": "Processed",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }
            else:
                return {
                    "response": "No active execution found for this session.",
                    "intent": "status",
                    "command": "",
                    "status": "Processed",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }

        elif intent_type == IntentClass.MODIFICATION:
            mission = execution_manager.missions.get_latest_for_session(session_id)
            if not mission:
                return {
                    "response": "There is no pending mission to modify.",
                    "intent": "error",
                    "command": "",
                    "status": "Failed",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }
            if mission.status not in ["PENDING_APPROVAL", "QUEUED"]:
                return {
                    "response": f"This mission ({mission.mission_id}) is already {mission.status.lower()} and cannot be modified. Wait for it to complete or check Mission Control for status.",
                    "intent": "error",
                    "command": "",
                    "status": "Failed",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }
            # If valid, we re-route the modified request to the planner via CAPABILITY_DISPATCH
            intent_type = IntentClass.CAPABILITY_DISPATCH
            workflow_id = getattr(mission.context, "workflow_id", "unknown")
            message = f"Modify the pending mission {mission.mission_id} with these changes: {message}"
            
            proposal = planner.generate_plan(message, intent_type.value)
            
            # Override to ensure the modified mission stays in the same workflow
            if workflow_id != "unknown":
                proposal.workflow_id = workflow_id
                
            new_mission = execution_manager.register_proposal(proposal, "dashboard_chat", session_id)
            card = execution_preview.format_proposal_card(proposal)
            return {
                "response": f"**Mission Created**\n\nID:\n{new_mission.mission_id}\n\n{card}",
                "intent": "creation \u00b7 confirmation required",
                "command": proposal.workflow_id,
                "status": "Awaiting Approval",
                "confirmation_required": True,
                "awaiting_confirmation": True
            }

        elif intent_type == IntentClass.CAPABILITY_DISPATCH:
            workflow_id = route_info.get("workflow_id", "unknown")
            proposal = planner.generate_plan(message, intent_type.value)
            
            if workflow_id != "unknown":
                proposal.workflow_id = workflow_id
                
            mission = execution_manager.register_proposal(proposal, "dashboard_chat", session_id)
            card = execution_preview.format_proposal_card(proposal)
            return {
                "response": f"**Mission Created**\n\nID:\n{mission.mission_id}\n\n{card}",
                "intent": "creation \u00b7 confirmation required",
                "command": proposal.workflow_id,
                "status": "Awaiting Approval",
                "confirmation_required": True,
                "awaiting_confirmation": True
            }
            
        elif intent_type == IntentClass.EXECUTIVE_COMMAND:
            cmd = route_info.get("command")
            res = ""
            if cmd == "priority":
                res = "**Executive Priority**\n\n1. Review pending commerce workflows.\n2. Ensure Creator Council assets are approved."
            elif cmd == "councils":
                res = "**Active Councils**\n\n- Creator Council\n- Commerce Council\n- Agency Council\n- Core System"
            elif cmd == "agents":
                res = "**Active Agents**\n\n- Video Creator Agent\n- POD Studio Agent\n- Builder Agent\n- Memory Manager"
            elif cmd == "missions":
                missions = execution_manager.missions.get_all()
                res = f"**Total Missions**: {len(missions)}"
            return {
                "response": res,
                "intent": f"executive \u00b7 {cmd}",
                "command": "",
                "status": "Processed",
                "confirmation_required": False,
                "awaiting_confirmation": False
            }

        # 2. Hard capability intercepts
        if intent_type == IntentClass.CAPABILITY_QUERY:
            return {
                "response": execution_preview.format_os_indicator(),
                "intent": "capability_query",
                "command": "",
                "status": "Processed",
                "confirmation_required": False,
                "awaiting_confirmation": False
            }
            
        if intent_type == IntentClass.WORKFLOW_QUERY:
            manifest = capability_aggregator.load()
            lines = ["**Available Workflows**", ""]
            for wf in manifest.get("workflows", []):
                lines.append(f"- **{wf.get('name')}** ({wf.get('domain')})")
            return {
                "response": "\n".join(lines),
                "intent": "workflow_query",
                "command": "",
                "status": "Processed",
                "confirmation_required": False,
                "awaiting_confirmation": False
            }

        # 3. Handle Creation / Business with Workflow Matcher
        if intent_type in (IntentClass.CREATION, IntentClass.BUSINESS):
            matched_workflow = workflow_matcher.match(message)
            
            if matched_workflow:
                self._debug_log("Workflow Matcher", {
                    "Matched Workflow": matched_workflow.get("id"),
                    "Planner": "enabled"
                })
                
                # We found a workflow, now use planner to generate MissionProposal
                proposal = planner.generate_plan(message, intent_type.value)
                
                # Override the planner's selected workflow
                proposal.workflow_id = matched_workflow["id"]
                proposal.workflow_name = matched_workflow["name"]
                
                if proposal.requires_approval:
                    mission = execution_manager.register_proposal(proposal, "dashboard_chat", session_id)
                    card = execution_preview.format_proposal_card(proposal)
                    card = f"**Mission Created**\n\nID:\n{mission.mission_id}\n\n{card}"
                    return {
                        "response": card,
                        "intent": proposal.intent,
                        "command": proposal.workflow_id or "",
                        "status": "Awaiting Approval",
                        "confirmation_required": True,
                        "awaiting_confirmation": True
                    }
                else:
                    card = execution_preview.format_proposal_card(proposal)
                    return {
                        "response": card,
                        "intent": proposal.intent,
                        "command": proposal.workflow_id or "",
                        "status": "Processed",
                        "confirmation_required": False,
                        "awaiting_confirmation": False
                    }
            else:
                self._debug_log("Workflow Matcher", {
                    "Matched Workflow": "None",
                    "Status": "Unknown Creation"
                })
                return {
                    "response": "No matching workflow found.\n\nAvailable creation systems:\n- Video\n- POD\n- Websites\n- Commerce\n\nWould you like to create a new workflow proposal?",
                    "intent": intent_type.value,
                    "command": "",
                    "status": "Refused",
                    "confirmation_required": False,
                    "awaiting_confirmation": False
                }

        # 4. Normal Conversation or other fallback
        self._debug_log("Conversation Fallback", {
            "Intent": intent_type.value,
            "LLM": "allowed"
        })
        return {
            "response": "", # Signify to caller to use legacy LLM
            "intent": intent_type.value,
            "command": "",
            "status": "Routed to LLM",
            "confirmation_required": False,
            "awaiting_confirmation": False
        }

chat_controller = ChatController()
