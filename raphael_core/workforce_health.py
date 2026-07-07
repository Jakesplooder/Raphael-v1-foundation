from typing import List, Dict, Any
from .agent_runtime import AgentRuntimeRegistry, AgentLifecycleManager

def scan_workforce_health(registry: AgentRuntimeRegistry, lifecycle: AgentLifecycleManager) -> List[Dict[str, Any]]:
    """
    Scans the runtime registry for workforce health signals and surfaces them.
    Signals that require authority transition (e.g. pressure >= 60 triggers Under Review recommendation)
    are returned as initiative queue items.
    """
    data = registry.load_registry()
    signals = []
    
    for agent_id, agent in data.items():
        state = agent.get("current_state")
        pressure = agent.get("safety_pressure_score", 0.0)
        
        # 1. Under Review Recommendation (Pressure >= 60)
        if pressure >= 60 and state == "active":
            # Lifecycle manager recommends Under Review transition internally.
            lifecycle.request_transition(
                agent_id, 
                "under_review", 
                f"Safety pressure score critical ({pressure})", 
                []
            )
            signals.append({
                "type": "workforce_lifecycle",
                "signal": "agent_under_review",
                "entity": agent_id,
                "current_state": "active",
                "recommended_transition": "under_review",
                "reason": f"Safety pressure score critical ({pressure})",
                "evidence": [],
                "alternative_interpretation": "Performance issues may reflect task complexity spike rather than agent capability decline.",
                "authority_required": False,
                "priority_score": 0.89,
                "status": "Detected"
            })
                
        # 2. Overload Detection
        # If consecutive_days_overloaded >= 3
        if agent.get("consecutive_days_overloaded", 0) >= 3 and state == "active":
            lifecycle.request_transition(agent_id, "overloaded", "Sustained high task backlog", [])
            
        # 3. Recovering too long
        # Mock logic
        pass

    return signals
