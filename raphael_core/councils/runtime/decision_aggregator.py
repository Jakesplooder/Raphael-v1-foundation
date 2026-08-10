import logging
from typing import List, Dict, Any
from ..core.decision import CouncilDecision

logger = logging.getLogger("rrk.councils.aggregator")

class DecisionAggregator:
    """Aggregates decisions, detects conflicts, and creates resolution plans."""
    
    def aggregate(self, decisions: List[CouncilDecision]) -> CouncilDecision:
        if not decisions:
            return CouncilDecision(action_id="UNKNOWN", council="Aggregator", decision="APPROVED")
            
        action_id = decisions[0].action_id
        
        # Conflict Detection
        rejections = [d for d in decisions if d.decision == "REJECTED"]
        revisions = [d for d in decisions if d.decision == "REVISION_REQUIRED"]
        
        if rejections:
            # If any council outright rejects, the final decision is REJECTED
            return CouncilDecision(
                action_id=action_id,
                council="Aggregator",
                decision="REJECTED",
                risks=[r for d in rejections for r in d.risks],
                severity="HIGH"
            )
            
        if revisions:
            # Impact Analysis & Resolution Plan
            all_impacts = set()
            all_changes = []
            re_reviews = set()
            
            for r in revisions:
                all_impacts.update(r.impact_domains)
                all_changes.extend(r.required_changes)
                re_reviews.add(r.council)
                re_reviews.update(r.re_review_required)
                
            return CouncilDecision(
                action_id=action_id,
                council="Aggregator",
                decision="REVISION_REQUIRED",
                required_changes=all_changes,
                impact_domains=list(all_impacts),
                re_review_required=list(re_reviews),
                severity="MEDIUM"
            )
            
        # All APPROVED
        return CouncilDecision(
            action_id=action_id,
            council="Aggregator",
            decision="APPROVED"
        )
