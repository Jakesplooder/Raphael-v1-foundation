from .simulation_world import SimulationWorld
from .simulation_event_bus import SimulationEventBus

class MarketSimulator:
    def __init__(self, event_bus: SimulationEventBus):
        self.event_bus = event_bus

    def simulate_month(self, world: SimulationWorld, marketing_spend: float):
        if not world.is_active: return
        
        # Simple heuristic simulation
        acquisition_rate = 1.0
        if world.customer_demand == "surging":
            acquisition_rate = 3.0
        elif world.customer_demand == "low":
            acquisition_rate = 0.2
            
        if world.competition_level == "very_high":
            acquisition_rate *= 0.5
            
        new_customers = int(marketing_spend * 0.05 * acquisition_rate)
        world.customers_acquired += new_customers
        
        # Assume $10 MRR per customer
        world.revenue += (world.customers_acquired * 10)
        
        if new_customers > 0:
            self.event_bus.emit("CUSTOMER_ACQUIRED", "MarketSimulator", {"new_customers": new_customers})
