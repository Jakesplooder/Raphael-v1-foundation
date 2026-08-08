from pathlib import Path
from raphael_core.kernel.services.business_registry.base_twin import BaseTwin
from raphael_core.kernel.services.business_registry.lifecycle import LifecycleState

class MentorMapTwin(BaseTwin):
    def __init__(self, storage_path: Path):
        super().__init__(
            business_id="mentormap_001",
            name="MentorMap",
            category="Career Technology",
            domain="career",
            storage_path=storage_path
        )
        
        if self.version == 1:
            self.lifecycle.transition(LifecycleState.INCUBATING)
            
            self.venture_metadata = {
                "parent_portfolio": "Raphael Holdings",
                "founder": "Raphael OS",
                "incubation_budget": 500,
                "validation_deadline": "30 days",
                "success_threshold": 0.75,
                "venture_stage": "INCUBATING"
            }
            
            self.financials["investment"] = 250
            self.financials["revenue"] = 0
            
            self.strategy["current_hypothesis"] = "AI matching increases mentor discovery"
            
            self.growth["users"] = 0
            self.growth["mentors"] = 0
            
            self.operations["mvp_progress"] = 0
            
            self.confidence = 0.74 # Starting confidence based on Investment Memo
            self.risk["operational_risk"] = 0.40
