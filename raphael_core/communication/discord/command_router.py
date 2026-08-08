from typing import List, Dict, Any, Callable
from .models import DiscordUser

class CommandRouter:
    def __init__(self):
        self.routes: Dict[str, Dict[str, Any]] = {}

    def register(self, command: str, handler: Callable, permission_required: str = None):
        self.routes[command] = {
            "handler": handler,
            "permission_required": permission_required
        }

    async def execute(self, command: str, user: DiscordUser, args: List[str] = None) -> str:
        route = self.routes.get(command)
        if not route:
            return f"Command not found: {command}"

        permission_required = route.get("permission_required")
        if permission_required and not user.has_permission(permission_required):
            return f"Permission denied. Requires '{permission_required}'."

        handler = route["handler"]
        return await handler(user, args)

# Read Commands (No permissions)
async def handle_status(user: DiscordUser, args: List[str]) -> str:
    return "RRK is ONLINE"

async def handle_decisions(user: DiscordUser, args: List[str]) -> str:
    return "Fetching pending decisions..."

# Action Commands (Require permissions)
async def handle_approve(user: DiscordUser, args: List[str]) -> str:
    if not args:
        return "Usage: /approve <decision_id>"
    # This would normally hook into ApprovalManager
    return f"Decision {args[0]} approved."

async def handle_execute(user: DiscordUser, args: List[str]) -> str:
    if not args:
        return "Usage: /execute <mission_id>"
    return f"Mission {args[0]} started."

def setup_router() -> CommandRouter:
    router = CommandRouter()
    
    # Read Commands
    router.register("/status", handle_status)
    router.register("/brief", handle_status)
    router.register("/missions", handle_status)
    router.register("/experiments", handle_status)
    router.register("/decisions", handle_decisions)
    
    # Action Commands
    router.register("/approve", handle_approve, permission_required="CEO")
    router.register("/reject", handle_approve, permission_required="CEO")
    router.register("/execute", handle_execute, permission_required="CEO")
    
    return router
