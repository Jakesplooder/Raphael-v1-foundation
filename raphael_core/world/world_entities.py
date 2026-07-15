from pydantic import BaseModel
from typing import Optional

class WorldSignal(BaseModel):
    id: str
    content: str
    source: str
    confidence: float = 0.0
    verification_count: int = 1
    type: str = "GENERAL"

class MarketTrend(BaseModel):
    name: str
    description: str
    impact_score: float

class Competitor(BaseModel):
    name: str
    threat_level: str
