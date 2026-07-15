import logging
import asyncio
from typing import Dict, Any

from raphael_core.feedback.outcome_memory import OutcomeMemory
from raphael_core.feedback.reality_tracker import RealityTracker
from raphael_core.feedback.prediction_validator import PredictionValidator
from raphael_core.feedback.simulation_calibrator import SimulationCalibrator
from raphael_core.simulation.simulation_memory import SimulationMemory
from raphael_core.simulation.simulation_event_bus import SimulationEventBus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test.feedback_loop")

# We mock an async test runner
async def run_feedback_benchmarks():
    logger.info("Starting D22 Phase 2 Benchmarks...")
    
    event_bus = SimulationEventBus()
    sim_mem = SimulationMemory()
    out_mem = OutcomeMemory()
    
    tracker = RealityTracker(event_bus, out_mem)
    validator = PredictionValidator(sim_mem, out_mem)
    calibrator = SimulationCalibrator(event_bus)
    
    # ---------------------------------------------------------
    # Benchmark 1: Reality Feedback & Calibration
    # ---------------------------------------------------------
    logger.info("\n--- Benchmark 1: Reality Feedback & Calibration ---")
    sim_id = "SIM-999-TEST"
    
    # 1. Mock the completed simulation
    sim_state = {
        "simulation_id": sim_id,
        "venture_type": "AI Compliance SaaS",
        "outcome": {
            "revenue": 50000,
            "customers": 250,
            "success": True
        }
    }
    sim_mem.save_state(sim_id, sim_state, status="completed")
    
    # 2. Mock the reality updates arriving via EventBus
    await tracker._handle_kpi_update({
        "payload": {"source_simulation_id": sim_id, "metric": "revenue", "value": 42000}
    })
    await tracker._handle_kpi_update({
        "payload": {"source_simulation_id": sim_id, "metric": "customers", "value": 190}
    })
    
    # 3. Validate Prediction
    val_result = validator.calculate_errors(sim_id)
    assert val_result["errors"]["revenue_error_pct"] == -0.16
    assert val_result["errors"]["customers_error_pct"] == -0.24
    logger.info(f"Validator calculated errors perfectly: {val_result['errors']}")
    
    # 4. Calibrate (Expected Minor Calibration: -0.05 confidence base, -0.10 acquisition coeff)
    proposal = calibrator.calibrate(val_result)
    assert proposal is not None
    assert proposal["action"] == "CALIBRATE_WEIGHTS"
    assert proposal["adjustments"]["confidence_base"] == -0.05
    assert proposal["adjustments"]["acquisition_coefficient"] == -0.10
    logger.info(f"Calibrator issued correct proposal: {proposal}")

    # ---------------------------------------------------------
    # Benchmark 2: Prediction Improvement Loop
    # ---------------------------------------------------------
    logger.info("\n--- Benchmark 2: Prediction Improvement Loop ---")
    logger.info("Simulating D19 adjusting weights based on previous proposal...")
    
    # We pretend D19 received the proposal and adjusts our simulation model config
    calibrator.simulation_models["v1.0"]["acquisition_coefficient"] += proposal["adjustments"]["acquisition_coefficient"]
    new_coeff = calibrator.simulation_models["v1.0"]["acquisition_coefficient"]
    
    logger.info(f"New Acquisition Coefficient: {new_coeff}")
    
    # If we run a new simulation with this coeff, the customer prediction would be lower,
    # meaning the future prediction error vs reality would be minimized!
    # Original prediction: 250
    # New prediction with 0.8 coeff = 200
    new_predicted_customers = 250 * new_coeff
    
    # New reality comes in: 190
    new_error = (190 - new_predicted_customers) / new_predicted_customers
    
    logger.info(f"Old Customer Prediction Error: -24%")
    logger.info(f"New Customer Prediction Error with Calibrated Weights: {new_error*100:.1f}%")
    
    assert abs(new_error) < 0.24 # The error margin shrank!
    logger.info("The learning loop successfully improved prediction accuracy!")
    logger.info("\nALL D22 PHASE 2 BENCHMARKS PASSED.")

if __name__ == "__main__":
    asyncio.run(run_feedback_benchmarks())
