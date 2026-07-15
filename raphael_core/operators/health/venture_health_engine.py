import logging
from typing import Dict, Any

logger = logging.getLogger("rrk.operators.health")

class VentureHealthEngine:
    def __init__(self):
        pass

    def analyze(self, kpi_data: Dict[str, Any]) -> Dict[str, Any]:
        revenue_trend = kpi_data.get("revenue_trend", "FLAT")
        cac_trend = kpi_data.get("cac_trend", "FLAT")
        
        if revenue_trend == "NEGATIVE" and cac_trend == "POSITIVE":
            return {
                "state": "WARNING",
                "recommendations": ["Reduce ad spend", "Test new designs", "Investigate onboarding friction"]
            }
        elif revenue_trend == "POSITIVE" and cac_trend in ["FLAT", "NEGATIVE"]:
            return {
                "state": "HEALTHY",
                "recommendations": ["Scale current campaigns", "Expand to adjacent channels"]
            }
        else:
            return {
                "state": "NEUTRAL",
                "recommendations": ["Continue monitoring", "Gather more data"]
            }
