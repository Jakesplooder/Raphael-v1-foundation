from typing import Dict, Any, Optional

class ActionRegistry:
    """
    Maps abstract intents to specific action providers, along with
    their risk profiles and required permissions.
    """
    def __init__(self):
        # In a real system, this could be loaded from JSON.
        self.registry = {
            "create_social_post": {
                "action": "create_social_post",
                "provider": "n8n",
                "risk": "LOW",
                "permission": "MARKETING_EXECUTION",
                "cost": 0
            },
            "launch_ad_campaign": {
                "action": "launch_ad_campaign",
                "provider": "n8n",
                "risk": "MEDIUM",
                "permission": "MARKETING_SPEND",
                "max_cost": 500
            },
            "spend_large_capital": {
                "action": "spend_large_capital",
                "provider": "finance_api",
                "risk": "HIGH",
                "permission": "CAPITAL_ALLOCATION"
            },
            "create_company": {
                "action": "create_company",
                "provider": "business_factory",
                "risk": "CRITICAL",
                "permission": "VENTURE_CREATION"
            },
            "create_shopify_product": {
                "action": "create_shopify_product",
                "provider": "n8n",
                "risk": "LOW",
                "permission": "COMMERCE_EXECUTION"
            }
        }

    def get_action_spec(self, intent: str) -> Optional[Dict[str, Any]]:
        return self.registry.get(intent)
