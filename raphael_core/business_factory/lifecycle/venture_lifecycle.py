from enum import Enum
import logging

logger = logging.getLogger("rrk.business_factory.lifecycle")

class VentureState(str, Enum):
    IDEA = "IDEA"
    VALIDATING = "VALIDATING"
    CREATED = "CREATED"
    LAUNCHING = "LAUNCHING"
    OPERATING = "OPERATING"
    GROWING = "GROWING"
    SCALING = "SCALING"
    PIVOTING = "PIVOTING"
    ACQUIRED = "ACQUIRED"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"

class VentureLifecycle:
    def __init__(self):
        self.ventures = {}
        
    def register(self, venture_id: str):
        self.ventures[venture_id] = VentureState.IDEA
        logger.info(f"[Lifecycle] {venture_id} registered as IDEA")
        
    def transition(self, venture_id: str, new_state: VentureState):
        old = self.ventures.get(venture_id, "UNKNOWN")
        self.ventures[venture_id] = new_state
        logger.info(f"[Lifecycle] {venture_id}: {old} -> {new_state.value}")
        
    def get_state(self, venture_id: str) -> VentureState:
        return self.ventures.get(venture_id, None)
        
    def decide(self, venture_id: str, revenue_trend: str, kpi_health: str) -> str:
        if revenue_trend == "NEGATIVE" and kpi_health == "WARNING":
            self.transition(venture_id, VentureState.PIVOTING)
            return "PIVOT"
        elif revenue_trend == "POSITIVE" and kpi_health == "HEALTHY":
            self.transition(venture_id, VentureState.GROWING)
            return "SCALE"
        elif revenue_trend == "CRITICAL" and kpi_health == "CRITICAL":
            self.transition(venture_id, VentureState.FAILED)
            return "SHUTDOWN"
        return "CONTINUE"
