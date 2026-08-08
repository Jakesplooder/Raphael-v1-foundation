import json
import time
from pathlib import Path
from typing import Dict, Any
from raphael_core.kernel.event_bus import emit

class IncidentManager:
    def __init__(self, incidents_dir=r"C:\RaphaelOS\Incidents"):
        self.incidents_dir = Path(incidents_dir)
        self.incidents_dir.mkdir(parents=True, exist_ok=True)
        
    def handle_failure(self, mission_id: str, error: str, category: str, cost: float):
        # 1. Detect & Classify
        incident_id = f"inc_{int(time.time())}_{mission_id}"
        incident_folder = self.incidents_dir / incident_id
        incident_folder.mkdir(parents=True, exist_ok=True)
        
        # 2. Contain & Recover (Mocking recovery attempt)
        recovery_success = False
        if category == "RESOURCE_FAILURE":
            recovery_success = True
            recovery_action = "Restarted worker, recovered successfully."
        else:
            recovery_action = "Attempted fallback, failed."
            
        status = "RECOVERED" if recovery_success else "CONTAINED"
        
        # 3. Write Artifacts
        incident_data = {
            "incident_id": incident_id,
            "mission_id": mission_id,
            "error": error,
            "category": category,
            "cost_incurred": cost,
            "status": status,
            "timestamp": time.time()
        }
        (incident_folder / "incident.json").write_text(json.dumps(incident_data, indent=2))
        
        timeline = [{"state": "DETECTED"}, {"state": "CLASSIFIED"}, {"state": status}]
        (incident_folder / "timeline.json").write_text(json.dumps(timeline, indent=2))
        
        recovery_data = {"attempt": 1, "action": recovery_action, "success": recovery_success}
        (incident_folder / "recovery_action.json").write_text(json.dumps(recovery_data, indent=2))
        
        # 4. Postmortem (if serious)
        if not recovery_success:
            postmortem = f"""# Incident Postmortem

**Incident ID:** {incident_id}
**Mission:** {mission_id}
**Cause:** {error}
**Category:** {category}
**Impact:** Mission failed, cost incurred: ${cost:.2f}

## Detection
Caught by execution engine during pipeline processing.

## Recovery
{recovery_action}

## Prevention
(Pending analysis - flag for rule engine update)
"""
            (incident_folder / "incident_postmortem.md").write_text(postmortem)
            
            # 5. Notify
            emit("MISSION.FAILURE", "IncidentManager", {
                "mission_id": mission_id,
                "problem": error,
                "recovery": recovery_action,
                "priority": "critical"
            })
            
        return incident_id

incident_manager = IncidentManager()
