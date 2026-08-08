from typing import Dict, Any, List
from .executive_state import StateProducer, ProducerResult

class WorkflowProducer(StateProducer):
    """
    Produces raw facts about currently active workflows by reading from the ExecutionRepository.
    """
    def __init__(self):
        pass
        
    def name(self) -> str:
        return "workflows"
        
    def category(self) -> str:
        return "executions"
        
    def collect(self) -> ProducerResult:
        try:
            from raphael_core.operator.execution_manager import ExecutionManager
            
            # Use the default instance or repositories
            manager = ExecutionManager()
            all_executions = manager.executions.list()
            
            # Build facts about running workflows
            running = []
            paused = []
            failed = []
            completed = []
            
            for exec_data in all_executions:
                if exec_data.status in ("RUNNING", "QUEUED"):
                    running.append(exec_data.to_dict())
                elif exec_data.status == "PAUSED":
                    paused.append(exec_data.to_dict())
                elif exec_data.status == "FAILED":
                    failed.append(exec_data.to_dict())
                else:
                    completed.append(exec_data.to_dict())
            
            data = {
                "active_count": len(running) + len(paused),
                "running": running,
                "paused": paused,
                "failed": failed,
                "completed": completed[-10:] # Keep last 10 completed for brief history
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
                errors=[f"Failed to collect workflows: {str(e)}"]
            )
