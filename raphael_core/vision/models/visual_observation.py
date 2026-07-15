from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class VisionConfidenceScore(BaseModel):
    score: float
    reasoning: str

class VisualLineage(BaseModel):
    venture_id: str
    product_id: Optional[str] = None
    design_id: Optional[str] = None
    vision_review_id: Optional[str] = None
    council_decision_id: Optional[str] = None

class VisualObservation(BaseModel):
    id: str
    source_image_id: str
    confidence: VisionConfidenceScore
    lineage: VisualLineage
    findings: Dict[str, Any]
    recommendations: List[str] = Field(default_factory=list)
