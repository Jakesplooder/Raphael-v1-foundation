from typing import Dict, Any, List
from .allocation_engine import AllocationEngine
from raphael_core.kernel.event_bus import emit

class ResourceScheduler:
    def __init__(self, engine: AllocationEngine):
        self.engine = engine
        
    def schedule_cycle(self, registry_businesses: List[Dict[str, Any]], available_gpu: int, available_budget: float):
        """
        Takes the raw businesses from the registry, extracts their twin and metadata,
        and asks the engine to allocate resources.
        Then emits RESOURCE_GRANTED for each.
        """
        # Format for engine: {"twin": BaseTwin, "opportunity": float, "strategic_importance": float}
        # For simulation, we'll mock opportunity and strategic importance if not provided by registry requirements.
        engine_input = []
        for b_data in registry_businesses:
            twin = b_data["twin"]
            reqs = b_data.get("requirements", {})
            engine_input.append({
                "twin": twin,
                "opportunity": reqs.get("opportunity_score", 0.5),
                "strategic_importance": reqs.get("strategic_importance", 0.5)
            })
            
        allocations = self.engine.allocate_resources(engine_input, available_gpu, available_budget)
        
        for business_id, alloc in allocations.items():
            emit("PORTFOLIO.RESOURCE_GRANTED", "ResourceScheduler", {
                "business_id": business_id,
                "allocation": alloc
            })
            
        return allocations
