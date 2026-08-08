from typing import Dict, Any, List
from raphael_core.kernel.event_bus import emit
from .base_twin import BaseTwin

class BusinessRegistry:
    def __init__(self):
        self.businesses: Dict[str, BaseTwin] = {}
        self.resource_requirements: Dict[str, Dict[str, Any]] = {}
        
    def register(self, twin: BaseTwin, requirements: Dict[str, Any]):
        business_id = twin.identity["business_id"]
        
        self.businesses[business_id] = twin
        self.resource_requirements[business_id] = requirements
        
        emit("BUSINESS.REGISTERED", "BusinessRegistry", {
            "business_id": business_id,
            "name": twin.identity["name"],
            "domain": twin.identity["domain"],
            "requirements": requirements
        })
        
    def get_business(self, business_id: str) -> BaseTwin:
        return self.businesses.get(business_id)
        
    def get_all_businesses(self) -> List[BaseTwin]:
        return list(self.businesses.values())
        
    def get_requirements(self, business_id: str) -> Dict[str, Any]:
        return self.resource_requirements.get(business_id, {})

business_registry = BusinessRegistry()
