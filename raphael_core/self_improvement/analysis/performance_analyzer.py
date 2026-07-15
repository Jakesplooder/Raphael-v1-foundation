import logging
from typing import Dict, List

logger = logging.getLogger("rrk.self_improvement.analysis")

class PerformanceAnalyzer:
    """Aggregates system-wide component metrics into a self-dashboard."""
    
    def analyze(self, component_scores: Dict[str, float]) -> Dict[str, any]:
        avg = sum(component_scores.values()) / len(component_scores) if component_scores else 0
        weakest = min(component_scores, key=component_scores.get) if component_scores else None
        strongest = max(component_scores, key=component_scores.get) if component_scores else None
        
        return {
            "average_score": round(avg, 2),
            "weakest_component": weakest,
            "weakest_score": component_scores.get(weakest, 0),
            "strongest_component": strongest,
            "strongest_score": component_scores.get(strongest, 0),
            "component_count": len(component_scores),
            "components": component_scores
        }
