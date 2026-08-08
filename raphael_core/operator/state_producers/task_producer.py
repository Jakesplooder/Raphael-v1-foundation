from typing import Dict, Any, List
from .executive_state import StateProducer, ProducerResult

class TaskProducer(StateProducer):
    """
    Produces raw facts about currently pending missions/tasks by reading from the MissionRepository.
    """
    def __init__(self):
        pass
        
    def name(self) -> str:
        return "tasks"
        
    def category(self) -> str:
        return "executions"
        
    def collect(self) -> ProducerResult:
        try:
            from raphael_core.operator.execution_manager import ExecutionManager
            
            manager = ExecutionManager()
            all_missions = manager.missions.list()
            
            pending = []
            approved = []
            rejected = []
            
            for mission in all_missions:
                m_dict = mission.to_dict()
                if mission.status == "PENDING_APPROVAL":
                    pending.append(m_dict)
                elif mission.status == "APPROVED":
                    approved.append(m_dict)
                else:
                    rejected.append(m_dict)
            
            data = {
                "pending_approval": pending,
                "approved": approved,
                "rejected": rejected[-10:] # Keep recent history
            }
            
            return ProducerResult(
                producer_name=self.name(),
                success=True,
                data=data,
                completeness=1.0
            )
        except Exception as e:
            return ProducerResult(
                producer_name=self.name(),
                success=False,
                data={},
                completeness=0.0,
                errors=[f"Failed to collect tasks: {str(e)}"]
            )
