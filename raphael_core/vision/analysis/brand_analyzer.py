from ..models.visual_observation import VisualObservation

class BrandAnalyzer:
    def __init__(self):
        pass
        
    def analyze(self, obs: VisualObservation, brand_guidelines: dict) -> dict:
        is_aligned = obs.findings.get("brand_alignment", 0) >= 0.8
        return {
            "is_aligned": is_aligned,
            "violations": obs.findings.get("brand_violations", [])
        }
