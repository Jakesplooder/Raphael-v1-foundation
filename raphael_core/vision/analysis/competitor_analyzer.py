from ..models.visual_observation import VisualObservation

class CompetitorAnalyzer:
    def __init__(self):
        pass
        
    def extract_patterns(self, obs: VisualObservation) -> dict:
        return {
            "pricing_tiers": obs.findings.get("pricing_tiers", []),
            "ui_patterns": obs.findings.get("ui_patterns", []),
            "ux_weaknesses": obs.findings.get("ux_weaknesses", [])
        }
