from typing import Dict, Any
from .simulation_world import SimulationWorld
from .simulation_event_bus import SimulationEventBus

class ScenarioGenerator:
    """
    Injects events and risks into the simulated world.
    """
    def __init__(self, event_bus: SimulationEventBus):
        self.event_bus = event_bus

    def apply_scenario(self, world: SimulationWorld, scenario_type: str) -> Dict[str, Any]:
        impact = {}
        if scenario_type == "bad_market":
            world.customer_demand = "low"
            world.competition_level = "very_high"
            impact = {"risk": "High", "opportunity": "Low", "description": "Market demand collapsed."}
            self.event_bus.emit("MARKET_SHIFT", "ScenarioGenerator", {"type": "bad_market"})
            
        elif scenario_type == "high_demand":
            world.customer_demand = "surging"
            impact = {"risk": "Low", "opportunity": "High", "description": "Demand is surging."}
            self.event_bus.emit("MARKET_SHIFT", "ScenarioGenerator", {"type": "high_demand"})
            
        return impact
