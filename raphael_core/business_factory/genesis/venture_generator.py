import logging
from .venture_blueprint import VentureBlueprint
from ..lifecycle.venture_lifecycle import VentureLifecycle, VentureState

logger = logging.getLogger("rrk.business_factory.genesis")

class VentureGenerator:
    """Turns validated opportunities into venture blueprints."""
    
    def __init__(self, lifecycle: VentureLifecycle):
        self.lifecycle = lifecycle
        self._next_id = 1
        
    def generate(self, opportunity_name: str, venture_type: str,
                 market_score: float, confidence: float,
                 opportunity_source: str = "WorldModel") -> VentureBlueprint:
        
        venture_id = f"VENTURE-{self._next_id:03d}"
        self._next_id += 1
        
        # Determine CEO type from venture type
        ceo_map = {
            "SaaS": "SaaSCEO",
            "Cybersecurity": "CybersecurityCEO",
            "POD": "PODBrandCEO",
            "Agency": "AgencyCEO",
            "Media": "MediaCEO",
        }
        ceo_type = ceo_map.get(venture_type, "SaaSCEO")
        
        # Determine initial departments
        dept_map = {
            "SaaS": ["Engineering", "Marketing", "Sales"],
            "Cybersecurity": ["Engineering", "Sales", "Operations"],
            "POD": ["Marketing", "Operations"],
            "Agency": ["Marketing", "Sales", "Operations"],
        }
        departments = dept_map.get(venture_type, ["Engineering", "Marketing"])
        
        blueprint = VentureBlueprint(
            venture_id=venture_id,
            name=opportunity_name.replace(" ", ""),
            venture_type=venture_type,
            ceo_type=ceo_type,
            initial_departments=departments,
            market_score=market_score,
            confidence=confidence,
            initial_capital=market_score * confidence * 100,
            opportunity_source=opportunity_source
        )
        
        self.lifecycle.register(venture_id)
        self.lifecycle.transition(venture_id, VentureState.CREATED)
        
        logger.info(f"[VentureGenerator] Created {venture_id}: {blueprint.name} "
                     f"(CEO: {ceo_type}, Depts: {departments})")
        return blueprint
