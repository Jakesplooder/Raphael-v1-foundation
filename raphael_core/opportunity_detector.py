import uuid
from typing import List, Dict, Any
import json
import os

OPPORTUNITY_SIGNALS = {
    "stalled_goal_with_available_agent": "Goal hasn't advanced in 14 days, capable agent unassigned",
    "pattern_match_unstarted": "Strong pattern exists for action type, no initiative started",
    "resource_underutilized": "High-capability resource idle for 7+ days",
    "hypothesis_validated": "Active hypothesis reached confidence > 0.75, no follow-up action",
    "external_trend_alignment": "Research agent found trend matching active business goal",
}

def detect_opportunities(world_model: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Scans the World Model for opportunities dynamically.
    """
    from .agent_workload_balancer import analyze_workloads
    from .llm_cost_optimizer import identify_cost_opportunities
    from .portfolio_optimizer import optimize_portfolio
    
    def get_nodes(label: str) -> List[Dict[str, Any]]:
        try:
            if world_model and "nodes" in world_model:
                return [n for n in world_model["nodes"] if n.get("node_type") == label]
            else:
                with open(os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), "world_model", "nodes.json"), "r", encoding="utf-8") as f:
                    nodes = json.load(f)
                    return [n for n in nodes if n.get("node_type") == label]
        except Exception:
            return []
            
    opportunities = []
    
    opportunities.extend(analyze_workloads())
    opportunities.extend(identify_cost_opportunities())
    opportunities.extend(optimize_portfolio())
    
    try:
        from .workforce_health import scan_workforce_health
        from .agent_runtime import AgentRuntimeRegistry, AgentLifecycleManager
        reg = AgentRuntimeRegistry()
        lif = AgentLifecycleManager(reg)
        opportunities.extend(scan_workforce_health(reg, lif))
    except ImportError:
        pass
    
    # Dynamic detection: Stalled Goal
    # Find any 'Goal' nodes in the world model that haven't been updated recently.
    try:
        goals = get_nodes("Goal")
        if not goals:
            # Fallback if no specific Goals found, check generic projects
            goals = get_nodes("Project")
            
        if goals:
            for g in goals[:1]: # Just flag the first one for the briefing
                opportunities.append({
                    "id": f"OPP-{str(uuid.uuid4())[:8].upper()}",
                    "signal_type": "stalled_goal_with_available_agent",
                    "entity_id": g.get("node_id", "UNKNOWN-GOAL"),
                    "title": f"Assign Agent to {g.get('name', 'Goal')}",
                    "description": OPPORTUNITY_SIGNALS["stalled_goal_with_available_agent"],
                    "priority_score": 0.8,
                    "supporting_evidence": [g.get("node_id")],
                    "type": "opportunity"
                })
    except Exception as e:
        pass
        
    # Dynamic detection: Resource Underutilized
    # Find agents in runtime registry with 0 active tasks
    try:
        agents = reg.load_registry()
        underutilized = [a for a in agents.values() if a.get("active_task_count", 0) == 0 and a.get("current_state") == "active"]
        
        for a in underutilized[:1]: # Just flag the first one
            opportunities.append({
                "id": f"OPP-{str(uuid.uuid4())[:8].upper()}",
                "signal_type": "resource_underutilized",
                "entity_id": a.get("agent_id"),
                "title": f"Assign {a.get('display_name')} to New Task",
                "description": OPPORTUNITY_SIGNALS["resource_underutilized"],
                "priority_score": 0.6,
                "supporting_evidence": [a.get("agent_id")],
                "type": "opportunity"
            })
    except Exception as e:
        pass
    
    return opportunities
