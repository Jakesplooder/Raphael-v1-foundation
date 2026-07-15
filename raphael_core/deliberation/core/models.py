from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class Argument(BaseModel):
    source: str
    position: str # e.g. "Reject", "Modify", "Support"
    argument: str
    evidence: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    priority: str = "MEDIUM"

class Option(BaseModel):
    option_id: str
    description: str
    score: float = 0.0
    simulated_outcome: Dict[str, Any] = Field(default_factory=dict)

class DeliberationDecision(BaseModel):
    decision_id: str
    original_action: str
    conflicts: List[str] = Field(default_factory=list)
    options: List[Option] = Field(default_factory=list)
    final_resolution: str
    confidence: float
    uncertainty: List[str] = Field(default_factory=list)
    information_needed: List[str] = Field(default_factory=list)
    reasoning_chain: List[Dict[str, Any]] = Field(default_factory=list)
