import os
import json
import time
from pathlib import Path
from raphael_core.dashboard_aggregator import aggregate_dashboard_data, check_staleness, STALENESS_THRESHOLDS
from raphael_core.system_health import calculate_system_health, apply_staleness_penalty

def test_health_score_calculation():
    # Test penalty application
    assert apply_staleness_penalty(100, "current") == 100
    assert apply_staleness_penalty(100, "stale") == 85
    assert apply_staleness_penalty(100, "missing") == 50
    assert apply_staleness_penalty(100, "error") == 50
    
    # Test calculation
    components = {
        "world_model": {"score": 100, "staleness": "current"},
        "learning": {"score": 100, "staleness": "stale"}, # 85
        "initiatives": {"score": 100, "staleness": "missing"}, # 50
        "workforce": {"score": 100, "staleness": "current"},
        "constitutional": {"score": 100, "staleness": "current"}
    }
    
    health = calculate_system_health(components)
    # (100*.30) + (85*.25) + (50*.20) + (100*.15) + (100*.10)
    # 30 + 21.25 + 10 + 15 + 10 = 86.25
    assert health["overall"] == 86.2

def test_dashboard_aggregator_missing_files():
    # Passing paths that don't exist
    data = aggregate_dashboard_data("fake1.json", "fake2.json", "fake3.json", "fake4.json")
    
    # Data should still return gracefully
    assert data["world_model"]["staleness"] == "missing"
    assert data["learning"]["staleness"] == "missing"
    assert data["llm_spend"]["staleness"] == "missing"
    assert len(data["initiatives"]) == 0
    # Health should be heavily penalized
    assert isinstance(data["health"]["overall"], float)

def test_dashboard_staleness():
    test_file = Path("test_stale.json")
    with open(test_file, 'w') as f:
        f.write("{}")
    
    # Manually set mtime to 30 hours ago
    past_time = time.time() - (30 * 3600)
    os.utime(test_file, (past_time, past_time))
    
    # Initiative queue threshold is 25 hours. At 30 hours it should be stale.
    STALENESS_THRESHOLDS["test_stale.json"] = 25
    staleness = check_staleness(test_file, 25)
    
    assert staleness == "stale"
    
    # Cleanup
    if test_file.exists():
        os.remove(test_file)
