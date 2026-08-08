from pathlib import Path
from raphael_core.kernel.services.business_registry.base_twin import BaseTwin
from raphael_core.kernel.services.business_registry.lifecycle import LifecycleState

class AIStoreTwin(BaseTwin):
    """
    AI Store — Commerce Division
    A curated e-commerce platform for AI hardware, software tools, and digital products.
    Inherits from BaseTwin. Does not copy Creator logic.
    """
    def __init__(self, storage_path: Path):
        super().__init__(
            business_id="ai_store_001",
            name="AI Store",
            category="Commerce Technology",
            domain="commerce",
            storage_path=storage_path
        )
        
        if self.version == 1:
            self.lifecycle.transition(LifecycleState.INCUBATING)
            
            self.venture_metadata = {
                "venture_id": "ai_store_001",
                "division": "commerce",
                "parent_portfolio": "Raphael Holdings",
                "founder": "Raphael OS",
                "capital_source": "exploration_pool",
                "incubation_budget": 500,
                "validation_deadline": "30 days",
                "success_threshold": 0.75,
                "venture_stage": "INCUBATING"
            }
            
            self.financials["investment"] = 300
            self.financials["revenue"] = 0
            self.financials["cogs"] = 0
            self.financials["gross_margin"] = 0
            
            self.strategy["current_hypothesis"] = "AI professionals will pay premium for curated, reliable AI tools and hardware"
            self.strategy["business_model"] = "transaction_economy"
            
            self.growth["products_listed"] = 0
            self.growth["validated_suppliers"] = 0
            self.growth["transactions"] = 0
            self.growth["monthly_visitors"] = 0
            
            self.operations["mvp_progress"] = 0
            self.operations["storefront_status"] = "not_started"
            
            self.confidence = 0.35
            self.risk["operational_risk"] = 0.35
            self.risk["supply_chain_risk"] = 0.25
            self.risk["customer_acquisition_risk"] = 0.40
