import os
import json
import logging

logger = logging.getLogger("rrk.vision.memory")

class VisionMemory:
    def __init__(self, base_dir="vision_memory"):
        self.base_dir = base_dir
        self.dirs = ["brands", "products", "competitors", "patterns"]
        self.setup()
        
    def setup(self):
        for d in self.dirs:
            os.makedirs(os.path.join(self.base_dir, d), exist_ok=True)
            
    def store_pattern(self, category: str, pattern_id: str, data: dict):
        if category not in self.dirs:
            logger.error(f"Invalid vision memory category: {category}")
            return
            
        file_path = os.path.join(self.base_dir, category, f"{pattern_id}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Stored visual pattern {pattern_id} in {category}")
        
    def retrieve_pattern(self, category: str, pattern_id: str) -> dict:
        file_path = os.path.join(self.base_dir, category, f"{pattern_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return {}
