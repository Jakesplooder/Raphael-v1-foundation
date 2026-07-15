import logging
from typing import List, Optional
from ..core.models import GoalHierarchy, Mission, StrategicObjective, Initiative, KeyResult, Metric

logger = logging.getLogger("rrk.executive.goals")

class GoalManager:
    def __init__(self):
        self.hierarchy: Optional[GoalHierarchy] = None
        
    def set_mission(self, mission: Mission):
        self.hierarchy = GoalHierarchy(mission=mission)
        logger.info(f"Mission established: {mission.statement}")
        
    def get_active_initiatives(self) -> List[Initiative]:
        if not self.hierarchy:
            return []
        active = []
        for obj in self.hierarchy.mission.objectives:
            for init in obj.initiatives:
                if init.status == "ACTIVE":
                    active.append(init)
        return active
        
    def get_initiative_owner(self, initiative_name: str) -> Optional[str]:
        for init in self.get_active_initiatives():
            if init.name == initiative_name:
                return init.owner
        return None
        
    def get_active_goals(self) -> List[str]:
        return [init.name for init in self.get_active_initiatives()]
        
    def get_strategic_priorities(self) -> List[str]:
        return ["Derived from StrategicObjectives"] if self.hierarchy else []
        
    def get_risk_profile(self) -> str:
        return "DYNAMIC"
