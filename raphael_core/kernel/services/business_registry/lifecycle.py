from enum import Enum

class LifecycleState(Enum):
    IDEA = "IDEA"
    PROPOSED = "PROPOSED"
    EVALUATING = "EVALUATING"
    APPROVED = "APPROVED"
    INCUBATING = "INCUBATING"
    VALIDATING = "VALIDATING"
    ACTIVE = "ACTIVE"
    SCALING = "SCALING"
    EXITED = "EXITED"
    RETIRED = "RETIRED"

class BusinessLifecycle:
    def __init__(self, initial_state: str = "PROPOSED"):
        self.state = LifecycleState(initial_state)
        
    def transition(self, new_state: LifecycleState) -> bool:
        # Simple permissive state machine for now, can be constrained later
        self.state = new_state
        return True
        
    def get_state(self) -> str:
        return self.state.value
