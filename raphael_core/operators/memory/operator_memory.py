import logging
import os
import json

logger = logging.getLogger("rrk.operators.memory")

class OperatorMemory:
    def __init__(self, base_dir="operator_memory"):
        self.base_dir = base_dir
        self.dirs = ["thesis", "experiments", "customers", "decisions"]
        
    def setup_venture(self, venture_id: str):
        for d in self.dirs:
            os.makedirs(os.path.join(self.base_dir, venture_id, d), exist_ok=True)
            
    def store_memory(self, venture_id: str, category: str, memory_id: str, data: dict):
        if category not in self.dirs:
            logger.error(f"Invalid memory category: {category}")
            return
            
        file_path = os.path.join(self.base_dir, venture_id, category, f"{memory_id}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Stored {category} memory for {venture_id}: {memory_id}")
        
    def retrieve_memory(self, venture_id: str, category: str, memory_id: str) -> dict:
        file_path = os.path.join(self.base_dir, venture_id, category, f"{memory_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return {}
