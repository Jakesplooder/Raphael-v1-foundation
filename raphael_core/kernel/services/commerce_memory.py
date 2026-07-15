import logging
from typing import List, Dict, Any, Optional

from ..models.commerce_intelligence import ProductMemoryEntry, CreativeMemoryEntry, MarketMemoryEntry

logger = logging.getLogger("rrk.services.commerce_memory")

class CommerceMemoryService:
    """
    A tri-vault intelligence repository for Commerce.
    Stores Product Memory, Creative Memory, and Market Memory.
    """
    def __init__(self):
        self.product_memory: List[ProductMemoryEntry] = []
        self.creative_memory: List[CreativeMemoryEntry] = []
        self.market_memory: List[MarketMemoryEntry] = []
        
    def save_creative_lesson(self, category: str, content: str, tags: List[str] = None):
        entry = CreativeMemoryEntry(category=category, content=content, tags=tags or [])
        self.creative_memory.append(entry)
        logger.info(f"[CommerceMemory] Saved Creative Lesson: {content[:100]}...")
        # In a full implementation, persist to Qdrant
        
    def save_market_insight(self, niche: str, insight: str, confidence: float = 1.0):
        entry = MarketMemoryEntry(niche=niche, insight=insight, confidence=confidence)
        self.market_memory.append(entry)
        logger.info(f"[CommerceMemory] Saved Market Insight for {niche}")
        
    def save_product_history(self, name: str, category: str, performance_score: float = 0.0):
        entry = ProductMemoryEntry(name=name, category=category, performance_score=performance_score)
        self.product_memory.append(entry)
        logger.info(f"[CommerceMemory] Vaulted Product History: {name}")
