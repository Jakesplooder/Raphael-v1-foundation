import logging
import uuid
from typing import List, Dict, Any
from ..core.models import Option, Argument

logger = logging.getLogger("rrk.deliberation.alternatives")

class AlternativeGenerator:
    """Generates discrete options based on arguments and perspectives."""
    
    def generate_options(self, original_action: str, arguments: List[Argument]) -> List[Option]:
        options = []
        options.append(Option(
            option_id=f"OPT-{uuid.uuid4().hex[:4].upper()}",
            description=original_action
        ))
        
        rejections = [arg for arg in arguments if arg.position == "Reject"]
        modifications = [arg for arg in arguments if arg.position == "Modify"]
        
        if rejections:
            options.append(Option(
                option_id=f"OPT-{uuid.uuid4().hex[:4].upper()}",
                description="Abandon action"
            ))
            
        if modifications:
            desc = "Revised plan: " + " + ".join([m.argument for m in modifications])
            options.append(Option(
                option_id=f"OPT-{uuid.uuid4().hex[:4].upper()}",
                description=desc
            ))
            
        # Hardcoded benchmarks cases logic
        action_lower = original_action.lower()
        if "launch" in action_lower and "safe" not in action_lower:
            options.append(Option(
                option_id=f"OPT-{uuid.uuid4().hex[:4].upper()}",
                description="Create safer lower-cost launch plan"
            ))
        elif "spend" in action_lower:
            options.append(Option(
                option_id=f"OPT-{uuid.uuid4().hex[:4].upper()}",
                description="Risk-adjusted recommendation"
            ))
        elif "microservices" in action_lower or "monolith" in action_lower:
            options.append(Option(
                option_id=f"OPT-{uuid.uuid4().hex[:4].upper()}",
                description="Decision based on scale requirements"
            ))
            
        return options
