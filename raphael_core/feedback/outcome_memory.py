import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger("rrk.feedback.outcome_memory")

class OutcomeMemory:
    """
    Stores and retrieves real-world outcomes tied to their original simulation IDs.
    """
    def __init__(self, base_dir: str = "raphael_storage/feedback/"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def log_reality_kpi(self, sim_id: str, kpi_name: str, value: Any):
        filepath = os.path.join(self.base_dir, f"{sim_id}_reality.json")
        data = self._load(filepath)
        
        if "kpis" not in data:
            data["kpis"] = {}
        data["kpis"][kpi_name] = value
        
        self._save(filepath, data)
        
    def get_reality_data(self, sim_id: str) -> Dict[str, Any]:
        filepath = os.path.join(self.base_dir, f"{sim_id}_reality.json")
        return self._load(filepath)

    def _load(self, filepath: str) -> dict:
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save(self, filepath: str, data: dict):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
