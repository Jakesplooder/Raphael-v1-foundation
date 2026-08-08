from abc import ABC, abstractmethod
from ..models.analytics_result import AnalyticsResult

class AnalyticsProvider(ABC):
    @abstractmethod
    def get_asset_performance(self, asset_id: str) -> AnalyticsResult:
        pass
