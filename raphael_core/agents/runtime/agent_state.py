from enum import Enum

class AgentState(str, Enum):
    IDLE = "idle"
    REASONING = "reasoning"
    PLANNING = "planning"
    DELEGATING = "delegating"
    EXECUTING = "executing"
    REVIEWING = "reviewing"
    LEARNING = "learning"
    COMPLETE = "complete"
    FAILED = "failed"
