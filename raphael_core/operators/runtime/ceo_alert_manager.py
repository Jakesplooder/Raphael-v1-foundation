import logging
from ...world.world_events import WorldEventBus

logger = logging.getLogger("rrk.operators.alerts")

class CEOAlertManager:
    def __init__(self, world_bus: WorldEventBus):
        self.world_bus = world_bus
        self.world_bus.subscribe("COMPETITOR_THREAT", self.handle_threat)
        self.active_alerts = []
        
    def handle_threat(self, payload: dict):
        logger.info(f"[CEOAlertManager] Routing threat to CEO: {payload['content']}")
        alert = {
            "target": "SaaSCEO" if "SaaS" in payload['content'] else "CybersecurityCEO",
            "type": "COMPETITOR_THREAT",
            "content": payload['content'],
            "severity": "HIGH"
        }
        self.active_alerts.append(alert)
