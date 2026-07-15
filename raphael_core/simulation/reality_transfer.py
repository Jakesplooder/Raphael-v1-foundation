import uuid
import logging
from typing import Dict, Any
from .simulation_event_bus import SimulationEventBus
from ..kernel.event_bus import emit as global_emit

logger = logging.getLogger("rrk.simulation.reality")

class RealityTransfer:
    """
    Transforms a successful simulation into a real-world venture blueprint.
    """
    def __init__(self, event_bus: SimulationEventBus):
        self.event_bus = event_bus

    def transfer(self, sim_id: str, world_state: Dict[str, Any], outcome: Dict[str, Any]) -> str:
        if outcome.get("recommendation") != "PROCEED":
            logger.warning(f"Cannot transfer {sim_id}: recommendation is ABORT.")
            return ""
            
        venture_id = f"VENTURE-{str(uuid.uuid4())[:8].upper()}"
        
        # Emit a reality-level event crossing the boundary from simulation to kernel
        global_emit("REALITY_TRANSFER_APPROVED", "RealityTransfer", {
            "source_simulation": sim_id,
            "venture_id": venture_id,
            "market": world_state.get("market"),
            "predicted_roi": outcome.get("roi")
        })
        
        logger.info(f"Simulation {sim_id} successfully transferred to reality as {venture_id}.")
        return venture_id
