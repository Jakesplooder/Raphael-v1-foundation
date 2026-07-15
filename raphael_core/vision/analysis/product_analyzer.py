from ..models.visual_observation import VisualObservation

class ProductAnalyzer:
    def __init__(self):
        pass
        
    def evaluate(self, obs: VisualObservation) -> dict:
        return {
            "composition_score": obs.findings.get("composition_score", 0),
            "emotional_appeal": obs.findings.get("emotional_appeal", "neutral"),
            "defects_detected": obs.findings.get("defects", [])
        }
