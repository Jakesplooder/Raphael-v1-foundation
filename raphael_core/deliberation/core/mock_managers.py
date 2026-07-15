from .interfaces import GoalProvider

class MockGoalManager(GoalProvider):
    def get_active_goals(self) -> list[str]:
        return ["Customer acquisition", "Market expansion"]
        
    def get_strategic_priorities(self) -> list[str]:
        return ["Growth over immediate profitability", "Speed to market"]
        
    def get_risk_profile(self) -> str:
        return "Aggressive"
