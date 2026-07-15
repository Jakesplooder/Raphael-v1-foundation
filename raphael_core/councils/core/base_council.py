from typing import Dict, Any
from .decision import CouncilDecision
from ..runtime.council_state import CouncilState

class BaseCouncil:
    def __init__(self, name: str):
        self.name = name
        self.state = CouncilState.IDLE
        
    def transition_to(self, new_state: CouncilState):
        self.state = new_state
        
    async def review_proposal(self, action_id: str, proposal: Dict[str, Any]) -> CouncilDecision:
        # Base implementation, overridden by specific councils
        return CouncilDecision(
            action_id=action_id,
            council=self.name,
            decision="APPROVED"
        )
