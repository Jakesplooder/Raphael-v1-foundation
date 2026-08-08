from typing import List, Dict, Any
from raphael_core.kernel.services.business_registry.base_twin import BaseTwin

class OpportunityRanker:
    def __init__(self):
        self.weights = {
            "roi": 0.30,
            "confidence": 0.25,
            "opportunity": 0.20,
            "strategic_importance": 0.15,
            "risk": 0.10
        }
        
    def score_business(self, twin: BaseTwin, opportunity_score: float, strategic_importance: float) -> float:
        roi = twin.financials.get("roi", 0.0)
        
        # Normalize ROI to a 0-1 scale loosely (assuming ROI is typically 0-10)
        norm_roi = min(1.0, max(0.0, roi / 10.0))
        
        confidence = twin.confidence
        risk = twin.risk.get("operational_risk", 0.10)
        
        score = (
            (norm_roi * self.weights["roi"]) +
            (confidence * self.weights["confidence"]) +
            (opportunity_score * self.weights["opportunity"]) +
            (strategic_importance * self.weights["strategic_importance"])
        ) - (risk * self.weights["risk"])
        
        return max(0.0, round(score, 4))
        
    def rank_portfolio(self, businesses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Expects a list of dicts: {"twin": BaseTwin, "opportunity": float, "strategic_importance": float}
        Returns the list sorted by score descending, with 'score' injected.
        """
        ranked = []
        for b in businesses:
            score = self.score_business(b["twin"], b.get("opportunity", 0.5), b.get("strategic_importance", 0.5))
            b["score"] = score
            ranked.append(b)
            
        return sorted(ranked, key=lambda x: x["score"], reverse=True)
