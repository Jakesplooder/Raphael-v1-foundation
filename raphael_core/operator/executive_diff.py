from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from .executive_state import ExecutiveSnapshot

class ExecutiveDiff(BaseModel):
    """
    Represents the delta between two ExecutiveSnapshots.
    Useful for answering 'What changed?' and triggering proactive alerts.
    """
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    new_events: List[Dict[str, Any]] = Field(default_factory=list)
    completed_tasks: List[Dict[str, Any]] = Field(default_factory=list)
    new_workflows: List[Dict[str, Any]] = Field(default_factory=list)
    
    initiative_changes: List[str] = Field(default_factory=list)
    risk_changes: List[str] = Field(default_factory=list)
    
    health_delta: float = 0.0
    
    # Just a general store for other changes
    other_changes: Dict[str, Any] = Field(default_factory=dict)


def generate_snapshot_diff(old_snap: Optional[ExecutiveSnapshot], new_snap: ExecutiveSnapshot) -> ExecutiveDiff:
    """
    Compares two snapshots and generates a structured diff.
    """
    if not old_snap:
        # If there is no previous snapshot, everything is 'new' conceptually, 
        # but usually we just return an empty diff or a baseline diff.
        return ExecutiveDiff()
        
    diff = ExecutiveDiff()
    
    # Compare Events
    old_events = old_snap.state.events.get("events", {}).get("recent", [])
    new_events = new_snap.state.events.get("events", {}).get("recent", [])
    
    old_event_ids = {e.get("id") for e in old_events if e.get("id")}
    for e in new_events:
        if e.get("id") and e.get("id") not in old_event_ids:
            diff.new_events.append(e)

    # Compare Tasks (Missions)
    old_pending = {t.get("mission_id") for t in old_snap.state.executions.get("tasks", {}).get("pending_approval", [])}
    new_pending = {t.get("mission_id") for t in new_snap.state.executions.get("tasks", {}).get("pending_approval", [])}
    
    old_approved = {t.get("mission_id") for t in old_snap.state.executions.get("tasks", {}).get("approved", [])}
    new_approved = {t.get("mission_id") for t in new_snap.state.executions.get("tasks", {}).get("approved", [])}
    
    # If it was pending but now it's approved/rejected
    for mission_id in (old_pending - new_pending):
        if mission_id in new_approved:
            diff.completed_tasks.append({"mission_id": mission_id, "status": "APPROVED"})
        else:
            # might be rejected
            diff.completed_tasks.append({"mission_id": mission_id, "status": "REJECTED_OR_UNKNOWN"})

    # Compare Workflows
    old_running = {w.get("execution_id") for w in old_snap.state.executions.get("workflows", {}).get("running", [])}
    new_running = {w.get("execution_id") for w in new_snap.state.executions.get("workflows", {}).get("running", [])}
    
    for wid in (new_running - old_running):
        # Find the actual workflow data
        for w in new_snap.state.executions.get("workflows", {}).get("running", []):
            if w.get("execution_id") == wid:
                diff.new_workflows.append(w)
                break
                
    return diff
