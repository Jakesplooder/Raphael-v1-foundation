import logging
from typing import List, Dict

logger = logging.getLogger("rrk.business_factory.boards")

class BoardAdvisor:
    def __init__(self, role: str, specialty: str):
        self.role = role
        self.specialty = specialty
        
    def advise(self, context: dict) -> str:
        return f"{self.role} advises based on {self.specialty}"

class VentureBoard:
    """
    Every venture gets a virtual board of advisors.
    Responsibilities: approve scaling, approve shutdown, evaluate strategy.
    """
    
    def __init__(self, venture_id: str):
        self.venture_id = venture_id
        self.advisors = [
            BoardAdvisor("Finance Advisor", "capital_efficiency"),
            BoardAdvisor("Growth Advisor", "market_expansion"),
            BoardAdvisor("Technical Advisor", "architecture"),
            BoardAdvisor("Risk Advisor", "threat_analysis"),
        ]
        
    def evaluate_venture(self, revenue_trend: str, kpi_health: str,
                         market_score: float) -> dict:
        votes = {"SCALE": 0, "CONTINUE": 0, "PIVOT": 0, "SHUTDOWN": 0}
        
        if revenue_trend == "POSITIVE" and kpi_health == "HEALTHY":
            votes["SCALE"] += 3
            votes["CONTINUE"] += 1
        elif revenue_trend == "NEGATIVE" and kpi_health == "WARNING":
            votes["PIVOT"] += 3
            votes["CONTINUE"] += 1
        elif revenue_trend == "CRITICAL":
            votes["SHUTDOWN"] += 4
        else:
            votes["CONTINUE"] += 4
            
        if market_score > 80:
            votes["SCALE"] += 1
        elif market_score < 40:
            votes["SHUTDOWN"] += 1
            
        decision = max(votes, key=votes.get)
        logger.info(f"[VentureBoard] {self.venture_id} decision: {decision} (votes: {votes})")
        return {"decision": decision, "votes": votes}
    
    def allocate_capital(self, ventures: List[Dict]) -> List[Dict]:
        """Predictive ROI-based capital allocation."""
        total_roi = sum(v.get("expected_roi", 0) for v in ventures)
        if total_roi == 0:
            return ventures
            
        for v in ventures:
            roi = v.get("expected_roi", 0)
            v["capital_share"] = round((roi / total_roi) * 100, 1)
            
        ventures.sort(key=lambda x: x["capital_share"], reverse=True)
        logger.info(f"[VentureBoard] Capital allocated across {len(ventures)} ventures by ROI")
        return ventures
