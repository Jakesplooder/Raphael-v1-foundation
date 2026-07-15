import uuid
import logging
from typing import Dict, Any

from .simulation_config import SimulationConfig
from .simulation_event_bus import SimulationEventBus
from .simulation_memory import SimulationMemory
from .simulation_world import SimulationWorld
from .scenario_generator import ScenarioGenerator
from .business_simulator import BusinessSimulator
from .outcome_predictor import OutcomePredictor
from .reality_transfer import RealityTransfer

logger = logging.getLogger("rrk.simulation.runtime")

class SimulationRuntime:
    """
    Orchestrates the entire execution lifecycle of a temporary reality simulation.
    """
    def __init__(self, config: SimulationConfig = None):
        self.config = config or SimulationConfig.standard()
        self.event_bus = SimulationEventBus()
        self.memory = SimulationMemory()
        
        self.scenario_gen = ScenarioGenerator(self.event_bus)
        self.business_sim = BusinessSimulator(self.event_bus, self.memory)
        self.predictor = OutcomePredictor(self.event_bus)
        self.transfer = RealityTransfer(self.event_bus)

    def run_simulation(self, venture_type: str, initial_capital: float, team: list, 
                       market_scenario: str = "normal", ceo_strategy: str = "balanced") -> Dict[str, Any]:
                       
        sim_id = f"SIM-{str(uuid.uuid4())[:8].upper()}"
        self.event_bus.emit("SIMULATION_STARTED", "SimulationRuntime", {"id": sim_id, "venture": venture_type})
        
        # 1. Initialize World
        world = SimulationWorld(
            market=venture_type,
            competition_level="normal",
            customer_demand="normal",
            starting_capital=initial_capital,
            team=team
        )
        
        self.memory.initialize_simulation(sim_id, venture_type, world.get_state())
        
        # 2. Inject Scenario
        if market_scenario != "normal":
            self.scenario_gen.apply_scenario(world, market_scenario)
            
        # 3. Execution Loop
        for month in range(1, self.config.duration_months + 1):
            if not world.is_active:
                break
            self.business_sim.run_month(sim_id, world, ceo_strategy=ceo_strategy)
            
        # 4. Predict Outcome
        outcome = self.predictor.predict(world, initial_capital)
        self.memory.finalize_simulation(sim_id, outcome)
        
        # 5. Reality Transfer if requested
        if outcome["recommendation"] == "PROCEED" and self.config.allow_reality_transfer:
            self.transfer.transfer(sim_id, world.get_state(), outcome)
            
        return outcome
