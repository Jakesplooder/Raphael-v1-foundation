import logging
from typing import Dict

logger = logging.getLogger("rrk.self_improvement.analysis")

class BottleneckDetector:
    """Identifies the weakest subsystem by comparing against a baseline."""
    
    def __init__(self, baseline_threshold: float = 70.0):
        self.baseline_threshold = baseline_threshold
    
    def detect(self, component_scores: Dict[str, float]) -> list:
        bottlenecks = []
        for component, score in component_scores.items():
            if score < self.baseline_threshold:
                gap = self.baseline_threshold - score
                bottlenecks.append({
                    "component": component,
                    "score": score,
                    "gap": round(gap, 2),
                    "severity": "CRITICAL" if gap > 30 else "HIGH" if gap > 15 else "MEDIUM"
                })
        bottlenecks.sort(key=lambda x: x["gap"], reverse=True)
        logger.info(f"[BottleneckDetector] Found {len(bottlenecks)} bottleneck(s)")
        return bottlenecks
