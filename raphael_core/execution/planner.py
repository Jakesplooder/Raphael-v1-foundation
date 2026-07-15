import uuid
from typing import Dict, Any, List
from ..kernel.event_bus import emit
from ..kernel.storage import KernelStorage

storage = KernelStorage()

class ExecutionPlanner:
    def __init__(self):
        self.domain = "execution"

    def create_plan(self, intent: str, steps: List[str]) -> str:
        exec_id = f"EXEC-{str(uuid.uuid4())[:8].upper()}"
        plan = {
            "id": exec_id,
            "intent": intent,
            "steps": steps,
            "status": "planned"
        }
        storage.save(self.domain, f"{exec_id}_plan.json", plan)
        emit("EXECUTION_PLANNED", "ExecutionPlanner", plan)
        return exec_id
