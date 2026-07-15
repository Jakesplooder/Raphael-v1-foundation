from typing import Dict, Any
from .simulation_world import SimulationWorld
from .simulation_event_bus import SimulationEventBus

class OutcomePredictor:
    def __init__(self, event_bus: SimulationEventBus):
        self.event_bus = event_bus

    def predict(self, world: SimulationWorld, initial_capital: float) -> Dict[str, Any]:
        success = world.is_active and world.revenue > 0
        roi = 0.0
        if success:
            roi = (world.revenue + world.capital) / initial_capital if initial_capital > 0 else 0
            
        success_prob = 0.8 if success and roi > 1.2 else 0.4 if success else 0.1
        
        confidence = 0.85
        risk_factors = []
        if world.competition_level == "very_high":
            risk_factors.append("High competition reduces acquisition efficiency.")
            confidence -= 0.15
            
        if world.customer_demand == "low":
            risk_factors.append("Low market demand requires high marketing spend.")
            confidence -= 0.2
            
        outcome = {
            "success": success,
            "success_probability": success_prob,
            "confidence": round(confidence, 2),
            "roi": round(roi, 2),
            "customers": world.customers_acquired,
            "risk_factors": risk_factors,
            "recommendation": "PROCEED" if success_prob > 0.7 else "ABORT"
        }
        
        self.event_bus.emit("SIMULATION_COMPLETED", "OutcomePredictor", outcome)
        return outcome
