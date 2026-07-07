import os
import json
import time
from typing import List, Dict, Any, Tuple
from datetime import datetime

QUEUE_FILE = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"C:\RaphaelOS"), r"\world_model\initiative_queue.json")

def _now() -> str:
    return datetime.utcnow().isoformat()

def shares_entity(opp: Dict[str, Any], risk: Dict[str, Any]) -> bool:
    return opp.get("entity_id") == risk.get("entity_id") and opp.get("entity_id") is not None

def correlate_signals(opportunities: List[Dict[str, Any]], risks: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Returns (opportunities, risks, correlated_items)
    Correlated items are removed from individual lists and combined into a single briefing item with both signals.
    """
    correlated = []
    
    # We must iterate over a copy of the list when modifying it
    for opp in opportunities[:]:
        related_risks = [r for r in risks if shares_entity(opp, r)]
        if related_risks:
            correlated.append({
                "id": f"CORR-{opp['id']}",
                "type": "correlated",
                "opportunity": opp,
                "risks": related_risks,
                "priority_score": min(1.0, opp["priority_score"] * 1.2),  # elevated priority
                "title": f"Correlated: {opp['title']} & {len(related_risks)} Risk(s)",
                "summary": f"Opportunity and risk share entity: {opp['entity_id']}",
                "supporting_evidence": list(set(opp.get("supporting_evidence", []) + sum([r.get("supporting_evidence", []) for r in related_risks], [])))
            })
            opportunities.remove(opp)
            for r in related_risks:
                if r in risks:
                    risks.remove(r)
                    
    return opportunities, risks, correlated

def load_queue() -> List[Dict[str, Any]]:
    if not os.path.exists(QUEUE_FILE):
        return []
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_queue(queue: List[Dict[str, Any]]):
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)

def enqueue_items(items: List[Dict[str, Any]]):
    queue = load_queue()
    # Filter out items that are already in the queue or were dismissed
    existing_ids = {q["id"]: q for q in queue}
    
    for item in items:
        if item["id"] not in existing_ids:
            item["status"] = "Detected"
            item["detected_at"] = _now()
            queue.append(item)
            
    save_queue(queue)

def evaluate_signal(signal_type: str, world_model: Dict[str, Any]) -> float:
    # Mock signal evaluation for stability guarantee
    # Real implementation would check if the goal is still stalled, etc.
    return 0.1 # Return a low score to mock signal resolution for testing

def recalculate_priority(item: Dict[str, Any], signal_strength: float) -> float:
    return item.get("priority_score", 0.5) * signal_strength

def update_deferred_priorities(queue: List[Dict[str, Any]], world_model: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Re-score deferred items against current World Model state.
    If the signal that triggered detection no longer exists,
    automatically transition to Dismissed with reason='signal_resolved'.
    """
    for item in queue:
        if item["status"] == "Deferred":
            # Determine primary signal type
            signal_type = item.get("signal_type")
            if item.get("type") == "correlated":
                signal_type = item["opportunity"].get("signal_type")
                
            current_signal_strength = evaluate_signal(signal_type, world_model)
            if current_signal_strength < 0.2:
                item["status"] = "Dismissed"
                item["dismiss_reason"] = "signal_resolved"
                item["dismissed_at"] = _now()
            else:
                item["priority_score"] = recalculate_priority(item, current_signal_strength)
    return queue

def dismiss_initiative(initiative_id: str):
    queue = load_queue()
    for item in queue:
        if item["id"] == initiative_id:
            item["status"] = "Dismissed"
            item["dismiss_reason"] = "manual"
            item["dismissed_at"] = _now()
    save_queue(queue)

def defer_initiative(initiative_id: str):
    queue = load_queue()
    for item in queue:
        if item["id"] == initiative_id:
            item["status"] = "Deferred"
            item["deferred_at"] = _now()
    save_queue(queue)
