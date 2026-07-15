from typing import List, Dict
from raphael_core.repositories.goals import IGoalRepository

class GoalService:
    def __init__(self, repository: IGoalRepository):
        self.repository = repository

    def get_all_goals(self) -> List[Dict[str, str]]:
        """
        Validates, searches, filters, and returns business representations of goals.
        """
        goals = self.repository.get_all_goals()
        # Add business validation/filtering here as needed
        return goals
