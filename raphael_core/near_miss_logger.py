import os
import json
from pathlib import Path
from typing import Dict, Any
import time

LOG_FILE = Path(os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model\near_misses.json"))

def log_near_miss(agent_id: str, incident_type: str, details: Dict[str, Any]):
    """
    Logs a near-miss boundary approach that didn't trigger a full violation.
    Used to calculate Safety Pressure.
    """
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    miss = {
        "timestamp": time.time(),
        "agent_id": agent_id,
        "incident_type": incident_type,
        "details": details
    }
    
    misses = []
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                misses = json.load(f)
        except Exception:
            pass
            
    misses.append(miss)
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(misses, f, indent=2)

def get_recent_near_misses(agent_id: str = None, hours: int = 24) -> list:
    """Retrieves near-misses for a given agent in the last X hours."""
    if not LOG_FILE.exists():
        return []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            misses = json.load(f)
    except Exception:
        return []
        
    cutoff = time.time() - (hours * 3600)
    filtered = [m for m in misses if m["timestamp"] > cutoff]
    
    if agent_id:
        filtered = [m for m in filtered if m["agent_id"] == agent_id]
        
    return filtered
