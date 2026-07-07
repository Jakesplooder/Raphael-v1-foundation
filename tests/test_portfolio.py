from raphael_core.dependency_analyzer import detect_cycles, find_critical_path, ConstitutionalViolationError
from raphael_core.capacity_forecaster import generate_capacity_forecast, forecast_confidence
from raphael_core.portfolio_optimizer import pareto_filter_recommendations

def test_cycle_detection_guard():
    """
    Inject a 3-node circular dependency (A -> B -> C -> A)
    Verify capacity_forecaster surfaces the cycle as a health issue
    Verify it does not infinite loop or produce a forecast
    """
    # Create the cycle
    adj = {
        "outbound": {
            "PROJ-A": {"DEPENDS_ON": [{"to_node": "PROJ-B"}]},
            "PROJ-B": {"DEPENDS_ON": [{"to_node": "PROJ-C"}]},
            "PROJ-C": {"DEPENDS_ON": [{"to_node": "PROJ-A"}]}
        }
    }
    
    # Verify detect_cycles directly
    cycles = detect_cycles("PROJ-A", adj)
    assert len(cycles) > 0
    assert "PROJ-A" in cycles[0] and "PROJ-B" in cycles[0] and "PROJ-C" in cycles[0]
    
    # Verify find_critical_path throws ConstitutionalViolationError
    try:
        find_critical_path("PROJ-A", {}, adj)
        assert False, "Should have thrown ConstitutionalViolationError"
    except ConstitutionalViolationError as e:
        assert "Circular dependency detected" in str(e)
    
    # Verify capacity forecaster catches it and outputs the right format
    forecast = generate_capacity_forecast("PROJ-A", {}, adj)
    assert "CAPACITY FORECAST \u2014 BLOCKED" in forecast or "CAPACITY FORECAST — BLOCKED" in forecast
    assert "Cannot forecast \u2014 circular dependency detected" in forecast or "Cannot forecast — circular dependency detected" in forecast
    assert "World Model Health: Flag created for Aaron review" in forecast

def test_critical_path_no_cycle():
    adj = {
        "outbound": {
            "PROJ-A": {"DEPENDS_ON": [{"to_node": "PROJ-B"}]},
            "PROJ-B": {"DEPENDS_ON": [{"to_node": "PROJ-C"}]}
        }
    }
    cp = find_critical_path("PROJ-A", {}, adj)
    assert "PROJ-B" in cp["path_nodes"]

def test_forecast_confidence_bounds():
    # Test ceiling 0.85
    high_conf = forecast_confidence(0, 10, 1.0, 1.0, 1.0)
    assert high_conf <= 0.85
    
    # Test floor 0.15
    low_conf = forecast_confidence(10, 0, 0.0, 0.0, 0.0)
    assert low_conf >= 0.15

def test_pareto_filter():
    recs = [
        {"id": "1", "estimated_time_savings_weeks": 3.0},
        {"id": "2", "estimated_time_savings_weeks": 0.5},
        {"id": "3", "estimated_time_savings_weeks": 2.0},
    ]
    filtered = pareto_filter_recommendations(recs, min_improvement_weeks=1.5)
    
    assert len(filtered) == 2
    assert filtered[0]["id"] == "1" # Should be sorted descending
    assert filtered[1]["id"] == "3"
