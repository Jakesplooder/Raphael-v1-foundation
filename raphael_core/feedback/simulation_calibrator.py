import logging
from typing import Dict, Any

logger = logging.getLogger("rrk.feedback.calibrator")

class SimulationCalibrator:
    """
    Takes prediction errors and formulates calibration proposals for D19.
    Implements Conservative Adaptive Learning (no automatic suppression).
    """
    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.simulation_models = {
            "v1.0": {"confidence_base": 0.85, "acquisition_coefficient": 1.0}
        }

    def calibrate(self, validation_result: Dict[str, Any]):
        if not validation_result:
            return
            
        sim_id = validation_result["sim_id"]
        max_error = abs(validation_result["max_error_pct"])
        errors = validation_result["errors"]
        venture_type = validation_result["venture_type"]
        
        logger.info(f"Calibrating simulation parameters for {venture_type} based on {sim_id}")
        
        proposal = {
            "target": "SimulationEngine",
            "venture_type": venture_type,
            "trigger_sim_id": sim_id,
            "action": "CALIBRATE_WEIGHTS"
        }
        
        if max_error <= 0.10:
            logger.info("0-10% Error: Normal range. No calibration needed.")
            return
            
        elif max_error <= 0.25:
            logger.info(f"10-25% Error: Minor Calibration. Max Error: {max_error}")
            proposal["adjustments"] = {"confidence_base": -0.05}
            if errors.get("customers_error_pct", 0) < -0.1:
                 proposal["adjustments"]["acquisition_coefficient"] = -0.10
            
        elif max_error <= 0.50:
            logger.info(f"25-50% Error: Major Calibration. Max Error: {max_error}")
            proposal["adjustments"] = {"confidence_base": -0.15}
            if errors.get("customers_error_pct", 0) < -0.2:
                 proposal["adjustments"]["acquisition_coefficient"] = -0.20
            
        else:
            logger.warning(f"50%+ Error: SIMULATION_WARNING. Max Error: {max_error}")
            logger.warning(f"Actions: Lower confidence significantly, require more evidence.")
            proposal["adjustments"] = {"confidence_base": -0.30, "requires_council_review": True}
            if errors.get("customers_error_pct", 0) < -0.4:
                 proposal["adjustments"]["acquisition_coefficient"] = -0.40
            
        # Emit improvement proposal to D19 EventBus
        self.event_bus.emit("IMPROVEMENT_PROPOSAL", "SimulationCalibrator", proposal)
        return proposal
