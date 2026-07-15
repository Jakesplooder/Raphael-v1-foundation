import uuid
import time
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class KnowledgeImportance(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    STRATEGIC = "strategic"


class KnowledgeCategory(str, Enum):
    ACADEMIC = "academic"
    PROGRAMMING = "programming"
    RESEARCH = "research"
    BUSINESS = "business"
    LESSONS_LEARNED = "lessons_learned"
    INVENTORIES = "inventories"
    CURATION = "curation"
    RELATIONSHIPS = "relationships"
    GENERAL = "general"


class KnowledgeTrack(str, Enum):
    PYTHON = "python"
    MACHINE_LEARNING = "machine_learning"
    ARCHITECTURE = "architecture"
    SECURITY = "security"
    MANAGEMENT = "management"
    MARKETING = "marketing"
    UNKNOWN = "unknown"


class KnowledgeItem(BaseModel):
    """
    Explicit factual/informational record.
    Distinct from Memory (which is experiential).
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    source_path: str
    
    category: KnowledgeCategory = KnowledgeCategory.GENERAL
    track: KnowledgeTrack = KnowledgeTrack.UNKNOWN
    importance: KnowledgeImportance = KnowledgeImportance.NORMAL
    
    summary: str = ""
    extracted_text: str = ""
    
    tags: List[str] = Field(default_factory=list)
    relationships: List[str] = Field(default_factory=list)  # E.g., ['python', 'ml']
    
    created_at: float = Field(default_factory=time.time)
    last_updated: float = Field(default_factory=time.time)
