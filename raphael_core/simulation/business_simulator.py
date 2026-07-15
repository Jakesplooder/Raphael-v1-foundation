from .simulation_world import SimulationWorld
from .simulation_event_bus import SimulationEventBus
from .market_simulator import MarketSimulator
from .agent_simulator import AgentSimulator
from .simulation_memory import SimulationMemory

class BusinessSimulator:
    def __init__(self, event_bus: SimulationEventBus, memory: SimulationMemory):
        self.event_bus = event_bus
        self.memory = memory
        self.market_sim = MarketSimulator(event_bus)
        self.agent_sim = AgentSimulator(event_bus)

    def run_month(self, sim_id: str, world: SimulationWorld, ceo_strategy: str = "balanced"):
        if not world.is_active: return
        
        world.current_month += 1
        
        # Output value dictates product quality/marketing ability
        output_value = self.agent_sim.simulate_month(world)
        
        marketing_spend = 0
        if ceo_strategy == "aggressive_growth":
            marketing_spend = min(world.capital, 10000)
        elif ceo_strategy == "balanced":
            marketing_spend = min(world.capital, 2000)
            
        world.capital -= marketing_spend
        if marketing_spend > 0:
            self.event_bus.emit("CAPITAL_SPENT", "BusinessSimulator", {"amount": marketing_spend, "category": "marketing"})
            
        self.market_sim.simulate_month(world, marketing_spend + (output_value * 0.1))
        
        # Check bankruptcy
        if world.capital <= 0 and world.revenue < 5000:
            world.is_active = False
            self.event_bus.emit("VENTURE_FAILED", "BusinessSimulator", {"reason": "Out of capital"})
            
        self.event_bus.emit("MONTH_ADVANCED", "BusinessSimulator", {"month": world.current_month, "capital": world.capital, "revenue": world.revenue})
        
        # Log decision
        self.memory.log_decision(sim_id, {
            "month": world.current_month,
            "strategy": ceo_strategy,
            "marketing_spend": marketing_spend,
            "capital_remaining": world.capital
        })
