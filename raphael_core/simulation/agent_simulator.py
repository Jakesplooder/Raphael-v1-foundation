from .simulation_world import SimulationWorld
from .simulation_event_bus import SimulationEventBus

class AgentSimulator:
    """
    Simulates employee performance ROI. 
    Contrasts high performance vs average employees.
    """
    def __init__(self, event_bus: SimulationEventBus):
        self.event_bus = event_bus

    def simulate_month(self, world: SimulationWorld):
        if not world.is_active: return
        
        total_salary = 0
        total_output_value = 0.0
        
        for member in world.team:
            perf = member.get("performance", 75)
            salary = member.get("monthly_cost", 5000)
            
            # High performers cost more but output non-linearly more value
            output_multiplier = (perf / 75.0) ** 1.5
            output_value = 5000 * output_multiplier
            
            total_salary += salary
            total_output_value += output_value
            
        world.capital -= total_salary
        self.event_bus.emit("CAPITAL_SPENT", "AgentSimulator", {"amount": total_salary, "category": "payroll"})
        
        return total_output_value
