from raphael_core.red_team_agent import RedTeamAgent
from raphael_core.canary_agent import CanaryAgent, CanarySignal
from raphael_core.near_miss_logger import log_near_miss, get_recent_near_misses
from raphael_core.security_pressure import calculate_safety_pressure
import time
import os

def test_red_team_all_scenarios_pass():
    """
    Runs the 6 regression Red Team scenarios against the current v1.5 architecture.
    All must pass.
    """
    rt = RedTeamAgent()
    results = rt.run_scenarios()
    
    assert len(results) == 6
    for res in results:
        assert res["passed"] is True, f"Red Team Scenario Failed: {res['scenario']} - {res['details']}"

def test_canary_baseline_poison_resistance():
    canary = CanaryAgent()
    
    # 30 day window. 23 days at normal rate (5.0), 7 days at high rate (80.0)
    normal = [{"query_rate": 5.0} for _ in range(23)]
    poison = [{"query_rate": 80.0} for _ in range(7)]
    
    canary.history["TEST_AGENT"] = normal + poison
    
    # Check baseline query rate. It should drop the top 3 and bottom 3 (10% of 30)
    # The remaining sorted list has 20 5.0s and 4 80.0s. 
    # The median should be exactly 5.0.
    baseline = canary.get_baseline("TEST_AGENT")
    
    assert baseline.query_rate == 5.0, f"Baseline poisoned! Expected 5.0, got {baseline.query_rate}"

def test_near_miss_logging_and_pressure():
    # Write a near miss
    log_near_miss("TEST_AGENT", "AUTHORITY_BOUNDARY_APPROACH", {"action": "deploy"})
    
    # Read it back
    misses = get_recent_near_misses("TEST_AGENT")
    assert len(misses) >= 1
    
    # Check pressure calculation
    pressure_data = calculate_safety_pressure("TEST_AGENT")
    
    assert pressure_data["pressure_score"] > 0.0
    assert pressure_data["near_miss_count_72h"] >= 1
    
    # Clean up test log to not pollute real log
    log_file = r"C:\RaphaelOS\world_model\near_misses.json"
    if os.path.exists(log_file):
        os.remove(log_file)
