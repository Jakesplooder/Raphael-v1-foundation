from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

class CommerceProductHistory(BaseModel):
    """
    Commerce Intelligence tracking.
    Every product generation becomes a case study stored in CommerceRepository.
    """
    id: str = Field(default_factory=lambda: f"PROD-{uuid.uuid4().hex[:8].upper()}")
    request_description: str
    brand_identity: Dict[str, Any] = Field(default_factory=dict)
    workflow_template: str
    generation_attempts: List[Dict[str, Any]] = Field(default_factory=list)
    final_assets: List[str] = Field(default_factory=list)
    seo_listings: Dict[str, Any] = Field(default_factory=dict)
    lessons_learned: List[str] = Field(default_factory=list)
    final_metrics: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=datetime.now().timestamp)

class ProductMemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: f"PMEM-{uuid.uuid4().hex[:8].upper()}")
    name: str
    category: str
    performance_score: float = 0.0
    variants: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=datetime.now().timestamp)

class CreativeMemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: f"CMEM-{uuid.uuid4().hex[:8].upper()}")
    category: str # "PromptPattern", "StylePreference", "OCRFailure"
    content: str
    tags: List[str] = Field(default_factory=list)
    timestamp: float = Field(default_factory=datetime.now().timestamp)

class MarketMemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: f"MMEM-{uuid.uuid4().hex[:8].upper()}")
    niche: str
    insight: str
    confidence: float
    timestamp: float = Field(default_factory=datetime.now().timestamp)
