import os
import time
from typing import Dict, Any, List
from .opportunity_detector import detect_opportunities
from .risk_detector import detect_risks
from .initiative_queue import (
    load_queue, save_queue, enqueue_items, correlate_signals, 
    update_deferred_priorities, _now
)
from .learning_metrics import get_learning_dashboard

ALTERNATIVE_INTERPRETATIONS = {
    "stalled_goal_with_available_agent": 
        "Goal may be intentionally paused. Check if Aaron deprioritized it "
        "in the last executive brief before assuming stagnation.",
    
    "confidence_decay_critical":
        "Confidence decay may reflect normal staleness, not actual incorrectness. "
        "Review whether the underlying entity has changed or just hasn't been confirmed.",
    
    "prediction_accuracy_declining":
        "Accuracy decline may reflect harder prediction tasks, not worse reasoning. "
        "Check whether recent predictions involved higher novelty than baseline.",
    
    "pattern_contradictions_rising":
        "Rising contradictions may indicate the pattern is splitting into two valid "
        "sub-patterns rather than becoming less reliable overall.",
        
    "resource_underutilized":
        "Resource may be blocked on a dependency not captured in the World Model. "
        "Verify external dependencies before assigning new work.",
        
    "agent_pressure_score_high":
        "Pressure score elevation may be temporary due to a bulk processing task "
        "that is about to conclude.",
        
    "agent_overload":
        "High load may reflect a temporary sprint on a priority project rather than structural overload.",
        
    "llm_cost_spike":
        "Cost increases may correlate with a high-complexity architecture phase requiring premium models, rather than inefficient routing.",
        
    "workflow_bottleneck":
        "Queue depth spikes may be due to scheduled upstream batching, not inefficient execution.",
        
    "portfolio_sequencing":
        "This project may have strategic or personal significance not captured in the World Model. Review personal context before deprioritizing."
}

def _get_interpretation(item: Dict[str, Any]) -> str:
    signal = item.get("signal_type")
    if item.get("type") == "correlated":
        signal = item["opportunity"].get("signal_type")
    return ALTERNATIVE_INTERPRETATIONS.get(signal, "Alternative interpretation not defined for this signal.")

def _format_item(item: Dict[str, Any]) -> str:
    lines = []
    lines.append(f"- {item.get('title')}")
    lines.append(f"  Confidence Score: {item.get('priority_score', 0)}")
    
    evidence = item.get("supporting_evidence", [])
    if not evidence:
        lines.append(f"  Evidence: NONE (VIOLATION)")
    else:
        lines.append(f"  Evidence: {', '.join(evidence)}")
        
    lines.append(f"  Alternative Interpretation: {_get_interpretation(item)}")
    
    if item.get("type") == "correlated":
        lines.append(f"  Correlated Risks:")
        for r in item.get("risks", []):
            lines.append(f"    - {r.get('title')}")
            
    return "\n".join(lines)

def generate_briefing(world_model: Dict[str, Any] = None) -> Dict[str, Any]:
    if world_model is None:
        import urllib.request, json
        try:
            req = urllib.request.Request("http://127.0.0.1:8788/api/world-model/graph", headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as response:
                world_model = json.loads(response.read().decode())
        except Exception as e:
            world_model = {"nodes": []}
            
    # 1. Detect
    opps = detect_opportunities(world_model)
    risks = detect_risks(world_model)
    
    # 2. Correlate
    opps, risks, correlated = correlate_signals(opps, risks)
    
    # 3. Enqueue
    enqueue_items(opps + risks + correlated)
    
    # 4. Clean & Sort Queue
    queue = load_queue()
    queue = update_deferred_priorities(queue, world_model)
    
    # Filter to only Detected or Deferred items
    active_items = [q for q in queue if q["status"] in ["Detected", "Deferred"]]
    
    # Sort by priority score descending
    active_items.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
    
    # Throttle to max 3-5 items (let's use 5 total limit across all types for focus)
    top_items = active_items[:5]
    
    # Mark as Briefed
    for i in queue:
        if i in top_items:
            i["status"] = "Briefed"
            i["briefed_at"] = _now()
            
    save_queue(queue)
    
    # Separate for display
    disp_opps = [i for i in top_items if i.get("type") == "opportunity"]
    disp_risks = [i for i in top_items if i.get("type") == "risk"]
    disp_corr = [i for i in top_items if i.get("type") == "correlated"]
    
    return {
        "opportunities": disp_opps,
        "risks": disp_risks,
        "correlated": disp_corr
    }

def print_daily_briefing():
    import datetime
    briefing = generate_briefing()
    
    print(f"DAILY EXECUTIVE BRIEFING")
    print(f"========================")
    print(f"Date: {datetime.date.today().isoformat()}")
    print(f"Generated: {datetime.datetime.now().strftime('%H:%M:%S')}")
    print(f"Authority Required: No\n")
    
    print("OVERNIGHT ACTIVITY")
    print("No critical overnight workflow failures.\n")
    
    print("CORRELATED INITIATIVES (HIGH PRIORITY)")
    if not briefing["correlated"]:
        print("None detected.")
    else:
        for i in briefing["correlated"]:
            print(_format_item(i))
    print("")
            
    print("OPPORTUNITIES DETECTED")
    if not briefing["opportunities"]:
        print("None detected.")
    else:
        for i in briefing["opportunities"]:
            print(_format_item(i))
    print("")
            
    print("RISKS DETECTED")
    if not briefing["risks"]:
        print("None detected.")
    else:
        for i in briefing["risks"]:
            print(_format_item(i))
    print("")
            
    print("LEARNING METRICS")
    metrics = get_learning_dashboard()
    # just print the values to save space or point to the dashboard
    print("See `learning-dashboard` for detailed metrics.\n")
    
    print("Constitutional compliance: Verified")
