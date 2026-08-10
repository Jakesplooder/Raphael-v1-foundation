import logging
from typing import Dict, Any, List

logger = logging.getLogger("rrk.councils.router")

class CouncilRouter:
    """Routes proposals to the relevant councils based on severity and impact."""
    
    def __init__(self, registry):
        self.registry = registry
        
    def determine_route(self, action_id: str, proposal: Dict[str, Any], previous_decision=None) -> List[Any]:
        # Mode 3: Full Governance Review (CRITICAL)
        if proposal.get("severity") == "CRITICAL" or (previous_decision and previous_decision.severity == "CRITICAL"):
            return self.registry.get_all_councils()
            
        # If this is a re-review (Revision)
        if previous_decision:
            if previous_decision.severity == "LOW":
                # Mode 1: Targeted Review
                return [self.registry.get_council(previous_decision.council)]
            else:
                # Mode 2: Impact Review (Original + Impacted)
                required_names = set(previous_decision.re_review_required)
                required_names.add(previous_decision.council)
                return [self.registry.get_council(name) for name in required_names if self.registry.get_council(name)]
                
        # Initial routing based on intent
        intent = proposal.get("intent", "").lower()
        councils = []
        if "software" in intent or "app" in intent or "api" in intent:
            councils.append(self.registry.get_council("Architecture Council"))
            councils.append(self.registry.get_council("Security Council"))
        if "brand" in intent or "product" in intent or "shirt" in intent:
            councils.append(self.registry.get_council("Commerce Council"))
            councils.append(self.registry.get_council("Brand Council"))
        if "spend" in intent or "ads" in intent or "company" in intent:
            councils.append(self.registry.get_council("Finance Council"))
            
        # Ensure we don't return Nones if registry lookup fails
        return [c for c in councils if c]
