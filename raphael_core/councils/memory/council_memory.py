import logging
import os
import json
from typing import Dict, Any

logger = logging.getLogger("rrk.councils.memory.council")

class CouncilMemoryService:
    """Stores council history: proposals, discussions, votes, and lessons."""
    def __init__(self, base_dir="council_history"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        
    def save_decision(self, action_id: str, decision_data: Dict[str, Any]):
        action_dir = os.path.join(self.base_dir, action_id)
        os.makedirs(action_dir, exist_ok=True)
        
        filepath = os.path.join(action_dir, "decision.json")
        with open(filepath, "w") as f:
            json.dump(decision_data, f, indent=2)
            
        logger.info(f"[{action_id}] Decision saved to Council Memory.")
