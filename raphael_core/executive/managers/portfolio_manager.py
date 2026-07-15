import logging
from typing import Dict, List, Optional
from ..core.models import Venture, VentureStage

logger = logging.getLogger("rrk.executive.portfolio")

class PortfolioManager:
    def __init__(self):
        self.ventures: Dict[str, Venture] = {}
        
    def register_venture(self, venture: Venture):
        self.ventures[venture.name] = venture
        logger.info(f"Registered venture: {venture.name} at stage {venture.stage}")
        
    def update_venture_stage(self, name: str, new_stage: VentureStage):
        if name in self.ventures:
            self.ventures[name].stage = new_stage
            logger.info(f"Venture {name} progressed to {new_stage}")
            
    def allocate_agent(self, venture_name: str, agent_id: str):
        if venture_name in self.ventures:
            self.ventures[venture_name].agents_assigned.append(agent_id)
            logger.info(f"Allocated agent {agent_id} to {venture_name}")
            
    def allocate_capital(self, requests: list, available_resources: dict) -> dict:
        """
        Allocates capital/resources based on the Portfolio Value of each request.
        """
        allocations = {req.venture_id: 0.0 for req in requests}
        for resource_type, total_amount in available_resources.items():
            type_requests = [r for r in requests if r.resource_type == resource_type]
            # Sort by portfolio value descending
            type_requests.sort(key=lambda x: x.portfolio_value(), reverse=True)
            
            remaining = total_amount
            for req in type_requests:
                if remaining <= 0:
                    break
                allocation = min(req.amount, remaining)
                allocations[req.venture_id] += allocation
                remaining -= allocation
                
        return allocations
            
    def get_portfolio_health(self) -> float:
        if not self.ventures:
            return 100.0
        return sum(v.health_score for v in self.ventures.values()) / len(self.ventures)
