import uuid
from typing import Dict, Any, Tuple
from ..kernel.models.business_objects import Decision, ROIAnalysis, RiskAssessment, BusinessState
from .roi_engine import ROIEngine
from .risk_engine import RiskEngine
from .executive_council import ExecutiveDecisionCouncil
from ..kernel.event_bus import global_event_bus
from ..kernel.interfaces import Event
import time
import asyncio

class DecisionEngine:
    def __init__(self):
        self.roi_engine = ROIEngine()
        self.risk_engine = RiskEngine()
        self.council = ExecutiveDecisionCouncil()
        
    def evaluate_opportunity(self, business_state: BusinessState, proposal: str, investment: float, expected_revenue: float) -> Tuple[Decision, ROIAnalysis, list[RiskAssessment]]:
        # 1. Create initial decision object
        decision = Decision(
            id=f"dec_{uuid.uuid4().hex[:8]}",
            business_id=business_state.business_id,
            decision_type="opportunity_evaluation",
            proposal=proposal,
            status="awaiting_approval"
        )
        
        # 2. Run ROI analysis
        roi = self.roi_engine.evaluate(decision.id, investment, expected_revenue)
        decision.expected_return = roi.expected_profit
        
        # 3. Run Risk assessment
        risks = self.risk_engine.evaluate(decision.id, proposal, business_state)
        decision.risks = [r.risk_description for r in risks]
        
        # 4. Council Review
        decision = self.council.review(decision, roi, risks, business_state)
        
        # 5. Emit approval requested event
        if decision.status == "awaiting_approval":
            # Fire and forget if called sync, or better to use asyncio.run if this is sync but we're in a mixed context.
            # wait, the event bus `publish` is async. We should handle it properly.
            # Assuming `evaluate_opportunity` is sync, we can use an asyncio task if event loop is running, or create one.
            # Let's do a safe dispatch
            payload = {
                "decision_id": decision.id,
                "business_id": decision.business_id,
                "proposal": decision.proposal,
                "expected_return": getattr(decision, 'expected_return', 0.0),
                "risk_level": "Unknown" if not risks else "High" if len(risks) > 2 else "Medium"
            }
            evt = Event(id=f"evt_{uuid.uuid4().hex[:8]}", timestamp=time.time(), source="decision_engine", type="approval_requested", payload=payload)
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(global_event_bus.publish(evt))
            except RuntimeError:
                asyncio.run(global_event_bus.publish(evt))
        
        return decision, roi, risks
