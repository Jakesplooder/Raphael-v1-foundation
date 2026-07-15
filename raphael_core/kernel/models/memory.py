import uuid
import time
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from raphael_core.kernel.interfaces import MemoryTier


class MemoryType(str, Enum):
    DECISION = "decision"
    FACT = "fact"
    SUMMARY = "summary"
    PREFERENCE = "preference"
    OBSERVATION = "observation"
    ERROR = "error"
    ARCHIVE = "archive"


class MemoryRecord(BaseModel):
    """
    Core cognitive unit representing a meaning vector within Raphael.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MemoryType
    content: str
    
    # Cognitive Heuristics
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    
    # Semantic Context
    source: str
    project: Optional[str] = None
    goal: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    
    # Vector Space
    embedding: Optional[List[float]] = None
    
    # Lifecycle
    tier: MemoryTier = MemoryTier.WORKING
    created_at: float = Field(default_factory=time.time)
    last_accessed: float = Field(default_factory=time.time)
    access_count: int = Field(default=0)
    
    def access(self):
        """Update access metrics for recency/frequency tracking."""
        self.last_accessed = time.time()
        self.access_count += 1

    def decay_score(self, current_time: float) -> float:
        """
        Calculate time-decayed relevance.
        Older memories decay unless they have high access counts or importance.
        """
        age_seconds = current_time - self.last_accessed
        age_days = age_seconds / 86400.0
        
        # Simple exponential decay softened by importance and access_count
        base_decay = 0.95 ** age_days
        retention = min(1.0, (self.importance + (self.access_count * 0.05)))
        return base_decay + (1.0 - base_decay) * retention
