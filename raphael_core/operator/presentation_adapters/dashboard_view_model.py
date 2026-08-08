from typing import List, Optional
from pydantic import BaseModel, Field

class HealthCard(BaseModel):
    overall_score: str
    trend: str
    status: str
    components: List[dict]  # [{"label": "Business", "value": 96}, ...]

class PriorityCard(BaseModel):
    title: str
    reason: str
    score: float
    recommended_action: str
    estimated_time: str

class InitiativeCard(BaseModel):
    name: str
    health: float
    momentum: str
    tasks_complete: int
    tasks_total: int
    blocked: bool
    eta: str
    owner: str

class AgentCard(BaseModel):
    agent: str
    role: str
    status: str
    current_task: str
    last_activity: str
    confidence: float

class RecommendationCard(BaseModel):
    id: str
    title: str
    impact: str
    action_type: str

class TimelineEvent(BaseModel):
    time: str
    description: str

class DashboardViewModel(BaseModel):
    """
    The flattened, presentation-specific model representing the entire Executive Dashboard UI.
    """
    header: str = "Executive Dashboard"
    health: HealthCard
    priorities: List[PriorityCard] = Field(default_factory=list)
    initiatives: List[InitiativeCard] = Field(default_factory=list)
    running_workflows: int = 0
    agent_activity: List[AgentCard] = Field(default_factory=list)
    council_activity: List[str] = Field(default_factory=list)
    alerts: List[str] = Field(default_factory=list)
    recommendations: List[RecommendationCard] = Field(default_factory=list)
    timeline: List[TimelineEvent] = Field(default_factory=list)
