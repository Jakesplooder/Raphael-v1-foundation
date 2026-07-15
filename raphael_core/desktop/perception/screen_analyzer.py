import logging

logger = logging.getLogger("rrk.desktop.perception")

class ScreenAnalyzer:
    """Feeds screenshots into the Vision pipeline for UI grounding."""
    
    def analyze(self, screen_state: dict) -> dict:
        elements = screen_state.get("elements", [])
        return {
            "buttons": [e for e in elements if e.get("type") == "button"],
            "inputs": [e for e in elements if e.get("type") == "input"],
            "navigation": [e for e in elements if e.get("type") == "nav"],
            "element_count": len(elements)
        }
