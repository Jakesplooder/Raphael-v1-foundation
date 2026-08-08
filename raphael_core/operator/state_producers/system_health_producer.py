from typing import Dict, Any
import time
from .executive_state import StateProducer, ProducerResult

class SystemHealthProducer(StateProducer):
    """
    Produces raw facts about the overall system health, bridging the existing
    kernel health modules into the ExecutiveState.
    """
    def name(self) -> str:
        return "system_health_core"
        
    def category(self) -> str:
        return "system"
        
    def collect(self) -> ProducerResult:
        try:
            from raphael_core.kernel.health import system_health
            
            # system_health() is synchronous and returns the health dict
            data = system_health()
            
            # Simple assumption: if overall is healthy, completeness is 1.0
            completeness = 1.0 if data.get("overall") == "healthy" else 0.8
            
            return ProducerResult(
                producer_name=self.name(),
                success=True,
                data=data,
                completeness=completeness
            )
        except Exception as e:
            return ProducerResult(
                producer_name=self.name(),
                success=False,
                data={},
                completeness=0.0,
                errors=[f"Failed to collect system health: {str(e)}"]
            )
