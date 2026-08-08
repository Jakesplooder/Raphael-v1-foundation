from pathlib import Path
from raphael_core.kernel.services.business_registry.base_twin import BaseTwin
from raphael_core.kernel.services.business_registry.lifecycle import LifecycleState

class BusinessTwin(BaseTwin):
    def __init__(self, business_id: str, storage_path: Path):
        super().__init__(
            business_id=business_id,
            name="Focus Marketing",
            category="Marketing Education",
            domain="Creator",
            storage_path=storage_path
        )
        
        # Override initial risk and confidence for Focus Marketing (established)
        if self.version == 1:
            self.lifecycle.transition(LifecycleState.ACTIVE)
            self.confidence = 0.97
            self.risk["operational_risk"] = 0.05
            self.risk["financial_risk"] = 0.02
