import logging
from typing import Dict, Any, List
from .council_state import CouncilState
from ..core.decision import CouncilDecision

logger = logging.getLogger("rrk.councils.runtime")

class CouncilRuntime:
    """Controls the lifecycle of a Council review."""
    
    async def run_review(self, council, action_id: str, proposal: Dict[str, Any]) -> CouncilDecision:
        logger.info(f"[{council.name}] Starting review for Action {action_id}")
        
        council.transition_to(CouncilState.REVIEWING)
        
        council.transition_to(CouncilState.DELIBERATING)
        
        council.transition_to(CouncilState.VOTING)
        decision = await council.review_proposal(action_id, proposal)
        
        council.transition_to(CouncilState.DECISION_READY)
        logger.info(f"[{council.name}] Decision: {decision.decision} (Confidence: {decision.confidence:.2f})")
        
        council.transition_to(CouncilState.MEMORY_UPDATE)
        
        council.transition_to(CouncilState.COMPLETE)
        return decision
