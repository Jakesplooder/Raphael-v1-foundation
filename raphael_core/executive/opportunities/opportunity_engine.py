import logging
from ...world.world_events import WorldEventBus
from ..core.models import Opportunity

logger = logging.getLogger("rrk.executive.opportunities")

class OpportunityEngine:
    def __init__(self, world_bus: WorldEventBus):
        self.world_bus = world_bus
        self.world_bus.subscribe("OPPORTUNITY_SIGNAL", self.handle_signal)
        self.world_bus.subscribe("MARKET_TREND_DETECTED", self.handle_trend)
        self.detected_opportunities = []
        
    def handle_signal(self, payload: dict):
        logger.info(f"[OpportunityEngine] Processing world signal: {payload['content']}")
        if "AI adoption" in payload['content'] and "Healthcare compliance" in payload['content']:
            opp = Opportunity(
                name="Healthcare AI Compliance SaaS",
                market_potential=85,
                strategic_alignment=90,
                capability_fit=80,
                risk=30,
                resource_cost=40,
                final_score=85,
                recommendation="EXPLORE"
            )
            self.detected_opportunities.append(opp)
            
    def handle_trend(self, payload: dict):
        logger.info(f"[OpportunityEngine] Processing market trend: {payload['content']}")
        if "Cybersecurity regulations" in payload['content']:
            opp = Opportunity(
                name="Cybersecurity Compliance Automation",
                market_potential=95,
                strategic_alignment=90,
                capability_fit=90,
                risk=20,
                resource_cost=30,
                final_score=85,
                recommendation="EXPLORE"
            )
            self.detected_opportunities.append(opp)
