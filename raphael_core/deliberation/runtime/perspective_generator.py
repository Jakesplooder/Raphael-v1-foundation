import logging
from typing import List, Dict, Any
from ..core.models import Argument

logger = logging.getLogger("rrk.deliberation.perspectives")

class PerspectiveGenerator:
    """Generates creative and strategic perspectives to inject into deliberation."""
    
    def generate_perspectives(self, conflict_context: Dict[str, Any], goals: List[str]) -> List[Argument]:
        perspectives = []
        task = conflict_context.get("task", "").lower()
        
        if "launch" in task or "growth" in task or "acquire" in task or "spend" in task:
            perspectives.append(Argument(
                source="Growth Perspective",
                position="Support",
                argument="Delaying or canceling costs significant market opportunity.",
                evidence=[f"Goal alignment: {goals[0] if goals else 'Growth'}"],
                confidence=0.85,
                priority="HIGH"
            ))
            
        if "expense" in task or "spend" in task or "acquire" in task:
            perspectives.append(Argument(
                source="Finance Perspective",
                position="Modify",
                argument="High cost is acceptable only if ROI timeline is < 6 months.",
                evidence=[],
                confidence=0.90,
                priority="MEDIUM"
            ))
            
        return perspectives
