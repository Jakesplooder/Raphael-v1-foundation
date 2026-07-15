from typing import Dict, Any
from ..kernel.event_bus import emit
from ..kernel.storage import KernelStorage
from .planner import ExecutionPlanner

storage = KernelStorage()

class Executor:
    def __init__(self):
        self.domain = "execution"

    def execute_plan(self, exec_id: str):
        plan = storage.load(self.domain, f"{exec_id}_plan.json")
        if not plan:
            emit("EXECUTION_FAILED", "Executor", {"id": exec_id, "reason": "Plan not found"})
            return

        emit("EXECUTION_STARTED", "Executor", {"id": exec_id, "intent": plan.get("intent")})
        
        for step in plan.get("steps", []):
            # Stub step execution
            emit("EXECUTION_STEP_COMPLETED", "Executor", {"id": exec_id, "step": step})
            
        plan["status"] = "completed"
        storage.save(self.domain, f"{exec_id}_plan.json", plan)
        emit("EXECUTION_LEARNED", "Executor", {"id": exec_id, "lessons": "Task completed successfully natively."})
