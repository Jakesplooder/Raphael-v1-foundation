from typing import Dict, Any

def apply_staleness_penalty(component_score: float, staleness: str) -> float:
    if staleness == "current":
        return component_score
    if staleness == "stale":
        return component_score * 0.85  # 15% penalty — data exists but aged
    if staleness in ("missing", "error"):
        return component_score * 0.50  # 50% penalty — component unreachable
    return component_score

def calculate_system_health(components: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates components and produces a single weighted health score [0-100].
    Applies staleness penalties to individual components before weighting.
    
    Expected format for components dict:
    {
        "world_model": {"score": 95, "staleness": "current"},
        "learning": {"score": 84, "staleness": "current"},
        "initiatives": {"score": 100, "staleness": "stale"},
        "workforce": {"score": 90, "staleness": "current"},
        "constitutional": {"score": 100, "staleness": "current"}
    }
    """
    
    # Defaults in case components are omitted
    wm = components.get("world_model", {"score": 100, "staleness": "missing"})
    learn = components.get("learning", {"score": 100, "staleness": "missing"})
    init = components.get("initiatives", {"score": 100, "staleness": "missing"})
    wf = components.get("workforce", {"score": 100, "staleness": "missing"})
    const = components.get("constitutional", {"score": 100, "staleness": "missing"})
    
    # Apply penalties
    wm_score = apply_staleness_penalty(wm["score"], wm["staleness"])
    learn_score = apply_staleness_penalty(learn["score"], learn["staleness"])
    init_score = apply_staleness_penalty(init["score"], init["staleness"])
    wf_score = apply_staleness_penalty(wf["score"], wf["staleness"])
    const_score = apply_staleness_penalty(const["score"], const["staleness"])
    
    # Weighted average
    overall = (
        wm_score * 0.30 +
        learn_score * 0.25 +
        init_score * 0.20 +
        wf_score * 0.15 +
        const_score * 0.10
    )
    
    return {
        "overall": round(overall, 1),
        "components": {
            "world_model": {"score": round(wm_score, 1), "staleness": wm["staleness"]},
            "learning": {"score": round(learn_score, 1), "staleness": learn["staleness"]},
            "initiatives": {"score": round(init_score, 1), "staleness": init["staleness"]},
            "workforce": {"score": round(wf_score, 1), "staleness": wf["staleness"]},
            "constitutional": {"score": round(const_score, 1), "staleness": const["staleness"]},
        }
    }
