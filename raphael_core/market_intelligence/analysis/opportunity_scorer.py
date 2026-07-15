class OpportunityScorer:
    """
    Calculates the Opportunity Intelligence Score (OIS).
    OIS = 20% Growth + 20% Demand + 15% Gap + 15% Feasibility + 10% Profit + 10% Alignment + 10% Historical Success
    """
    def __init__(self):
        self.weights = {
            "market_growth": 0.20,
            "customer_demand": 0.20,
            "competition_gap": 0.15,
            "technical_feasibility": 0.15,
            "profit_potential": 0.10,
            "strategic_alignment": 0.10,
            "historical_success": 0.10
        }

    def calculate_ois(self, metrics: dict) -> float:
        score = 0.0
        for key, weight in self.weights.items():
            value = metrics.get(key, 50) # Default to average 50 if missing
            score += (value * weight)
        return round(score, 2)
