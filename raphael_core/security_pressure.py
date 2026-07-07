from typing import Dict
from .near_miss_logger import get_recent_near_misses

def calculate_safety_pressure(agent_id: str) -> Dict[str, Any]:
    """
    Calculates the Safety Pressure Score for a given agent.
    Score is 0.0 (safe) to 1.0 (maximum pressure).
    High pressure blocks the agent from high-risk assignments.
    """
    # Base pressure from near-misses in last 72 hours
    misses = get_recent_near_misses(agent_id, hours=72)
    
    # Weight misses by recency and count
    pressure = len(misses) * 0.15
    
    # Clamp to [0.0, 1.0]
    pressure = max(0.0, min(1.0, pressure))
    
    return {
        "agent_id": agent_id,
        "pressure_score": pressure,
        "near_miss_count_72h": len(misses),
        "status": "ELEVATED" if pressure >= 0.6 else "NORMAL"
    }

def get_all_pressure_scores(agent_ids: list[str]) -> Dict[str, dict]:
    """Calculate pressure for multiple agents."""
    return {a_id: calculate_safety_pressure(a_id) for a_id in agent_ids}
