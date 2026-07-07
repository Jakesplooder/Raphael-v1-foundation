from typing import List, Dict, Any

def forecast_confidence(
    blocking_dependencies: int,
    resolved_dependencies: int,
    pattern_support: float,
    agent_availability: float,
    historical_accuracy: float,
) -> float:
    """
    Confidence formula for capacity forecasts.
    All inputs normalized to 0-1 range.
    """
    dependency_clarity = resolved_dependencies / max(1, resolved_dependencies + blocking_dependencies)
    
    base = (
        dependency_clarity    * 0.40 +  # Most important — unresolved deps kill forecasts
        pattern_support       * 0.25 +  # Historical patterns for similar projects
        agent_availability    * 0.20 +  # Agents assigned and available
        historical_accuracy   * 0.15    # How accurate past forecasts were
    )
    
    # Hard ceiling: never above 0.85 — forecasts are inherently uncertain
    # Hard floor: never below 0.15 — even uncertain forecasts have some signal
    return round(max(0.15, min(0.85, base)), 2)

def generate_capacity_forecast(project_id: str, world_model: Dict[str, Any], adj: dict) -> str:
    """
    Generates the strict CAPACITY FORECAST text format defined in ADR 004.
    """
    from .dependency_analyzer import detect_cycles, find_critical_path, ConstitutionalViolationError
    
    try:
        cycles = detect_cycles(project_id, adj)
        if cycles:
            cycle_str = " -> ".join(cycles[0])
            return (
                f"CAPACITY FORECAST — BLOCKED\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Project: {project_id}\n"
                f"Status: Cannot forecast — circular dependency detected\n\n"
                f"Cycle detected:\n"
                f"  {cycle_str}\n\n"
                f"Recommendation: Review and resolve circular dependency before forecasting.\n"
                f"World Model Health: Flag created for Aaron review.\n"
            )
            
        cp = find_critical_path(project_id, world_model, adj)
        
        # Mock data for demonstration
        velocity = 3
        remaining_tasks = 24
        est_completion = 8
        blocking_deps = 2
        resolved_deps = 8
        
        conf = forecast_confidence(
            blocking_dependencies=blocking_deps,
            resolved_dependencies=resolved_deps,
            pattern_support=0.8,
            agent_availability=0.6,
            historical_accuracy=0.7
        )
        
        # Determine confidence reasoning string based on score
        reasoning = "low — blocking dependencies unresolved"
        if conf > 0.5:
            reasoning = "moderate — some historical patterns match"
        if conf > 0.7:
            reasoning = "high — strong clarity and agent availability"
            
        return (
            f"CAPACITY FORECAST\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"Project: {project_id}\n"
            f"Current velocity: {velocity} tasks/week\n"
            f"Remaining tasks: {remaining_tasks}\n"
            f"Estimated completion: {est_completion} weeks\n\n"
            f"Blocking dependencies:\n"
            f"  - {cp['bottleneck_node']} (BLOCKS 6 tasks)\n"
            f"  - Commerce Agent availability (ASSIGNED to 4 other tasks)\n\n"
            f"Risk-adjusted estimate: {est_completion + 3}-{est_completion + 6} weeks\n"
            f"Confidence: {conf} ({reasoning})\n"
        )
    except Exception as e:
        return f"Error generating forecast: {str(e)}"
