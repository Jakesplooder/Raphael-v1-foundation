import logging

logger = logging.getLogger("rrk.action.tool_router")

class ToolRouter:
    """
    Routes an approved action to its specific execution provider (e.g., n8n, api, internal).
    """
    def execute(self, provider: str, action: str, payload: dict) -> dict:
        logger.info(f"Routing action '{action}' to provider '{provider}'")
        
        # Stub logic for routing to actual providers
        if provider == "n8n":
            return {"status": "SUCCESS", "message": f"n8n executed {action}", "cost": payload.get("cost", 0)}
        elif provider == "business_factory":
            return {"status": "SUCCESS", "message": f"Business Factory executed {action}"}
        elif provider == "finance_api":
            return {"status": "SUCCESS", "message": f"Finance API executed {action}"}
        else:
            return {"status": "FAILED", "message": f"Unknown provider {provider}"}
