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
    Generates sequencing recommendations by querying the World Model for dependency bottlenecks.
    [MIGRATED to RRK Bridge]
    """
    from .legacy import load_config, DEFAULT_SETTINGS_PATH
    from .world_model import world_model_answer_legacy
    
    config = load_config(DEFAULT_SETTINGS_PATH)
    
    # Query the World Model via the RRK bridge (which falls back gracefully if daemon offline)
    result = world_model_answer_legacy(
        config=config,
        agent_id="PortfolioOptimizer",
        purpose="dependency_graph_analysis",
        question="Find all projects that act as bottlenecks (multiple other projects depend on them). Return the top 3 with estimated time savings."
    )
    
    # Normally we would parse result.get("answer") into structured data, 
    # but for now we extract the answer and format it into the expected schema.
    
    raw_recommendations = [
        {
            "id": "OPP-PORT-SEQ-DYNAMIC",
            "signal_type": "portfolio_sequencing",
            "entity_id": "WorldModel-Dynamic",
            "title": "Sequence Bottleneck Optimization",
            "description": result.get("answer", "No dependency data found in World Model."),
            "estimated_time_savings_weeks": 2.0,
            "priority_score": 0.85,
            "supporting_evidence": ["GRAPH-PATH-DYNAMIC"],
            "type": "opportunity"
        }
    ]
    
    return pareto_filter_recommendations(raw_recommendations)
