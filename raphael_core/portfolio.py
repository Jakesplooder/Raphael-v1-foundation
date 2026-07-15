import logging
from typing import List, Dict
from .kernel.storage import KernelStorage
from .kernel.event_bus import emit

storage = KernelStorage()

class PortfolioManager:
    def __init__(self):
        self.domain = "portfolio"

    def register_venture(self, venture_id: str, details: dict):
        portfolio = storage.load(self.domain, "active_portfolio.json") or {}
        portfolio[venture_id] = details
        storage.save(self.domain, "active_portfolio.json", portfolio)
        
        emit("VENTURE_REGISTERED", "PortfolioManager", {"venture_id": venture_id})

    def evaluate_portfolio(self) -> Dict[str, str]:
        portfolio = storage.load(self.domain, "active_portfolio.json") or {}
        results = {}
        for vid in portfolio.keys():
            results[vid] = "Healthy"
        
        emit("PORTFOLIO_EVALUATED", "PortfolioManager", {"results": results})
        return results
