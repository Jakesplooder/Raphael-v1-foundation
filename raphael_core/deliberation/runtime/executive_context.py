import logging
from typing import Dict, Any, List
from ..core.interfaces import GoalProvider

logger = logging.getLogger("rrk.deliberation.context")

class ExecutiveContextEngine:
    def __init__(self, goal_provider: GoalProvider):
        self.goal_provider = goal_provider
        
    def get_context(self) -> Dict[str, Any]:
        return {
            "active_goals": self.goal_provider.get_active_goals(),
            "strategic_priorities": self.goal_provider.get_strategic_priorities(),
            "risk_profile": self.goal_provider.get_risk_profile()
        }
