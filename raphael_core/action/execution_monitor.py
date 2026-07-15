import logging
from .action_memory import ActionMemory

logger = logging.getLogger("rrk.action.monitor")

class ExecutionMonitor:
    """
    Monitors execution results, logs them to ActionMemory, and emits events.
    """
    def __init__(self, event_bus, memory: ActionMemory):
        self.event_bus = event_bus
        self.memory = memory

    def log_execution_result(self, intent: str, result: dict, provider: str):
        status = result.get("status", "FAILED")
        
        # Extract metrics (like cost, revenue generated)
        metrics = {
            "cost": result.get("cost", 0),
            "message": result.get("message", "")
        }
        
        # Save to historical external memory
        self.memory.log_action(intent, status, provider, metrics)
        
        if status == "SUCCESS":
            self.event_bus.emit("ACTION_EXECUTED", "ExecutionMonitor", {"intent": intent, "metrics": metrics})
            # Trigger D19 Self-Improvement hook
            self.event_bus.emit("ACTION_LEARNED", "ExecutionMonitor", {"intent": intent})
        else:
            self.event_bus.emit("ACTION_FAILED", "ExecutionMonitor", {"intent": intent, "error": result.get("message")})
            
        return status
