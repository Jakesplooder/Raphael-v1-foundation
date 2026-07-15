from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

class BuildCaseStudy(BaseModel):
    """
    Build Intelligence tracking.
    Every build becomes a case study stored permanently in BuilderRepository.
    """
    id: str = Field(default_factory=lambda: f"BCS-{uuid.uuid4().hex[:8].upper()}")
    request_id: str
    request_description: str
    architecture: Dict[str, Any] = Field(default_factory=dict)
    workflow_template: str
    generated_files: List[str] = Field(default_factory=list)
    compiler_errors_encountered: List[str] = Field(default_factory=list)
    patch_history: List[Dict[str, Any]] = Field(default_factory=list)
    successful_fixes: List[Dict[str, str]] = Field(default_factory=list)
    review_results: List[Dict[str, Any]] = Field(default_factory=list)
    lessons_learned: List[str] = Field(default_factory=list)
    final_metrics: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=datetime.now().timestamp)

class EngineeringMemoryEntry(BaseModel):
    """
    Entries for BuilderMemory to move beyond Prompt Engineering into Experience.
    """
    id: str = Field(default_factory=lambda: f"EMEM-{uuid.uuid4().hex[:8].upper()}")
    category: str # e.g. "Pattern", "Component", "CompilerError", "FrameworkDoc", "ArchitectureDecision"
    tags: List[str] = Field(default_factory=list)
    content: str
    context: Dict[str, Any] = Field(default_factory=dict)
    timestamp: float = Field(default_factory=datetime.now().timestamp)
