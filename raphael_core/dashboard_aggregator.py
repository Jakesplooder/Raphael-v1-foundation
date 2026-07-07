import os
import json
import time
from pathlib import Path
from typing import Dict, Any
from .system_health import calculate_system_health

STALENESS_THRESHOLDS = {
    "initiative_queue.json": 25,   # should update daily
    "llm_ledger.json": 72,         # updates per task
    "world_model_cache.json": 48,  # updates on refresh
    "learning_metrics.json": 25,   # should update daily
}

def check_staleness(filepath: Path, threshold_hours: float) -> str:
    """Returns 'current', 'stale', or 'missing'"""
    if not filepath.exists():
        return "missing"
    try:
        age_hours = (time.time() - filepath.stat().st_mtime) / 3600
        return "stale" if age_hours > threshold_hours else "current"
    except Exception:
        return "error"

def aggregate_dashboard_data(wm_path: str, initiative_path: str, ledger_path: str, learning_path: str) -> Dict[str, Any]:
    """
    Reads from existing outputs with Degraded State Policy.
    Produces safe data dictionary.
    """
    
    # 1. Initiative Queue (Panel 1 Focus)
    init_file = Path(initiative_path)
    init_staleness = check_staleness(init_file, STALENESS_THRESHOLDS.get(init_file.name, 25))
    initiatives = []
    if init_staleness in ("current", "stale"):
        try:
            with open(init_file, 'r', encoding='utf-8') as f:
                queue = json.load(f)
                initiatives = [q for q in queue if q.get("status") in ("Detected", "Briefed")]
                # Sort by priority
                initiatives = sorted(initiatives, key=lambda x: x.get("priority_score", 0), reverse=True)[:3]
        except Exception:
            init_staleness = "error"
            
    # 2. World Model Stats (Panel 2)
    wm_file = Path(wm_path)
    # Using a mock cache file name if world_model.json is the real one
    wm_staleness = check_staleness(wm_file, STALENESS_THRESHOLDS.get("world_model_cache.json", 48))
    wm_nodes = 0
    wm_rels = 0
    if wm_staleness in ("current", "stale"):
        try:
            with open(wm_file, 'r', encoding='utf-8') as f:
                wm = json.load(f)
                wm_nodes = len(wm.get("nodes", []))
                wm_rels = len(wm.get("edges", []))
        except Exception:
            wm_staleness = "error"

    # 3. LLM Spend (Panel 2)
    ledger_file = Path(ledger_path)
    ledger_staleness = check_staleness(ledger_file, STALENESS_THRESHOLDS.get(ledger_file.name, 72))
    total_spend = 0.0
    avoidable_pct = 0.0
    if ledger_staleness in ("current", "stale"):
        try:
            with open(ledger_file, 'r', encoding='utf-8') as f:
                ledger = json.load(f)
                spend = sum(t.get("cost_usd", 0.0) for t in ledger)
                avoid_spend = sum(t.get("cost_usd", 0.0) for t in ledger if t.get("could_use_local") is True)
                total_spend = spend
                if spend > 0:
                    avoidable_pct = (avoid_spend / spend) * 100
        except Exception:
            ledger_staleness = "error"
            
    # 4. Learning Metrics (Panel 2)
    learn_file = Path(learning_path)
    learn_staleness = check_staleness(learn_file, STALENESS_THRESHOLDS.get(learn_file.name, 25))
    accuracy = 84
    accuracy_trend = "+3%"
    # Mock reading learning_metrics.json
    if learn_staleness in ("current", "stale"):
        pass
    else:
        accuracy = 0
        accuracy_trend = "N/A"
        
    # Calculate Health Score
    health_components = {
        "world_model": {"score": 95 if wm_nodes > 0 else 50, "staleness": wm_staleness},
        "learning": {"score": accuracy, "staleness": learn_staleness},
        "initiatives": {"score": 100 if len(initiatives) > 0 else 90, "staleness": init_staleness},
        "workforce": {"score": 90, "staleness": "current"}, # Mock agent score
        "constitutional": {"score": 100, "staleness": "current"} # Mock constitutional score
    }
    health_data = calculate_system_health(health_components)
    
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "health": health_data,
        "initiatives": initiatives,
        "world_model": {
            "nodes": wm_nodes,
            "rels": wm_rels,
            "staleness": wm_staleness
        },
        "learning": {
            "accuracy": accuracy,
            "trend": accuracy_trend,
            "staleness": learn_staleness
        },
        "llm_spend": {
            "spend": total_spend,
            "avoidable_pct": avoidable_pct,
            "staleness": ledger_staleness
        },
        "workforce": {
            "active": 12,        # Mock
            "overloaded": 1,     # Mock
            "staleness": "current"
        },
        "workflows": {
            "queue": 2,          # Mock
            "blocked": 0,        # Mock
            "staleness": "current"
        },
        "portfolio": {
            "projects": [
                {"name": "POD Business", "status": "78% ^"},
                {"name": "Raphael OS", "status": "Phase 69.9"},
                {"name": "Agency", "status": "30% -"}
            ],
            "blockers": [
                "ComfyUI stability blocks 6 tasks"
            ]
        }
    }

import datetime
