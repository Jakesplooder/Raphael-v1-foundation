from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class LineageMetadata(BaseModel):
    lineage_id: str
    parent_id: Optional[str] = None
    created_by: str
    approved_by: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    version: str = "1.0"

class ResourceRequest(BaseModel):
    venture_id: str
    resource_type: str
    amount: float
    expected_return: float
    confidence: float
    risk: float
    timeframe: str = "1M"
    
    def portfolio_value(self) -> float:
        # Portfolio Value = (Expected Return * Confidence) - (Resource Cost * Risk)
        return (self.expected_return * self.confidence) - (self.amount * self.risk)



class Metric(BaseModel):
    name: str
    target: float
    current: float = 0.0
    trend: str = "FLAT" # POSITIVE, NEGATIVE, FLAT
    velocity: str = "0%"

class KeyResult(BaseModel):
    name: str
    metrics: List[Metric] = Field(default_factory=list)
    status: str = "ACTIVE"

class Initiative(BaseModel):
    name: str
    owner: str
    contributors: List[str] = Field(default_factory=list)
    key_results: List[KeyResult] = Field(default_factory=list)
    status: str = "ACTIVE"

class StrategicObjective(BaseModel):
    name: str
    initiatives: List[Initiative] = Field(default_factory=list)
    status: str = "ACTIVE"

class Mission(BaseModel):
    statement: str
    objectives: List[StrategicObjective] = Field(default_factory=list)

class GoalHierarchy(BaseModel):
    mission: Mission

from enum import Enum

class VentureStage(str, Enum):
    IDEA = "IDEA"
    VALIDATING = "VALIDATING"
    BUILDING = "BUILDING"
    LAUNCHING = "LAUNCHING"
    GROWING = "GROWING"
    OPTIMIZING = "OPTIMIZING"
    EXITING = "EXITING"
    ARCHIVED = "ARCHIVED"

class VentureResources(BaseModel):
    agent_hours: int = 0
    gpu_hours: int = 0
    compute_allocation: float = 0.0

class Venture(BaseModel):
    name: str
    stage: VentureStage = VentureStage.IDEA
    health_score: float = 100.0
    resources: VentureResources = Field(default_factory=VentureResources)
    priority_score: int = 50
    risk_level: str = "MEDIUM"
    growth_potential: str = "HIGH"
    agents_assigned: List[str] = Field(default_factory=list)

class MarketSignal(BaseModel):
    signal_id: str
    category: str
    source: str
    observation: str
    confidence: float
    timestamp: str

class Opportunity(BaseModel):
    name: str
    market_potential: float = 0.0
    strategic_alignment: float = 0.0
    capability_fit: float = 0.0
    risk: float = 0.0
    resource_cost: float = 0.0
    final_score: float = 0.0
    recommendation: str = ""
