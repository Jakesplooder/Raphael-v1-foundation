import logging
from typing import Dict, List, Any
from ..core.models import Metric
from ..core.events import ExecutiveEventBus, ExecutiveEvent, ExecutiveEventType

logger = logging.getLogger("rrk.executive.kpi")

class KPIManager:
    def __init__(self, event_bus: ExecutiveEventBus):
        self.event_bus = event_bus
        self.metrics_history: Dict[str, List[float]] = {}
        
    def update_metric(self, venture: str, metric_name: str, value: float, target: float):
        key = f"{venture}:{metric_name}"
        if key not in self.metrics_history:
            self.metrics_history[key] = []
            
        history = self.metrics_history[key]
        history.append(value)
        
        trend = "FLAT"
        velocity = "0%"
        if len(history) >= 2:
            prev = history[-2]
            diff = value - prev
            pct_change = (diff / prev) * 100 if prev != 0 else 0
            
            trend = "NEGATIVE" if diff < 0 else ("POSITIVE" if diff > 0 else "FLAT")
            velocity = f"{pct_change:+.1f}%"
            
            if "cost" in metric_name.lower() and value > target:
                self.event_bus.emit(ExecutiveEvent(
                    event_type=ExecutiveEventType.GOAL_AT_RISK,
                    source="KPIManager",
                    payload={
                        "venture": venture,
                        "metric": metric_name,
                        "value": value,
                        "target": target,
                        "trend": trend,
                        "velocity": velocity
                    }
                ))
                
        logger.info(f"Updated KPI [{venture}] {metric_name} = {value} (Target: {target}, Trend: {trend})")
