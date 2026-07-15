import os
import json
import logging

logger = logging.getLogger("rrk.desktop.memory")

class DesktopMemory:
    """
    Persists desktop interaction intelligence.
    
    Directories:
    - workflows/          — Successful multi-step sequences
    - successful_sequences/ — Atomic action patterns that work
    - failed_actions/     — Actions that failed and recovery strategies
    - application_models/ — Learned UI layouts for specific applications
    - ui_patterns/        — Recurring UI element patterns
    """
    
    def __init__(self, base_dir="desktop_memory"):
        self.base_dir = base_dir
        self.dirs = ["workflows", "successful_sequences", "failed_actions", "application_models", "ui_patterns"]
        self.setup()
        
    def setup(self):
        for d in self.dirs:
            os.makedirs(os.path.join(self.base_dir, d), exist_ok=True)
            
    def store(self, category: str, entry_id: str, data: dict):
        if category not in self.dirs:
            logger.error(f"Invalid desktop memory category: {category}")
            return
            
        file_path = os.path.join(self.base_dir, category, f"{entry_id}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Stored desktop memory '{entry_id}' in {category}")
        
    def retrieve(self, category: str, entry_id: str) -> dict:
        file_path = os.path.join(self.base_dir, category, f"{entry_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return {}
