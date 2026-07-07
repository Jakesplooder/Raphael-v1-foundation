from dataclasses import dataclass
from typing import List
import statistics

@dataclass
class Baseline:
    query_rate: float
    task_creation_rate: float
    approval_request_rate: float

@dataclass
class CanarySignal:
    type_name: str
    severity: str

class CanaryAgent:
    """
    Sits directly under Raphael Core.
    Not a council member. Not a specialized agent.
    A continuous behavioral observer.
    """
    
    def __init__(self):
        # Mock historical history structure: List of dicts representing daily stats
        self.history = {}
        
    def _get_historical_data(self, agent_id: str, days: int) -> List[dict]:
        # Mock retrieval of past 'days' stats for agent
        return self.history.get(agent_id, [])

    def compute_robust_baseline(self, agent_id: str, days: int = 30) -> Baseline:
        """
        Calculates median baseline over the past 'days' to resist poisoning.
        Drops top and bottom 10% before median computation.
        """
        data = self._get_historical_data(agent_id, days)
        if not data:
            return Baseline(0.0, 0.0, 0.0)
            
        def _robust_median(metric_name: str) -> float:
            values = sorted([d.get(metric_name, 0.0) for d in data])
            if len(values) >= 10:
                trim_count = max(1, int(len(values) * 0.10))
                values = values[trim_count:-trim_count]
            if not values:
                return 0.0
            return statistics.median(values)
            
        return Baseline(
            query_rate=_robust_median("query_rate"),
            task_creation_rate=_robust_median("task_creation_rate"),
            approval_request_rate=_robust_median("approval_request_rate")
        )

    def get_baseline(self, agent_id: str) -> Baseline:
        return self.compute_robust_baseline(agent_id, days=30)
        
    def get_current_behavior(self, agent_id: str, window_hours: int = 24) -> Baseline:
        # Mock returning current 24 hour stats
        data = self._get_historical_data(agent_id, 1)
        if data:
            d = data[-1]
            return Baseline(d.get("query_rate", 0.0), d.get("task_creation_rate", 0.0), d.get("approval_request_rate", 0.0))
        return Baseline(0.0, 0.0, 0.0)
        
    def baseline_was_set_during_anomaly(self, agent_id: str) -> bool:
        # Mock logic checking if the entire 30-day baseline period was anomalously high compared to 90-day
        return False

    def observe(self, agent_id: str) -> List[CanarySignal]:
        """
        Asks one question:
        'Is this agent behaving consistently with its history?'
        """
        baseline = self.get_baseline(agent_id)
        current = self.get_current_behavior(agent_id, window_hours=24)
        
        signals = []
        
        # Avoid div zero by defaulting baseline to at least 1.0 if it's currently very low
        base_qr = max(1.0, baseline.query_rate)
        base_tc = max(1.0, baseline.task_creation_rate)
        base_ar = max(1.0, baseline.approval_request_rate)
        
        if current.query_rate > base_qr * 2.0:
            signals.append(CanarySignal("query_rate_spike", severity="warning"))
            
        if current.task_creation_rate > base_tc * 3.0:
            signals.append(CanarySignal("task_creation_anomaly", severity="warning"))
            
        if current.approval_request_rate > base_ar * 5.0:
            signals.append(CanarySignal("approval_flood", severity="critical"))
            
        if self.baseline_was_set_during_anomaly(agent_id):
            signals.append(CanarySignal("baseline_integrity_risk", severity="warning"))
            
        return signals

def run_canary_observation(agent_id: str) -> List[CanarySignal]:
    canary = CanaryAgent()
    return canary.observe(agent_id)
