from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class VentureThesis:
    """
    Records WHY we believe this company should exist.
    Later Raphael can answer: 'Was our strategy wrong, or was our original assumption wrong?'
    """
    belief: str
    assumptions: List[str]
    risk_assumptions: List[str]
    
    def to_dict(self):
        return {
            "belief": self.belief,
            "assumptions": self.assumptions,
            "risk_assumptions": self.risk_assumptions
        }

@dataclass
class BusinessProposal:
    name: str
    category: str
    type: str
    problem: str
    solution: str
    target_customer: str
    revenue_model: List[str]
    strategic_alignment: Dict[str, bool]
    initial_resources_requested: Dict[str, Any]
    
    # Venture Thesis — WHY this company should exist
    thesis: Optional[VentureThesis] = None
    
    # Internal state
    state: str = "PROPOSED"
    
    def to_dict(self):
        result = {
            "name": self.name,
            "category": self.category,
            "type": self.type,
            "problem": self.problem,
            "solution": self.solution,
            "target_customer": self.target_customer,
            "revenue_model": self.revenue_model,
            "strategic_alignment": self.strategic_alignment,
            "initial_resources_requested": self.initial_resources_requested,
            "state": self.state
        }
        if self.thesis:
            result["thesis"] = self.thesis.to_dict()
        return result
