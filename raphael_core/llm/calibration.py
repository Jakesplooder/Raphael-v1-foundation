import json
import os
from typing import Dict, Any
from .capability_profiles import PROFILES, CapabilityProfile

CALIBRATION_FILE = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model\provider_calibration.json")

def get_calibrated_profiles() -> Dict[str, CapabilityProfile]:
    """
    Returns the capability profiles, adjusted by historical calibration.
    """
    profiles = dict(PROFILES)
    if os.path.exists(CALIBRATION_FILE):
        with open(CALIBRATION_FILE, 'r') as f:
            calibrations = json.load(f)
            for provider, calib in calibrations.items():
                if provider in profiles:
                    # Apply adjustments
                    prof = profiles[provider]
                    prof.reasoning = max(1, min(10, prof.reasoning + calib.get("reasoning_adj", 0)))
                    prof.prediction = max(1, min(10, prof.prediction + calib.get("prediction_adj", 0)))
    return profiles

def calibrate_provider(provider_name: str, task_type: str, success: bool):
    """
    Phase 69.5: Provider Calibration
    Adjusts a provider's score dynamically based on outcome.
    """
    calibrations = {}
    if os.path.exists(CALIBRATION_FILE):
        with open(CALIBRATION_FILE, 'r') as f:
            calibrations = json.load(f)
            
    if provider_name not in calibrations:
        calibrations[provider_name] = {"reasoning_adj": 0, "prediction_adj": 0, "total_tasks": 0, "successes": 0}
        
    calib = calibrations[provider_name]
    calib["total_tasks"] += 1
    if success:
        calib["successes"] += 1
        adj_key = f"{task_type}_adj"
        if adj_key in calib:
            calib[adj_key] = min(3, calib[adj_key] + 1)
    else:
        adj_key = f"{task_type}_adj"
        if adj_key in calib:
            calib[adj_key] = max(-3, calib[adj_key] - 1)
            
    with open(CALIBRATION_FILE, 'w') as f:
        json.dump(calibrations, f, indent=2)
