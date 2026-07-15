import logging
import asyncio

from .action_registry import ActionRegistry
from .permission_engine import PermissionEngine
from .simulation_gate import SimulationGate
from .tool_router import ToolRouter
from .execution_monitor import ExecutionMonitor
from .action_memory import ActionMemory

logger = logging.getLogger("rrk.action.kernel")

class ActionKernel:
    """
    The orchestrator that gives Raphael OS "hands".
    Routes Intents through Registry -> Permission -> Simulation Gate -> Tool Router -> Execution Monitor.
    """
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.registry = ActionRegistry()
        self.permission_engine = PermissionEngine()
        self.simulation_gate = SimulationGate(event_bus)
        self.tool_router = ToolRouter()
        self.memory = ActionMemory()
        self.monitor = ExecutionMonitor(event_bus, self.memory)

    async def execute_intent(self, role: str, intent: str, payload: dict) -> dict:
        self.event_bus.emit("ACTION_REQUESTED", "ActionKernel", {"intent": intent, "role": role})
        
        # 1. Action Registry Lookup
        spec = self.registry.get_action_spec(intent)
        if not spec:
            msg = f"Unknown action intent: {intent}"
            logger.error(msg)
            self.event_bus.emit("ACTION_FAILED", "ActionKernel", {"intent": intent, "error": msg})
            return {"status": "FAILED", "reason": msg}
            
        provider = spec["provider"]
        risk = spec["risk"]
        permission = spec["permission"]
        max_cost = spec.get("max_cost", float('inf'))
        cost = payload.get("cost", 0)

        # 2. Permission Engine
        perm_status = self.permission_engine.check_permission(role, permission, cost)
        if perm_status == "DENIED":
            msg = f"Role '{role}' is DENIED permission '{permission}'"
            self.event_bus.emit("ACTION_FAILED", "ActionKernel", {"intent": intent, "error": msg})
            return {"status": "DENIED", "reason": msg}
        elif perm_status == "REQUIRES_APPROVAL":
            msg = f"Role '{role}' requires CEO approval for permission '{permission}'"
            self.event_bus.emit("ACTION_FAILED", "ActionKernel", {"intent": intent, "error": msg})
            return {"status": "DENIED", "reason": msg}
            
        if cost > max_cost:
             msg = f"Cost {cost} exceeds max cost {max_cost} for intent {intent}"
             self.event_bus.emit("ACTION_FAILED", "ActionKernel", {"intent": intent, "error": msg})
             return {"status": "DENIED", "reason": msg}

        self.event_bus.emit("ACTION_AUTHORIZED", "ActionKernel", {"intent": intent})
        
        # 3. Simulation Gate
        sim_status = await self.simulation_gate.evaluate(intent, risk, spec)
        if sim_status == "DENIED":
            return {"status": "DENIED", "reason": "Simulation Failed"}
        elif sim_status == "REQUIRES_HUMAN":
            return {"status": "REQUIRES_HUMAN", "reason": "Critical risk, human/executive approval required."}
            
        # 4. Tool Router (Execution)
        result = self.tool_router.execute(provider, intent, payload)
        
        # 5. Execution Monitor & D19 Memory
        final_status = self.monitor.log_execution_result(intent, result, provider)
        
        return {"status": final_status, "details": result}
