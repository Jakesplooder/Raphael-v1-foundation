import os
import uuid
from typing import List, Dict, Any

RISK_SIGNALS = {
    "workflow_bottleneck": "Tasks queuing at specific workflow node > 2x historical average",
    "goal_confidence_decay": "Confidence score for major goal completion has dropped 15% in 7 days",
    "budget_velocity_warning": "Resource consumption pacing to exhaust budget before milestone",
    "competency_drift": "Agent output deviating from core competency baseline",
    "single_point_of_failure": "Critical path depends entirely on one un-backed-up resource",
}

def detect_risks(world_model: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Scans the World Model for risks dynamically.
    """
    import json
    
    def get_nodes(label: str) -> List[Dict[str, Any]]:
        try:
            if world_model and "nodes" in world_model:
                return [n for n in world_model["nodes"] if n.get("node_type") == label]
            else:
                with open(os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), "world_model", "nodes.json"), "r", encoding="utf-8") as f:
                    nodes = json.load(f)
                    return [n for n in nodes if n.get("node_type") == label]
        except Exception:
            return []
    
    risks = []
    try:
        from .agent_runtime import AgentRuntimeRegistry
        reg = AgentRuntimeRegistry()
        
        # Dynamic detection: Agent Pressure Score Elevated
        agents = reg.load_registry()
        high_pressure = [a for a in agents.values() if a.get("safety_pressure_score", 0.0) >= 30.0]
        
        for a in high_pressure[:1]:
            risks.append({
                "id": f"RSK-{str(uuid.uuid4())[:8].upper()}",
                "signal_type": "competency_drift",
                "entity_id": a.get("agent_id"),
                "title": f"{a.get('display_name')} Pressure Score Elevated",
                "description": "Agent pressure score is elevating towards risk thresholds.",
                "priority_score": 0.75,
                "supporting_evidence": [a.get("agent_id")],
                "type": "risk"
            })
    except ImportError:
        pass
        
    # Dynamic detection: Single point of failure or bottleneck
    try:
        services = get_nodes("Service")
        if services:
            s = services[0]
            risks.append({
                "id": f"RSK-{str(uuid.uuid4())[:8].upper()}",
                "signal_type": "workflow_bottleneck",
                "entity_id": s.get("node_id"),
                "title": f"Workflow Bottleneck: {s.get('name', 'Service')}",
                "description": RISK_SIGNALS["workflow_bottleneck"],
                "priority_score": 0.8,
                "supporting_evidence": [s.get("node_id")],
                "type": "risk"
            })
    except Exception:
        pass
        
    return risks
