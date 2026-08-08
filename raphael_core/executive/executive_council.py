from typing import List
from ..kernel.models.business_objects import Decision, ROIAnalysis, RiskAssessment, BusinessState

class ExecutiveDecisionCouncil:
    def __init__(self):
        pass
        
    def review(self, decision: Decision, roi: ROIAnalysis, risks: List[RiskAssessment], state: BusinessState) -> Decision:
        # Heuristic scoring
        risk_score = 0
        for r in risks:
            if r.impact == "High":
                risk_score += 3
            elif r.impact == "Medium":
                risk_score += 2
            else:
                risk_score += 1
                
        # Calculate composite confidence
        # Simple heuristic: positive ROI gives base confidence, high risks subtract
        base_confidence = roi.confidence
        risk_penalty = min(0.5, risk_score * 0.1)
        
        decision.confidence = max(0.1, base_confidence - risk_penalty)
        
        # Decision Logic
        if roi.roi_percentage < 0.5:
            decision.status = "rejected"
            decision.supporting_data["reason"] = "Insufficient ROI"
        elif any(r.impact == "High" for r in risks):
            decision.status = "approved_with_conditions"
            decision.supporting_data["condition"] = "Require validation experiment first due to high risk"
        else:
            decision.status = "approved"
            
        return decision
