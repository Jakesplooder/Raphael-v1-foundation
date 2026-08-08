import uuid
from typing import Dict, Any, List
from ..kernel.models.business_objects import RiskAssessment, BusinessState

class RiskEngine:
    def __init__(self):
        pass
        
    def evaluate(self, decision_id: str, proposal: str, business_state: BusinessState) -> List[RiskAssessment]:
        risks = []
        
        # Heuristic rules based on user prompt for mock
        if "ads" in proposal.lower() or "advertising" in proposal.lower():
            risks.append(RiskAssessment(
                id=f"risk_{uuid.uuid4().hex[:8]}",
                decision_id=decision_id,
                risk_description="Audience validation incomplete",
                probability=0.45,
                impact="High",
                mitigation_strategy="Run small validation experiment first"
            ))
            
        if "scale" in proposal.lower() or "expand" in proposal.lower() or "increase" in proposal.lower():
            risks.append(RiskAssessment(
                id=f"risk_{uuid.uuid4().hex[:8]}",
                decision_id=decision_id,
                risk_description="Operational bottleneck",
                probability=0.3,
                impact="Medium",
                mitigation_strategy="Ensure builder capacity is sufficient"
            ))
            
        return risks
