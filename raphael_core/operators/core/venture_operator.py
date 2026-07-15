import logging
from typing import Optional
from ..runtime.operator_state import OperatorState
from .operator_manifest import OperatorManifest
from .operator_intent import OperatorIntent
from ..runtime.authority_manager import AuthorityManager

logger = logging.getLogger("rrk.operators.base")

class VentureOperator:
    def __init__(self, venture_id: str, manifest: OperatorManifest, authority_manager: AuthorityManager):
        self.venture_id = venture_id
        self.manifest = manifest
        self.authority_manager = authority_manager
        self.state: OperatorState = OperatorState.IDLE
        self.current_authority_level = 1
        
    def transition_to(self, new_state: OperatorState):
        logger.info(f"[{self.manifest.name}] State transition: {self.state.value} -> {new_state.value}")
        self.state = new_state
        
    def propose_intent(self, intent_str: str, actions: list, outcomes: dict, required_level: int = 1, escalation_reason: str = "") -> str:
        intent = OperatorIntent(
            venture_id=self.venture_id,
            operator=self.manifest.name,
            intent=intent_str,
            actions=actions,
            expected_outcomes=outcomes,
            authority_required=required_level,
            current_authority=self.current_authority_level,
            escalation_reason=escalation_reason
        )
        return self.authority_manager.evaluate_intent(intent)
        
    def tick(self):
        # Base implementation, overridden by specific CEOs
        pass
