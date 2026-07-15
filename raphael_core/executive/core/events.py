from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any, Callable, List

class ExecutiveEventType(str, Enum):
    KPI_UPDATED = "KPI_UPDATED"
    GOAL_AT_RISK = "GOAL_AT_RISK"
    TARGET_ACHIEVED = "TARGET_ACHIEVED"
    PERFORMANCE_DEGRADED = "PERFORMANCE_DEGRADED"
    OPPORTUNITY_CREATED = "OPPORTUNITY_CREATED"
    GOAL_CREATED = "GOAL_CREATED"
    GOAL_COMPLETED = "GOAL_COMPLETED"
    INITIATIVE_BLOCKED = "INITIATIVE_BLOCKED"
    VENTURE_CREATED = "VENTURE_CREATED"
    VENTURE_AT_RISK = "VENTURE_AT_RISK"
    OPPORTUNITY_DISCOVERED = "OPPORTUNITY_DISCOVERED"
    STRATEGIC_REVIEW_REQUIRED = "STRATEGIC_REVIEW_REQUIRED"

class ExecutiveEvent(BaseModel):
    event_type: ExecutiveEventType
    source: str
    payload: Dict[str, Any]

class ExecutiveEventBus:
    def __init__(self):
        self.subscribers: Dict[ExecutiveEventType, List[Callable]] = {e: [] for e in ExecutiveEventType}
        
    def subscribe(self, event_type: ExecutiveEventType, handler: Callable):
        self.subscribers[event_type].append(handler)
        
    def emit(self, event: ExecutiveEvent):
        for handler in self.subscribers.get(event.event_type, []):
            handler(event)
