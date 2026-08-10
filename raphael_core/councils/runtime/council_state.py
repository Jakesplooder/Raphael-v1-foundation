from enum import Enum

class CouncilState(str, Enum):
    IDLE = "idle"
    REVIEWING = "reviewing"
    DELIBERATING = "deliberating"
    VOTING = "voting"
    DECISION_READY = "decision_ready"
    MEMORY_UPDATE = "memory_update"
    COMPLETE = "complete"
