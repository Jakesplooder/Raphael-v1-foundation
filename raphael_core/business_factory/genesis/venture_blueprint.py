from pydantic import BaseModel, Field
from typing import List, Optional

class VentureBlueprint(BaseModel):
    venture_id: str
    name: str
    venture_type: str
    ceo_type: str
    initial_departments: List[str] = Field(default_factory=list)
    market_score: float = 0.0
    confidence: float = 0.0
    initial_capital: float = 0.0
    opportunity_source: str = ""
