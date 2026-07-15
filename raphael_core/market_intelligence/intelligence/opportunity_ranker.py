import logging
from typing import List, Dict, Any
from ..analysis.opportunity_scorer import OpportunityScorer
from .opportunity_state import OpportunityState

logger = logging.getLogger("rrk.market.ranker")

class OpportunityRanker:
    """
    Sorts and filters opportunities based on their Opportunity Intelligence Score (OIS).
    Rejects those that fall below the acceptable threshold.
    """
    def __init__(self, threshold: float = 70.0):
        self.scorer = OpportunityScorer()
        self.threshold = threshold

    def rank_opportunities(self, opportunities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ranked = []
        for opp in opportunities:
            if "ois_score" not in opp:
                opp["ois_score"] = self.scorer.calculate_ois(opp.get("metrics", {}))
                
            if opp["ois_score"] < self.threshold:
                opp["state"] = OpportunityState.REJECTED
                logger.info(f"Rejected Opportunity: {opp.get('name')} (Score: {opp['ois_score']})")
            else:
                opp["state"] = OpportunityState.ANALYZING
                ranked.append(opp)
                
        # Sort descending by OIS
        ranked.sort(key=lambda x: x["ois_score"], reverse=True)
        return ranked
