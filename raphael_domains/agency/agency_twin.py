from pathlib import Path
from raphael_core.kernel.services.business_registry.base_twin import BaseTwin
from raphael_core.kernel.services.business_registry.lifecycle import LifecycleState

class AgencyTwin(BaseTwin):
    """
    Raphael Agency — Service Economy Division
    
    An AI-powered services agency offering marketing automation, cybersecurity audits,
    and business process automation to external clients.
    
    Unlike Creator (attention), Career (network), or Commerce (transaction),
    the Agency operates on a SERVICE ECONOMY model:
    - Revenue comes from client contracts and recurring service delivery
    - Growth is measured by clients, MRR, and delivery capacity
    - The Agency can potentially fund other ventures through internal cash flow
    
    Inherits from BaseTwin. Does not copy Creator logic.
    """
    def __init__(self, storage_path: Path):
        super().__init__(
            business_id="agency_001",
            name="Raphael Agency",
            category="AI Services",
            domain="agency",
            storage_path=storage_path
        )
        
        if self.version == 1:
            self.lifecycle.transition(LifecycleState.INCUBATING)
            
            self.venture_metadata = {
                "venture_id": "agency_001",
                "division": "agency",
                "parent_portfolio": "Raphael Holdings",
                "founder": "Raphael OS",
                "capital_source": "exploration_pool",
                "incubation_budget": 400,
                "validation_deadline": "30 days",
                "success_threshold": 0.70,
                "venture_stage": "INCUBATING",
                "strategic_role": "internal_cash_flow_engine"
            }
            
            # --- Service Economy Financials ---
            self.financials["investment"] = 400
            self.financials["revenue"] = 0
            self.financials["monthly_recurring_revenue"] = 0
            self.financials["service_margin"] = 0
            self.financials["customer_acquisition_cost"] = 0
            self.financials["lifetime_value"] = 0
            
            # --- Client & Contract Metrics ---
            self.operations["clients"] = 0
            self.operations["contracts"] = 0
            self.operations["active_engagements"] = 0
            self.operations["delivery_capacity"] = 5  # max concurrent clients
            self.operations["delivery_quality_score"] = 0
            self.operations["utilization_rate"] = 0    # delivery_capacity usage %
            self.operations["mvp_progress"] = 0
            
            # --- Service Lines ---
            self.strategy["business_model"] = "service_economy"
            self.strategy["current_hypothesis"] = "AI automation reduces service delivery cost by 60%, enabling profitable agency operations at scale"
            self.strategy["service_lines"] = [
                {"name": "Marketing Automation", "status": "planned", "revenue": 0},
                {"name": "Cybersecurity Audits", "status": "planned", "revenue": 0},
                {"name": "Business Process Automation", "status": "planned", "revenue": 0}
            ]
            
            # --- Growth Metrics ---
            self.growth["pipeline_leads"] = 0
            self.growth["conversion_rate"] = 0
            self.growth["churn_rate"] = 0
            self.growth["net_revenue_retention"] = 0
            
            # --- Risk Profile ---
            self.confidence = 0.60
            self.risk["operational_risk"] = 0.20       # Lower — services are less risky than products
            self.risk["client_concentration_risk"] = 0.30
            self.risk["talent_dependency_risk"] = 0.15  # AI agents reduce this
            self.risk["delivery_risk"] = 0.20
