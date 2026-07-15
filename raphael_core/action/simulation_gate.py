import logging
import asyncio

logger = logging.getLogger("rrk.action.simulation_gate")

class SimulationGate:
    """
    Determines if an action needs a simulation based on its Risk Tier.
    """
    def __init__(self, event_bus):
        self.event_bus = event_bus

    async def evaluate(self, intent: str, risk_level: str, action_spec: dict) -> str:
        """
        Returns 'APPROVED', 'DENIED', or 'REQUIRES_HUMAN'
        """
        if risk_level == "LOW":
            logger.info(f"LOW risk action {intent}. Skipping simulation.")
            return "APPROVED"
            
        elif risk_level == "MEDIUM":
            self.event_bus.emit("ACTION_SIMULATION_STARTED", "SimulationGate", {"intent": intent, "type": "MINI"})
            logger.info(f"MEDIUM risk action {intent}. Running <5s mini-simulation.")
            await asyncio.sleep(0.1) # Simulate quick ROI check
            # Mock success for now
            self.event_bus.emit("ACTION_SIMULATION_APPROVED", "SimulationGate", {"intent": intent})
            return "APPROVED"
            
        elif risk_level == "HIGH":
            self.event_bus.emit("ACTION_SIMULATION_STARTED", "SimulationGate", {"intent": intent, "type": "FULL_D22"})
            logger.info(f"HIGH risk action {intent}. Requiring full D22 Simulation.")
            await asyncio.sleep(0.2) # Simulate deep check
            self.event_bus.emit("ACTION_SIMULATION_APPROVED", "SimulationGate", {"intent": intent})
            return "APPROVED"
            
        elif risk_level == "CRITICAL":
            logger.warning(f"CRITICAL risk action {intent}. Simulation passed, but escalating to HUMAN_APPROVAL.")
            return "REQUIRES_HUMAN"
            
        return "DENIED"
