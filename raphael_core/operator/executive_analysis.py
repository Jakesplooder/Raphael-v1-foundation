from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class HealthMetrics(BaseModel):
    business_health: float = 0.0
    execution_health: float = 0.0
    workflow_health: float = 0.0
    agent_health: float = 0.0
    financial_health: Optional[float] = None
    strategic_risk: str = "Medium"

class ObjectivePriority(BaseModel):
    id: str
    title: str
    score: float
    urgency: float
    confidence: float
    business_impact: float
    estimated_cost: float
    reasoning: str

class ExecutiveRecommendation(BaseModel):
    id: str
    action: str
    target: str
    confidence: float
    reasoning: str
    impact: str

class ExecutiveAnalysis(BaseModel):
    """
    The interpreted executive perspective.
    Consumes ExecutiveSnapshot and produces actionable insights and metrics.
    """
    analysis_id: str = Field(default_factory=lambda: "ANA-" + datetime.utcnow().strftime("%Y%m%d%H%M%S"))
    snapshot_id: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    # 6 Core Outputs
    health: HealthMetrics = Field(default_factory=HealthMetrics)
    priorities: List[ObjectivePriority] = Field(default_factory=list)
    recommendations: List[ExecutiveRecommendation] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    opportunities: List[str] = Field(default_factory=list)
    anomalies: List[str] = Field(default_factory=list)
    confidence: float = 0.0

class ExecutiveAnalyzer:
    """
    Orchestrates the interpretation of the ExecutiveSnapshot.
    Passes the snapshot through the Health, Priority, and Recommendation engines.
    """
    def __init__(self):
        from .health_engine import HealthEngine
        from .priority_engine import PriorityEngine
        from .recommendation_engine import RecommendationEngine
        self.health_engine = HealthEngine()
        self.priority_engine = PriorityEngine()
        self.rec_engine = RecommendationEngine()
        
    def analyze(self, snapshot) -> ExecutiveAnalysis:
        health_metrics = self.health_engine.evaluate(snapshot)
        priorities = self.priority_engine.evaluate(snapshot)
        recs = self.rec_engine.evaluate(snapshot)
        
        # Determine risks based on snapshot
        risks = []
        if health_metrics.strategic_risk in ("High", "Critical"):
            risks.append("Critical core subsystems are offline or failing.")
            
        return ExecutiveAnalysis(
            snapshot_id=snapshot.snapshot_id,
            health=health_metrics,
            priorities=priorities,
            recommendations=recs,
            risks=risks,
            confidence=snapshot.completeness # Base confidence on state completeness
        )

# Global singleton
executive_analyzer = ExecutiveAnalyzer()
