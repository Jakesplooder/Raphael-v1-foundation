import os
import json
from raphael_core.agent_workload_balancer import analyze_workloads, _mock_agent_history
from raphael_core.llm_cost_optimizer import identify_cost_opportunities, load_ledger, evaluate_local_viability
from raphael_core.initiative_queue import load_queue, enqueue_items, update_deferred_priorities, save_queue

def test_cost_privacy():
    ledger = load_ledger()
    for entry in ledger:
        # Guarantee no PII or content is present
        assert "prompt" not in entry
        assert "response" not in entry
        # Guarantee necessary optimization fields exist
        assert "task_type" in entry
        assert "tokens_consumed" in entry or ("tokens_input" in entry and "tokens_output" in entry)
        assert "could_use_local" in entry

def test_thrashing_case_1_ignored():
    # 1-day 80% imbalance
    _mock_agent_history["Developer Agent"] = {"current_tasks": 7, "consecutive_high_days": 1, "pressure_score": 42}
    opps = analyze_workloads()
    assert len(opps) == 0

def test_thrashing_case_2_triggers():
    # 4-day 50% imbalance
    _mock_agent_history["Developer Agent"] = {"current_tasks": 7, "consecutive_high_days": 4, "pressure_score": 42}
    opps = analyze_workloads()
    assert len(opps) == 1
    assert opps[0]["signal_type"] == "agent_overload"

def test_thrashing_case_3_reset_behavior():
    # Imbalance was detected, queued, and deferred
    opp = {
        "id": "OPP-BAL-DEV",
        "signal_type": "agent_overload",
        "status": "Deferred",
        "priority_score": 0.8
    }
    save_queue([opp])
    
    # Day 5: Imbalance drops
    # (Mock the evaluate_signal in initiative_queue to return 0.1 for this test)
    import raphael_core.initiative_queue as iq
    original_eval = iq.evaluate_signal
    def mock_eval(sig, wm):
        return 0.15 # Under 0.2 threshold
    iq.evaluate_signal = mock_eval
    
    try:
        queue = load_queue()
        queue = update_deferred_priorities(queue)
        
        assert queue[0]["status"] == "Dismissed"
        assert queue[0]["dismiss_reason"] == "signal_resolved"
    finally:
        iq.evaluate_signal = original_eval

def test_cost_optimizer():
    evaluate_local_viability()
    opps = identify_cost_opportunities()
    # Mock data should detect 1 claude task but it doesn't meet the acute threshold
    assert len(opps) == 0
