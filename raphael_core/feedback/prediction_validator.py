import logging
from typing import Dict, Any
from ..simulation.simulation_memory import SimulationMemory
from .outcome_memory import OutcomeMemory

logger = logging.getLogger("rrk.feedback.validator")

class PredictionValidator:
    """
    Compares original Simulation Predictions against Actual Reality Data.
    Calculates Prediction Error %.
    """
    def __init__(self, sim_memory: SimulationMemory, outcome_memory: OutcomeMemory):
        self.sim_memory = sim_memory
        self.outcome_memory = outcome_memory

    def calculate_errors(self, sim_id: str) -> Dict[str, Any]:
        # Load prediction from simulation memory (final outcome state)
        sim_data = self.sim_memory.load_state(sim_id, status="completed")
        # Load reality from outcome memory
        reality_data = self.outcome_memory.get_reality_data(sim_id)
        
        if not sim_data or not reality_data:
            logger.warning(f"Incomplete data for validation on {sim_id}")
            return {}
            
        prediction = sim_data.get("outcome", {})
        reality_kpis = reality_data.get("kpis", {})
        
        errors = {}
        # Calculate revenue error
        if "revenue" in prediction and "revenue" in reality_kpis:
            p_rev = prediction["revenue"]
            r_rev = reality_kpis["revenue"]
            if p_rev > 0:
                err = (r_rev - p_rev) / p_rev
                errors["revenue_error_pct"] = round(err, 4)
                
        # Calculate customers error
        if "customers" in prediction and "customers" in reality_kpis:
            p_cust = prediction["customers"]
            r_cust = reality_kpis["customers"]
            if p_cust > 0:
                err = (r_cust - p_cust) / p_cust
                errors["customers_error_pct"] = round(err, 4)
                
        # Max error determines severity
        max_error = 0.0
        for k, v in errors.items():
            if abs(v) > abs(max_error):
                max_error = v
                
        result = {
            "sim_id": sim_id,
            "errors": errors,
            "max_error_pct": max_error,
            "venture_type": sim_data.get("venture_type", "unknown")
        }
        return result
