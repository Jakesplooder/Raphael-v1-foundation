import logging
from typing import List, Dict, Any
from ..core.models import MarketSignal, Opportunity

logger = logging.getLogger("rrk.executive.opportunities")

class SignalProcessor:
    def process(self, signals: List[MarketSignal]) -> List[Dict[str, Any]]:
        processed = []
        for sig in signals:
            if sig.confidence > 0.5:
                parsed_topic = sig.category
                parsed_insight = sig.observation
                processed.append({"topic": parsed_topic, "insight": parsed_insight})
        return processed

class OpportunityGenerator:
    def generate(self, insights: List[Dict[str, Any]]) -> List[Opportunity]:
        opportunities = []
        for i in insights:
            if "cybersecurity" in i["topic"].lower():
                opportunities.append(Opportunity(
                    name="SMB Security Assessment Service",
                    market_potential=85.0,
                    strategic_alignment=90.0,
                    capability_fit=80.0,
                    risk=40.0,
                    resource_cost=30.0
                ))
            elif "ai" in i["topic"].lower():
                opportunities.append(Opportunity(
                    name="AI Resume Generator",
                    market_potential=85.0,
                    strategic_alignment=70.0,
                    capability_fit=95.0,
                    risk=20.0,
                    resource_cost=10.0
                ))
        return opportunities

class OpportunityRanker:
    def rank(self, opportunities: List[Opportunity]) -> List[Opportunity]:
        for opp in opportunities:
            opp.final_score = (opp.market_potential + opp.strategic_alignment + opp.capability_fit) - opp.risk - opp.resource_cost
            if opp.final_score > 150:
                opp.recommendation = "Explore"
            else:
                opp.recommendation = "Archive"
                
        # Sort by final score descending
        opportunities.sort(key=lambda x: x.final_score, reverse=True)
        return opportunities
