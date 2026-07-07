from typing import List, Dict, Any

# Mock state simulating tracking history
# In reality, this would be persisted to World Model over time
# We track how many consecutive days an agent was >40% imbalanced from average
_mock_agent_history = {
    "Developer Agent": {"current_tasks": 7, "consecutive_high_days": 4, "pressure_score": 42},
    "Research Agent": {"current_tasks": 1, "consecutive_high_days": 0, "pressure_score": 4},
    "QA Agent": {"current_tasks": 0, "consecutive_high_days": 0, "pressure_score": 1}
}

def analyze_workloads() -> List[Dict[str, Any]]:
    """
    Phase 69.7: Agent Workload Balancer
    Scans agent assignment data and produces load imbalance recommendations.
    Implements 3-day / 40% threshold stability rule to prevent thrashing.
    """
    opportunities = []
    
    # Calculate average
    total_tasks = sum(data["current_tasks"] for data in _mock_agent_history.values())
    avg_tasks = total_tasks / len(_mock_agent_history) if _mock_agent_history else 0
    
    for agent, data in _mock_agent_history.items():
        if data["current_tasks"] > avg_tasks * 1.40: # 40% imbalance
            if data["consecutive_high_days"] > 3:    # 3-day threshold
                opportunities.append({
                    "id": f"OPP-BAL-{agent.split()[0].upper()}",
                    "signal_type": "agent_overload",
                    "entity_id": agent,
                    "title": f"Rebalance Tasks from {agent}",
                    "description": f"Agent is overloaded ({data['current_tasks']} tasks). Recommend moving 2 tasks to underloaded agents.",
                    "priority_score": 0.75,
                    "supporting_evidence": ["PATTERN-112"],
                    "type": "opportunity"
                })
                
    return opportunities

def get_weekly_utilization() -> Dict[str, Any]:
    """
    Weekly summary metrics for Agent Workload.
    """
    total_tasks = sum(data["current_tasks"] for data in _mock_agent_history.values())
    avg_tasks = total_tasks / len(_mock_agent_history) if _mock_agent_history else 0
    return {
        "avg_utilization": round(avg_tasks, 1),
        "trend_vs_last_week": "+12%"
    }
