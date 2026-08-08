from typing import Dict, Optional
from .providers.base import AnalyticsProvider
from .models.analytics_result import AnalyticsResult

class AnalyticsGateway:
    def __init__(self):
        self.providers: Dict[str, AnalyticsProvider] = {}

    def register_provider(self, name: str, provider: AnalyticsProvider):
        self.providers[name] = provider

    def collect_asset_metrics(self, provider_name: str, asset_id: str) -> Optional[AnalyticsResult]:
        if provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not registered in AnalyticsGateway")
            
        provider = self.providers[provider_name]
        return provider.get_asset_performance(asset_id)
