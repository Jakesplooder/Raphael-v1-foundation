from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class AnalyticsResult:
    asset_id: str
    collected_at: datetime = field(default_factory=datetime.utcnow)

    views: int = 0
    impressions: int = 0
    clicks: int = 0

    ctr: float = 0.0
    retention: float = 0.0

    conversions: int = 0
    revenue: float = 0.0

    source: str = ""
