import json
import os
from typing import Dict, Any
from .reasoning_engine import engine as reasoning_engine
from .prediction_evaluator import PREDICTIONS_DIR, EVALUATIONS_DIR
from .pattern_evolution import process_reflection
from .llm.calibration import calibrate_provider

def generate_reflection(prediction_id: str) -> Dict[str, Any]:
    """
    Phase 69.5: Executive Reflection Engine
    Analyzes why a prediction failed and recommends adjustments.
    """
    pred_path = os.path.join(PREDICTIONS_DIR, f"{prediction_id}.json")
    eval_path = os.path.join(EVALUATIONS_DIR, f"EVAL-{prediction_id}.json")
    
    if not os.path.exists(pred_path) or not os.path.exists(eval_path):
        raise ValueError("Both Prediction and Evaluation must exist to reflect.")
        
    with open(pred_path, 'r') as f:
        prediction = json.load(f)
    with open(eval_path, 'r') as f:
        evaluation = json.load(f)
        
    accuracy = evaluation.get("accuracy", {}).get("overall", 100)
    
    # If accuracy is > 90%, it's a success reflection
    is_success = accuracy >= 90
    
    system_prompt = (
        "You are Raphael's Executive Reflection Engine. Analyze the variance between the "
        "original prediction and the actual outcome. Do not hallucinate external events. "
        "Identify missing evidence, recommend weighting adjustments, and state confidence changes."
    )
    
    context = json.dumps({
        "original_reasoning": prediction.get("llm_reasoning"),
        "predicted_score": prediction.get("prediction_score"),
        "actual_accuracy": accuracy,
        "metrics": evaluation.get("accuracy")
    }, indent=2)
    
    task = "Write an Executive Reflection detailing missing evidence and recommended adjustments."
    
    result = reasoning_engine.reason(
        mode="single",
        system_prompt=system_prompt,
        context=context,
        task=task,
        budget_mode="best",
        capability="reasoning"
    )
    
    reflection = {
        "reflection_id": f"REF-{prediction_id}",
        "prediction_id": prediction_id,
        "is_success": is_success,
        "executive_review": result["response"],
        "recommended_confidence_adjustment": -0.05 if not is_success else 0.02
    }
    
    # Save Reflection alongside Evaluation
    eval_dir = os.path.dirname(eval_path)
    with open(os.path.join(eval_dir, f"{reflection['reflection_id']}.json"), 'w') as f:
        json.dump(reflection, f, indent=2)
        
    # Trigger Provider Calibration (Find which provider made the prediction)
    trace = prediction.get("reasoning_trace", {})
    nodes = trace.get("nodes", [])
    if nodes:
        primary_provider = nodes[0].get("provider", "ollama")
        calibrate_provider(primary_provider, "prediction", is_success)
        
    # Trigger Pattern Evolution based on this reflection
    process_reflection(reflection, prediction)
    
    return reflection
