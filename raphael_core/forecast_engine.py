import json
import time
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, List
from .reasoning_engine import engine as reasoning_engine
from . import world_model
from . import pattern_engine

PREDICTIONS_DIR = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model\predictions")
os.makedirs(PREDICTIONS_DIR, exist_ok=True)
TRACKING_FILE = os.path.join(PREDICTIONS_DIR, "prediction_accuracy.json")

def generate_forecast(plan: Dict[str, Any], mode: str = "consensus") -> Dict[str, Any]:
    """
    Phase 69.4: Forecast Engine
    Generates a deterministic prediction incorporating semantic reasoning.
    Rule: LLMs reason. Raphael decides.
    """
    start_time = time.time()
    
    # 1. Deterministic Evidence Retrieval
    plan_desc = plan.get("name", "Unknown Plan")
    patterns = pattern_engine.pattern_search(plan_desc)[:3]
    lessons = []
    events = []
    for p in patterns:
        if p.get("supporting_lessons"):
            lessons.extend(p["supporting_lessons"])
        if p.get("supporting_events"):
            events.extend(p["supporting_events"])
            
    # Calculate deterministic similarity (simplified for scaffolding)
    hist_similarity = 0.85 if len(patterns) > 0 else 0.35
    
    # Prepare context for LLM
    context = f"""
Plan Name: {plan_desc}
Plan Steps: {json.dumps(plan.get("steps", []))}
Historical Similarity: {hist_similarity}
Patterns Found: {len(patterns)}
Lessons Found: {len(lessons)}
Events Found: {len(events)}
    """
    
    # System Prompt Hash & Versioning
    system_prompt = "You are Raphael's Predictive Intelligence Engine. Evaluate the provided strategic plan."
    prompt_hash = hashlib.md5(system_prompt.encode()).hexdigest()[:8]
    prompt_version = "1.0"
    
    # 2. Semantic Reasoning via Reasoning Engine
    task = "Forecast the expected timeline, key risks, and probability of success based on evidence provided."
    reasoning_result = reasoning_engine.reason(
        mode=mode,
        system_prompt=system_prompt,
        context=context,
        task=task,
        budget_mode="balanced",
        capability="prediction"
    )
    
    # 3. Deterministic Confidence & Scoring Formulas
    # (Historical * 0.35) + (Pattern * 0.25) + (Lessons * 0.15) + (WorldModel * 0.25)
    score = (hist_similarity * 0.35) + (min(len(patterns)/3, 1.0) * 0.25) + (min(len(lessons)/2, 1.0) * 0.15) + 0.10
    
    prediction_obj = {
        "prediction_id": f"PRED-{int(time.time())}",
        "plan_id": plan.get("plan_id", "UNKNOWN"),
        "prediction_score": round(score, 2),
        "historical_similarity": hist_similarity,
        "patterns_used": len(patterns),
        "lessons_used": len(lessons),
        "llm_reasoning": reasoning_result["response"],
        "reasoning_trace": reasoning_result["trace"],
        "prompt_metadata": {
            "version": prompt_version,
            "hash": prompt_hash,
            "name": "executive_prediction.md"
        },
        "generated_at": datetime.utcnow().isoformat(),
        "status": "forecasted"
    }
    
    # If insufficient evidence, log hypothesis deterministic penalty
    if len(patterns) < 3:
        prediction_obj["hypothesis_triggered"] = True
        prediction_obj["prediction_score"] *= 0.8 # Penalty
        
    # Save Prediction
    with open(os.path.join(PREDICTIONS_DIR, f"{prediction_obj['prediction_id']}.json"), 'w') as f:
        json.dump(prediction_obj, f, indent=2)
        
    # Update accuracy tracker (Phase 69.5 hooks)
    _track_prediction(prediction_obj)
        
    return prediction_obj

def _track_prediction(pred: dict):
    # Just initializes or appends to prediction_accuracy.json
    if not os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'w') as f:
            json.dump([], f)
    with open(TRACKING_FILE, 'r+') as f:
        data = json.load(f)
        data.append({"prediction_id": pred["prediction_id"], "score": pred["prediction_score"], "actual": None})
        f.seek(0)
        json.dump(data, f, indent=2)
