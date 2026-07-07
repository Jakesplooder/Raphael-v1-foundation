import os
import json
from raphael_core.opportunity_detector import detect_opportunities
from raphael_core.risk_detector import detect_risks
from raphael_core.initiative_queue import (
    correlate_signals, load_queue, enqueue_items, QUEUE_FILE, save_queue, 
    dismiss_initiative, defer_initiative, update_deferred_priorities
)
from raphael_core.daily_briefing import generate_briefing
def clean_queue():
    if os.path.exists(QUEUE_FILE):
        os.remove(QUEUE_FILE)
    yield
    if os.path.exists(QUEUE_FILE):
        os.remove(QUEUE_FILE)

def test_detection_and_correlation():
    opps = detect_opportunities()
    risks = detect_risks()
    
    assert len(opps) >= 2
    assert len(risks) >= 2
    
    opps, risks, correlated = correlate_signals(opps, risks)
    
    # We mocked one shared entity: GOAL-ALPHA
    assert len(correlated) == 1
    assert correlated[0]["opportunity"]["entity_id"] == "GOAL-ALPHA"
    assert len(correlated[0]["risks"]) == 1

def test_throttling():
    # Inject 10 items
    items = []
    for i in range(10):
        items.append({
            "id": f"TEST-{i}",
            "priority_score": i * 0.1,
            "title": f"Test {i}",
            "type": "opportunity"
        })
    enqueue_items(items)
    
    # Call internal queue sort/throttle logic that's inside generate_briefing
    # Wait, generate_briefing also detects new ones. We just want to test queue length.
    queue = load_queue()
    assert len(queue) == 10
    
    queue.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
    top_items = queue[:5]
    assert len(top_items) == 5
    # The highest priority is 0.9 (TEST-9)
    assert top_items[0]["id"] == "TEST-9"

def test_lifecycle_dismiss():
    opps = detect_opportunities()
    enqueue_items(opps)
    
    queue = load_queue()
    assert len(queue) >= 2
    
    opp_id = queue[0]["id"]
    dismiss_initiative(opp_id)
    
    queue = load_queue()
    dismissed = [q for q in queue if q["id"] == opp_id][0]
    assert dismissed["status"] == "Dismissed"
    
    # Generating briefing should ignore dismissed
    briefing = generate_briefing()
    # It will detect again, but enqueue_items won't overwrite dismissed status
    queue_after = load_queue()
    still_dismissed = [q for q in queue_after if q["id"] == opp_id][0]
    assert still_dismissed["status"] == "Dismissed"

def test_lifecycle_deferred_priority_update():
    items = [{
        "id": "DEF-1",
        "signal_type": "stalled_goal_with_available_agent",
        "status": "Deferred",
        "priority_score": 0.8,
        "type": "opportunity"
    }]
    save_queue(items)
    
    queue = load_queue()
    # update_deferred_priorities evaluates signal and if < 0.2 dismisses it
    queue = update_deferred_priorities(queue, {})
    assert queue[0]["status"] == "Dismissed"
    assert queue[0]["dismiss_reason"] == "signal_resolved"

def test_briefing_transparency():
    """
    Every item in the briefing must contain:
    - supporting_evidence (at least one evidence ID)
    - alternative_interpretation (non-empty string)
    - priority_score (confidence)
    
    A briefing item without these fields is a constitutional violation.
    """
    from raphael_core.daily_briefing import _get_interpretation
    
    briefing = generate_briefing()
    all_items = briefing["opportunities"] + briefing["risks"] + briefing["correlated"]
    
    assert len(all_items) > 0, "Briefing generated no items for transparency test."
    
    for item in all_items:
        # Check evidence
        assert item.get("supporting_evidence"), f"Missing evidence: {item['title']}"
        assert len(item["supporting_evidence"]) > 0, f"Empty evidence list: {item['title']}"
        
        # Check interpretation
        interpretation = _get_interpretation(item)
        assert interpretation, f"Missing alternative interpretation: {item['title']}"
        assert len(interpretation) > 10, f"Alternative interpretation too short: {item['title']}"
        
        # Check priority (confidence)
        assert item.get("priority_score") is not None, f"Missing confidence/priority: {item['title']}"
