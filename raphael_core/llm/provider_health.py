import time
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class HealthStatus:
    last_response_time: float = 0.0
    latency_average: float = 0.0
    timeout_count: int = 0
    failure_count: int = 0
    rate_limit_count: int = 0  # 429s
    unavailable: bool = False
    average_tokens_sec: float = 0.0
    total_cost_estimate: float = 0.0
    
    def record_success(self, latency: float, tokens: int, cost: float):
        self.last_response_time = time.time()
        self.latency_average = (self.latency_average * 0.9) + (latency * 0.1) if self.latency_average > 0 else latency
        tps = tokens / latency if latency > 0 else 0
        self.average_tokens_sec = (self.average_tokens_sec * 0.9) + (tps * 0.1) if self.average_tokens_sec > 0 else tps
        self.total_cost_estimate += cost
        self.unavailable = False
        
    def record_failure(self, is_429: bool = False, is_timeout: bool = False):
        self.failure_count += 1
        if is_429:
            self.rate_limit_count += 1
        if is_timeout:
            self.timeout_count += 1
            
        if self.failure_count > 3 or self.rate_limit_count > 2:
            self.unavailable = True
            
    def reset(self):
        self.failure_count = 0
        self.timeout_count = 0
        self.rate_limit_count = 0
        self.unavailable = False

class ProviderHealthMonitor:
    def __init__(self):
        self.health_records: Dict[str, HealthStatus] = {
            "claude": HealthStatus(),
            "gemini": HealthStatus(),
            "ollama": HealthStatus(),
            "openai": HealthStatus(),
            "local_reasoner": HealthStatus()
        }
        
    def get_health(self, provider_name: str) -> HealthStatus:
        return self.health_records.get(provider_name.lower(), HealthStatus())
        
    def is_healthy(self, provider_name: str) -> bool:
        health = self.get_health(provider_name)
        return not health.unavailable
