import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger("rrk.world.memory")

class WorldKnowledgeGraph:
    def __init__(self, base_dir="world_memory"):
        self.base_dir = base_dir
        self.categories = {
            "entities": ["companies", "technologies", "markets", "regulations"],
            "relationships": ["creates_opportunity", "threatens", "competes_with", "enables"],
            "events": ["market_events", "competitor_events", "regulatory_events"],
            "reasoning": ["opportunity_chains"]
        }
        self.setup_structure()

    def setup_structure(self):
        for main_cat, subcats in self.categories.items():
            for subcat in subcats:
                os.makedirs(os.path.join(self.base_dir, main_cat, subcat), exist_ok=True)
                
    def store_node(self, main_category: str, subcategory: str, node_id: str, data: dict):
        if main_category not in self.categories or subcategory not in self.categories[main_category]:
            logger.error(f"Invalid category path: {main_category}/{subcategory}")
            return
            
        file_path = os.path.join(self.base_dir, main_category, subcategory, f"{node_id}.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Stored node {node_id} in {main_category}/{subcategory}")
        
    def retrieve_node(self, main_category: str, subcategory: str, node_id: str) -> dict:
        file_path = os.path.join(self.base_dir, main_category, subcategory, f"{node_id}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return {}
        
    def retrieve_reasoning_chain(self, chain_id: str) -> List[Dict[str, Any]]:
        chain_data = self.retrieve_node("reasoning", "opportunity_chains", chain_id)
        return chain_data.get("chain", [])
