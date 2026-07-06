from typing import Optional
from .provider_health import ProviderHealthMonitor
from .budget_manager import get_routing_tier
from .capability_profiles import PROFILES, CapabilityProfile

class ProviderManager:
    def __init__(self):
        self.health_monitor = ProviderHealthMonitor()
        
    def select_provider(self, mode: str, required_capability: str = None) -> Optional[str]:
        """
        Selects the best provider based on budget mode, health, and capability profiles.
        """
        preferred_tier = get_routing_tier(mode)
        
        best_provider = None
        best_score = -1
        
        for provider_name in preferred_tier:
            if not self.health_monitor.is_healthy(provider_name):
                continue
                
            if required_capability:
                profile = PROFILES.get(provider_name)
                if profile:
                    score = getattr(profile, required_capability, 0)
                    if score > best_score:
                        best_score = score
                        best_provider = provider_name
            else:
                # First healthy provider in the tier wins if no capability requirement
                return provider_name
                
        return best_provider or "ollama" # ultimate fallback
        
    def record_success(self, provider_name: str, latency: float, tokens: int, cost: float):
        self.health_monitor.get_health(provider_name).record_success(latency, tokens, cost)
        
    def record_failure(self, provider_name: str, is_429: bool = False, is_timeout: bool = False):
        self.health_monitor.get_health(provider_name).record_failure(is_429, is_timeout)
