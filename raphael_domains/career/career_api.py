from typing import Dict, Any
import logging

from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore

from .career_twin import get_career_twin, record_skill_acquisition
from .opportunity_engine import score_opportunity
from .market_intelligence import fetch_market_signals

logger = logging.getLogger("career.api")

class CareerAPI:
    """
    External API gateway for the Career Domain.
    All external operations MUST be wrapped in IdempotencyStore.
    """
    
    def __init__(self, config: Any):
        self.config = config
        self.idempotency_store = IdempotencyStore()

    def executive_brief(self, request_id: str, person_id: str) -> Dict[str, Any]:
        """
        Generates an executive brief for a person.
        Wrapped with idempotency to handle client retries safely.
        """
        idempotency_key = f"exec_brief_{request_id}_{person_id}"
        
        # 1. Idempotency Check
        existing_result = self.idempotency_store.get(idempotency_key)
        if existing_result:
            logger.info(f"[IDEMPOTENCY] Executive brief {idempotency_key} already generated. Returning cached.")
            return existing_result
            
        try:
            # 2. Fetch the Twin (Rule 1: Graph Traversal)
            twin = get_career_twin(self.config, person_id)
            
            # 3. Optional: Trigger a market intelligence fetch if needed
            # For demonstration, we fetch market signals dynamically
            fetch_market_signals("latest containerization trends", idempotency_key=f"market_fetch_{request_id}")
            
            # 4. Fetch Opportunities (Rule 2: Semantic Discovery)
            # In a real scenario, this uses the skills from the twin to formulate a query.
            skills = ", ".join([s["name"] for s in twin.get("skills", [])])
            query = f"roles requiring {skills}"
            opportunities = score_opportunity(self.config, twin, query)
            
            # 5. Assemble Payload
            payload = {
                "request_id": request_id,
                "person_id": person_id,
                "career_twin": twin,
                "top_opportunities": opportunities[:3]
            }
            
            # 6. Store Result
            self.idempotency_store.set(idempotency_key, payload)
            
            return payload
            
        except Exception as e:
            logger.error(f"Failed to generate executive brief: {e}")
            raise
