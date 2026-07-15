import logging
import os
import json
from typing import Dict, Any

logger = logging.getLogger("rrk.executive.memory")

class ExecutiveMemoryService:
    def __init__(self, base_dir="executive_history"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        
    def save_strategic_decision(self, exec_id: str, context: Dict, decision: Dict, metrics_before: Dict, metrics_after: Dict, lessons: list):
        action_dir = os.path.join(self.base_dir, exec_id)
        os.makedirs(action_dir, exist_ok=True)
        
        with open(os.path.join(action_dir, "context.json"), "w") as f:
            json.dump(context, f, indent=2)
            
        with open(os.path.join(action_dir, "decision.json"), "w") as f:
            json.dump(decision, f, indent=2)
            
        with open(os.path.join(action_dir, "metrics_before.json"), "w") as f:
            json.dump(metrics_before, f, indent=2)
            
        with open(os.path.join(action_dir, "metrics_after.json"), "w") as f:
            json.dump(metrics_after, f, indent=2)
            
        with open(os.path.join(action_dir, "lessons.json"), "w") as f:
            json.dump(lessons, f, indent=2)
            
        logger.info(f"[{exec_id}] Executive decision saved to memory.")
