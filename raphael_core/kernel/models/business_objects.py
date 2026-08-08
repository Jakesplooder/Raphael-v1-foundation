from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

def generate_id():
    return str(uuid.uuid4())

class BusinessObject(BaseModel):
    id: str = Field(default_factory=generate_id)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class Business(BusinessObject):
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    status: str = "active"

class Initiative(BusinessObject):
    business_id: str
    name: str
    objective: str
    status: str = "planning" # planning, active, completed, paused
    priority: str = "medium"

class Campaign(BusinessObject):
    initiative_id: str
    name: str
    status: str = "draft"
    metrics: Dict[str, float] = Field(default_factory=dict) # revenue, clicks, ctr
    target_audience: Optional[str] = None

class ContentAsset(BusinessObject):
    campaign_id: str
    title: str
    asset_type: str # video, article, thumbnail
    status: str = "draft" # draft, QA, published
    url: Optional[str] = None

class AffiliateLink(BusinessObject):
    campaign_id: str
    partner: str
    url: str
    clicks: int = 0
    conversions: int = 0
    revenue_generated: float = 0.0

class Product(BusinessObject):
    business_id: str
    name: str
    sku: Optional[str] = None
    price: float = 0.0
    status: str = "active"

class Supplier(BusinessObject):
    name: str
    contact_info: Optional[str] = None
    rating: float = 0.0

class Order(BusinessObject):
    business_id: str
    customer_id: Optional[str] = None
    product_ids: List[str] = Field(default_factory=list)
    total_amount: float
    status: str = "pending"

class Revenue(BusinessObject):
    business_id: str
    source_id: str # order_id, campaign_id, etc.
    amount: float
    currency: str = "USD"
    date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class Expense(BusinessObject):
    business_id: str
    category: str
    amount: float
    currency: str = "USD"
    date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class KPI(BusinessObject):
    business_id: str
    metric_name: str
    value: float
    target: Optional[float] = None
    date: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class Experiment(BusinessObject):
    business_id: str
    campaign_id: Optional[str] = None
    hypothesis: str
    control_asset_id: str
    treatment_asset_id: str
    metric_goal: str
    baseline_metrics: Dict[str, float] = Field(default_factory=dict)
    treatment_metrics: Dict[str, float] = Field(default_factory=dict)
    sample_size: int = 0
    confidence: float = 0.0
    status: str = "proposed" # proposed, running, completed, promoted, rejected
    winner: Optional[str] = None
    lessons_learned: List[str] = Field(default_factory=list)
    builder_recommendation: Optional[str] = None

class AssetPerformance(BusinessObject):
    business_id: str
    asset_id: str
    views: int = 0
    ctr: float = 0.0
    retention: float = 0.0
    clicks: int = 0
    conversions: int = 0
    revenue: float = 0.0

class BusinessLesson(BusinessObject):
    business_id: str
    category: str # hook, thumbnail, pricing, audience, distribution
    observation: str
    evidence: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.0
    applies_to: List[str] = Field(default_factory=list)
    created_from: Optional[str] = None # experiment_id

class Channel(BusinessObject):
    business_id: str
    platform: str
    channel_id: str
    name: str
    subscribers: int = 0
    connected: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AnalyticsSnapshot(BusinessObject):
    asset_id: str
    provider: str
    metrics: Dict[str, float] = Field(default_factory=dict)
    collected_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class MetricDiagnosis(BusinessObject):
    business_id: str
    asset_id: str
    failed_metric: str
    observed_metrics: Dict[str, float] = Field(default_factory=dict)
    diagnosis_category: str
    explanation: str
    confidence: float
    evidence: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)

class BuilderProposal(BusinessObject):
    business_id: str
    asset_id: str
    diagnosis_id: str
    proposed_changes: Dict[str, Any] = Field(default_factory=dict)
    expected_impact: str
    status: str = "draft" # draft, approved, rejected, testing

class OptimizationRun(BusinessObject):
    business_id: str
    asset_id: str
    diagnosis_id: str
    proposal_id: str
    experiment_id: str
    outcome: Optional[str] = None # success, failed
    improvement_score: Optional[float] = None

class BusinessState(BusinessObject):
    business_id: str
    revenue: float = 0.0
    expenses: float = 0.0
    active_campaigns: int = 0
    customers: int = 0
    cash_position: float = 0.0
    growth_rate: float = 0.0

class Decision(BusinessObject):
    business_id: str
    decision_type: str # investment, expansion, hiring, campaign, shutdown, partnership
    proposal: str
    supporting_data: Dict[str, Any] = Field(default_factory=dict)
    expected_return: float = 0.0
    risks: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    status: str = "proposed" # proposed, approved, rejected, executed

class ROIAnalysis(BusinessObject):
    decision_id: str
    investment: float
    expected_revenue: float
    expected_profit: float
    roi_percentage: float
    confidence: float

class RiskAssessment(BusinessObject):
    decision_id: str
    risk_description: str
    probability: float
    impact: str # Low, Medium, High
    mitigation_strategy: Optional[str] = None
