import time
from typing import Dict, Any, List
from raphael_core.kernel.registry import registry
from raphael_core.kernel.interfaces import ServiceModule, ModuleHealth, Event, EventType

class CapabilityObservatory(ServiceModule):
    """
    Subscribes to capability events and maintains metrics for the ExecutiveStateEngine.
    """
    
    def __init__(self):
        self._metrics: Dict[str, Dict[str, Any]] = {}
        self._active_runs: Dict[str, float] = {}
        self._running = False
        
    def name(self) -> str:
        return "CapabilityObservatory"
        
    def depends_on(self) -> list[str]:
        return ["EventBus"]
        
    async def initialize(self) -> None:
        pass
        
    async def start(self) -> None:
        self._running = True
        event_bus = registry.get_service("EventBus")
        if event_bus:
            event_bus.subscribe("*", self._on_event)
            
    async def heartbeat(self) -> bool:
        return self._running
        
    async def stop(self) -> None:
        self._running = False
        
    async def shutdown(self) -> None:
        pass
        
    def health(self) -> ModuleHealth:
        return ModuleHealth.OK if self._running else ModuleHealth.FAILED
        
    def status(self) -> str:
        return f"Observing {len(self._metrics)} capabilities."
        
    def metrics(self) -> Dict[str, Any]:
        return self._metrics
        
    def get_capability_metrics(self) -> Dict[str, Any]:
        return self._metrics
        
    def _init_capability(self, capability: str):
        if capability not in self._metrics:
            self._metrics[capability] = {
                "runs": 0,
                "successes": 0,
                "failures": 0,
                "avg_runtime": 0,
                "total_runtime": 0
            }

    async def _on_event(self, event: Event) -> None:
        if event.type == EventType.MISSION_CREATED and event.source == "CapabilityService":
            capability = event.payload.get("capability")
            req_id = event.execution_id
            if capability and req_id:
                self._init_capability(capability)
                self._metrics[capability]["runs"] += 1
                self._active_runs[req_id] = time.time()
                
        elif event.type == EventType.WORKFLOW_COMPLETED and event.source == "CapabilityService":
            capability = event.payload.get("capability")
            req_id = event.execution_id
            if capability and req_id:
                self._init_capability(capability)
                
                # Check outcome
                result = event.payload.get("result", {})
                if result.get("status") == "success":
                    self._metrics[capability]["successes"] += 1
                else:
                    self._metrics[capability]["failures"] += 1
                    
                # Calculate runtime
                start_time = self._active_runs.pop(req_id, None)
                if start_time:
                    runtime = time.time() - start_time
                    self._metrics[capability]["total_runtime"] += runtime
                    runs = self._metrics[capability]["runs"]
                    if runs > 0:
                        self._metrics[capability]["avg_runtime"] = self._metrics[capability]["total_runtime"] / runs
