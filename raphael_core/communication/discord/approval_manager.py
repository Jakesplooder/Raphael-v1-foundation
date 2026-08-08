from raphael_core.kernel.event_bus import global_event_bus
from raphael_core.kernel.interfaces import Event
from .models import DiscordUser
import time
import uuid

class ApprovalManager:
    def __init__(self):
        self.users = {
            "ceo_01": DiscordUser(discord_id="ceo_01", role="CEO", permissions=["CEO"]),
            "op_01": DiscordUser(discord_id="op_01", role="Operator", permissions=["execute_missions"]),
            "obs_01": DiscordUser(discord_id="obs_01", role="Observer", permissions=["view_dashboards"])
        }

    async def process_approval(self, discord_id: str, decision_id: str, action: str):
        user = self._get_user_by_id(discord_id)
        if not user or not user.has_permission("CEO"):
            return {"status": "error", "message": "Permission denied"}

        # Emit an event that the executive layer will pick up to update the Decision object
        await global_event_bus.publish(Event(
            id=f"evt_{uuid.uuid4().hex[:8]}",
            timestamp=time.time(),
            source="discord_approval_manager",
            type="decision_actioned",
            payload={
                "decision_id": decision_id,
                "action": action, # "approved" or "rejected"
                "actioned_by": user.role
            }
        ))
        
        return {"status": "success", "message": f"Decision {decision_id} marked as {action}."}

    def _get_user_by_id(self, discord_id: str):
        return self.users.get(discord_id)
