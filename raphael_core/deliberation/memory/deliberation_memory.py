import logging
import os
import json
from typing import Dict, Any
from ..core.models import DeliberationDecision

logger = logging.getLogger("rrk.deliberation.memory")

class DeliberationMemoryService:
    def __init__(self, base_dir="deliberation_history"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        
    def save_decision(self, decision: DeliberationDecision):
        action_dir = os.path.join(self.base_dir, decision.decision_id)
        os.makedirs(action_dir, exist_ok=True)
        
        filepath = os.path.join(action_dir, "outcome.json")
        with open(filepath, "w") as f:
            json.dump(decision.model_dump(), f, indent=2)
            
        logger.info(f"[{decision.decision_id}] Reasoning chain saved to Deliberation Memory.")
