from typing import List, Dict, Any

def pareto_filter_recommendations(
    recommendations: List[Dict[str, Any]],
    min_improvement_weeks: float = 1.5,
    max_recommendations: int = 3,
) -> List[Dict[str, Any]]:
    """
    Only surface sequencing recommendations where reordering
    saves at least min_improvement_weeks of calendar time.
    
    Trivial optimizations (saving 2 days) create noise.
    Meaningful optimizations (saving 2 weeks) justify attention.
    """
    meaningful = [
        r for r in recommendations
        if r.get("estimated_time_savings_weeks", 0) >= min_improvement_weeks
    ]
    return sorted(
        meaningful,
        key=lambda r: r.get("estimated_time_savings_weeks", 0),
        reverse=True
    )[:max_recommendations]

def optimize_portfolio() -> List[Dict[str, Any]]:
    """
    Phase 69.8: Portfolio Optimizer
    Generates sequencing recommendations.
    """
    raw_recommendations = [
        {
            "id": "OPP-PORT-SEQ1",
            "signal_type": "portfolio_sequencing",
            "entity_id": "Project A",
            "title": "Sequence Project A before Project B",
            "description": "Given current capacity and dependencies, completing Project A before Project B reduces total completion time by 3 weeks because B depends on A's output.",
            "estimated_time_savings_weeks": 3.0,
            "priority_score": 0.85,
            "supporting_evidence": ["GRAPH-PATH-1", "CAPACITY-SIM-1"],
            "type": "opportunity"
        },
        {
            "id": "OPP-PORT-SEQ2",
            "signal_type": "portfolio_sequencing",
            "entity_id": "Project C",
            "title": "Sequence Project C before Project D",
            "description": "Saves 0.5 weeks of time.",
            "estimated_time_savings_weeks": 0.5, # Will be filtered out
            "priority_score": 0.60,
            "supporting_evidence": ["GRAPH-PATH-2"],
            "type": "opportunity"
        }
    ]
    
    return pareto_filter_recommendations(raw_recommendations)
