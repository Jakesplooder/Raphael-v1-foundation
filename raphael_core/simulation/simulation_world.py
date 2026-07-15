from typing import Dict, Any

class SimulationWorld:
    """
    Holds the state of the temporary reality.
    """
    def __init__(self, market: str, competition_level: str, customer_demand: str, starting_capital: float, team: list):
        self.market = market
        self.competition_level = competition_level
        self.customer_demand = customer_demand
        self.capital = starting_capital
        self.team = team
        
        self.current_month = 0
        self.customers_acquired = 0
        self.revenue = 0.0
        self.is_active = True

    def get_state(self) -> Dict[str, Any]:
        return {
            "market": self.market,
            "competition_level": self.competition_level,
            "customer_demand": self.customer_demand,
            "capital": self.capital,
            "team": self.team,
            "current_month": self.current_month,
            "customers_acquired": self.customers_acquired,
            "revenue": self.revenue,
            "is_active": self.is_active
        }
