from typing import List, Dict, Any
from datetime import datetime
import uuid
import os
import json

def emit_lifecycle_event(agent_id: str, old_state: str, new_state: str, reason: str, evidence: List[str]):
    """
    Mocks emitting an event node to the World Model.
    """
    # In a full implementation, this creates an Event Node and links it to the Agent Node
    pass

def emit_performance_review(record: dict):
    """
    Mocks emitting a Performance Review Record node to the World Model.
    Persists it to a local json for CLI/testing.
    """
    fp = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), r"\world_model\performance_reviews.json")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    reviews = []
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            reviews = json.load(f)
    reviews.append(record)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2)

def get_performance_reviews() -> List[dict]:
    fp = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), r"\world_model\performance_reviews.json")
    if not os.path.exists(fp):
        return []
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)
        
def acknowledge_review(review_id: str):
    fp = os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), r"\world_model\performance_reviews.json")
    if not os.path.exists(fp): return False
    with open(fp, "r", encoding="utf-8") as f:
        reviews = json.load(f)
    found = False
    for r in reviews:
        if r["review_id"] == review_id:
            r["reviewed_by_aaron"] = True
            found = True
    if found:
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(reviews, f, indent=2)
    return found

class WorldModelEmitter:
    def emit_training_record(self, agent_id: str, training_proposal: Dict[str, Any]) -> str:
        """
        Emits a formalized training record node into the World Model.
        """
        node_id = f"TRN-{str(uuid.uuid4())[:8].upper()}"
        
        log_path = os.path.join(os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), r"\world_model"), "training_records.json")
        try:
            if os.path.exists(log_path):
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            else:
                logs = []
        except Exception:
            logs = []
            
        training_proposal["node_id"] = node_id
        logs.append(training_proposal)
        
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2)
            
        return node_id

def get_training_records() -> List[Dict[str, Any]]:
    log_path = os.path.join(os.path.join(os.environ.get("RAPHAEL_DATA_DIR", r"R:\RaphaelOS"), r"\world_model"), "training_records.json")
    try:
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return []
