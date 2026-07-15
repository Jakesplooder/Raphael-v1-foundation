from pydantic import BaseModel, Field
from typing import List, Optional

class CouncilDecision(BaseModel):
    action_id: str
    council: str
    decision: str # APPROVED, REJECTED, REVISION_REQUIRED
    severity: str = "LOW" # LOW, MEDIUM, HIGH, CRITICAL
    confidence: float = 1.0
    uncertainty: str = ""
    risks: List[str] = Field(default_factory=list)
    required_changes: List[str] = Field(default_factory=list)
    impact_domains: List[str] = Field(default_factory=list)
    affected_components: List[str] = Field(default_factory=list)
    re_review_required: List[str] = Field(default_factory=list)
    memory_update: bool = True
