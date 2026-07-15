import os
import json
import logging

logger = logging.getLogger("rrk.business_factory.memory")

class BusinessMemory:
    """
    Final memory layer for the entire Business Factory.
    
    Categories:
    - successful/           — Ventures that succeeded
    - failed/               — Ventures that failed (and why)
    - patterns/             — Winning business models
    - market_intelligence/  — What markets work
    - architecture_history/ — Why the factory looks the way it does
    """
    
    def __init__(self, base_dir="business_factory_memory"):
        self.base_dir = base_dir
        self.categories = ["successful", "failed", "patterns", "market_intelligence", "architecture_history"]
        self.setup()
        
    def setup(self):
        for cat in self.categories:
            os.makedirs(os.path.join(self.base_dir, cat), exist_ok=True)
            
    def store(self, category: str, entry_id: str, data: dict):
        if category not in self.categories:
            logger.error(f"Invalid business memory category: {category}")
            return
        file_path = os.path.join(self.base_dir, category, f"{entry_id}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Stored business memory '{entry_id}' in {category}")
        
    def retrieve(self, category: str, entry_id: str) -> dict:
        file_path = os.path.join(self.base_dir, category, f"{entry_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return {}
        
    def list_category(self, category: str) -> list:
        cat_dir = os.path.join(self.base_dir, category)
        if os.path.exists(cat_dir):
            return [f.replace(".json", "") for f in os.listdir(cat_dir) if f.endswith(".json")]
        return []
