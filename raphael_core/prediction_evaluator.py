import json
import os
from datetime import datetime
from typing import Dict, Any

PREDICTIONS_DIR = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model\predictions")
EVALUATIONS_DIR = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model\evaluations")
os.makedirs(EVALUATIONS_DIR, exist_ok=True)
TRACKING_FILE = os.path.join(PREDICTIONS_DIR, "prediction_accuracy.json")

def evaluate_prediction(prediction_id: str, actual_outcome: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase 69.5: Prediction Evaluation Engine
    Compares a forecast against reality.
    """
    pred_path = os.path.join(PREDICTIONS_DIR, f"{prediction_id}.json")
    if not os.path.exists(pred_path):
        raise ValueError(f"Prediction {prediction_id} not found.")
        
    with open(pred_path, 'r', encoding='utf-8') as f:
        prediction = json.load(f)
        
    # In a real system, these would be deep semantic comparisons. 
    # For MVP, we calculate raw numeric distances.
    timeline_acc = max(0, 100 - abs(prediction.get("predicted_timeline_days", 10) - actual_outcome.get("actual_timeline_days", 10)) * 5)
    budget_acc = max(0, 100 - abs(prediction.get("predicted_budget", 100) - actual_outcome.get("actual_budget", 100)))
    risk_acc = 100 if prediction.get("risks_identified", 0) >= actual_outcome.get("risks_materialized", 0) else 50
    
    overall_acc = (timeline_acc + budget_acc + risk_acc) / 3
    
    evaluation = {
        "evaluation_id": f"EVAL-{prediction_id}",
        "prediction_id": prediction_id,
        "plan_id": prediction.get("plan_id"),
        "accuracy": {
            "overall": round(overall_acc, 2),
            "timeline": round(timeline_acc, 2),
            "budget": round(budget_acc, 2),
            "risk": round(risk_acc, 2),
            "confidence_calibration": round(100 - abs(prediction.get("prediction_score", 0.5)*100 - overall_acc), 2)
        },
        "actual_outcome": actual_outcome,
        "evaluated_at": datetime.utcnow().isoformat()
    }
    
    with open(os.path.join(EVALUATIONS_DIR, f"{evaluation['evaluation_id']}.json"), 'w', encoding='utf-8') as f:
        json.dump(evaluation, f, indent=2)
        
    # Update Tracking File
    _update_tracking(prediction_id, overall_acc)
    
    return evaluation

def _update_tracking(prediction_id: str, actual_score: float):
    if not os.path.exists(TRACKING_FILE):
        return
    with open(TRACKING_FILE, 'r+') as f:
        data = json.load(f)
        for item in data:
            if item.get("prediction_id") == prediction_id:
                item["actual"] = actual_score
                break
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
