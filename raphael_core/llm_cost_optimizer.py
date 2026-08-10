import os
import json
from typing import List, Dict, Any

LEDGER_FILE = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), r"\world_model\llm_ledger.json")

def load_ledger() -> List[Dict[str, Any]]:
    if not os.path.exists(LEDGER_FILE):
        return []
    with open(LEDGER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_ledger(ledger: List[Dict[str, Any]]):
    with open(LEDGER_FILE, 'w', encoding='utf-8') as f:
        json.dump(ledger, f, indent=2)

def evaluate_local_viability():
    """
    Evaluates whether tasks completed by premium models could have
    been handled by local models at comparable accuracy.
    Updates the 'could_use_local' field.
    """
    ledger = load_ledger()
    
    # Establish baseline local accuracy per task_type
    local_accuracy = {}
    local_tasks = [t for t in ledger if t["provider"] == "ollama"]
    for t in local_tasks:
        ttype = t["task_type"]
        if ttype not in local_accuracy:
            local_accuracy[ttype] = []
        local_accuracy[ttype].append(t["accuracy_score"])
        
    avg_local = {k: sum(v)/len(v) for k, v in local_accuracy.items()}
    
    updated = False
    for t in ledger:
        if t["provider"] != "ollama" and t["could_use_local"] is None:
            ttype = t["task_type"]
            # If we have local data for this task type, compare
            if ttype in avg_local:
                # If local accuracy is within 5% of this task's accuracy
                if avg_local[ttype] >= t["accuracy_score"] - 0.05:
                    t["could_use_local"] = True
                else:
                    t["could_use_local"] = False
                updated = True
                
    if updated:
        save_ledger(ledger)

def identify_cost_opportunities() -> List[Dict[str, Any]]:
    """
    Identifies if a specific task type is routinely over-provisioned.
    """
    evaluate_local_viability()
    ledger = load_ledger()
    
    avoidable_cost = 0.0
    avoidable_count = 0
    overprovisioned_types = set()
    
    for t in ledger:
        if t["could_use_local"] is True and t["provider"] != "ollama":
            avoidable_cost += t.get("cost_usd", 0.0)
            avoidable_count += 1
            overprovisioned_types.add(t["task_type"])
            
    opportunities = []
    if avoidable_count >= 5 or avoidable_cost > 1.0: # Arbitrary threshold for acute notification
        opportunities.append({
            "id": "OPP-LLM-COST",
            "signal_type": "llm_cost_spike",
            "entity_id": "ROUTER",
            "title": "LLM Cost Optimization Available",
            "description": f"Identified {avoidable_count} tasks costing ${avoidable_cost:.2f} that could use local inference.",
            "priority_score": 0.70,
            "supporting_evidence": [f"LEDGER-{t}" for t in overprovisioned_types],
            "type": "opportunity"
        })
        
    return opportunities

def get_weekly_cost_trends() -> Dict[str, Any]:
    """
    Aggregates LLM usage for the weekly summary.
    """
    evaluate_local_viability()
    ledger = load_ledger()
    
    total_spend = sum(t.get("cost_usd", 0.0) for t in ledger)
    avoidable_spend = sum(t.get("cost_usd", 0.0) for t in ledger if t["could_use_local"] is True)
    
    avoidable_pct = (avoidable_spend / total_spend * 100) if total_spend > 0 else 0
    
    return {
        "total_spend": total_spend,
        "avoidable_spend": avoidable_spend,
        "avoidable_pct": round(avoidable_pct, 1),
        "total_tasks": len(ledger)
    }
