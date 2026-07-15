import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger("rrk.action.memory")

class ActionMemory:
    """
    Stores historical external execution actions for D19 intelligence calculation.
    """
    def __init__(self, base_dir: str = "raphael_storage/actions/"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.filepath = os.path.join(self.base_dir, "action_history.json")
        self._initialize_memory()

    def _initialize_memory(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log_action(self, intent: str, status: str, provider: str, metrics: Dict[str, Any]):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
            
        record = {
            "intent": intent,
            "status": status,
            "provider": provider,
            "metrics": metrics
        }
        history.append(record)
        
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
            
    def get_history(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
