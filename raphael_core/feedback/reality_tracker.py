import logging
from typing import Dict, Any
from .outcome_memory import OutcomeMemory

logger = logging.getLogger("rrk.feedback.tracker")

class RealityTracker:
    """
    Hybrid event + scheduled tracker. Listens for immediate reality updates
    and persists them, ready for the scheduled validator to process.
    """
    def __init__(self, event_bus, memory: OutcomeMemory):
        self.event_bus = event_bus
        self.memory = memory
        
        # Subscribe to real-time events
        self.event_bus.subscribe("REALITY_KPI_UPDATED", self._handle_kpi_update)
        self.event_bus.subscribe("VENTURE_HEALTH_CHANGED", self._handle_health_change)

    async def _handle_kpi_update(self, event: dict):
        payload = event.get("payload", {})
        sim_id = payload.get("source_simulation_id")
        metric = payload.get("metric")
        value = payload.get("value")
        
        if sim_id and metric:
            self.memory.log_reality_kpi(sim_id, metric, value)
            logger.info(f"Reality tracker logged KPI: {metric}={value} for {sim_id}")

    async def _handle_health_change(self, event: dict):
        payload = event.get("payload", {})
        sim_id = payload.get("source_simulation_id")
        status = payload.get("status")
        
        if sim_id and status:
            self.memory.log_reality_kpi(sim_id, "health_status", status)
            logger.warning(f"Venture health change detected for {sim_id}: {status}")
