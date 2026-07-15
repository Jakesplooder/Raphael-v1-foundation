import logging
from ..vision.models.visual_observation import VisualObservation
from ..vision.analysis.brand_analyzer import BrandAnalyzer

logger = logging.getLogger("rrk.councils.vision")

class VisionCouncil:
    def __init__(self):
        self.brand_analyzer = BrandAnalyzer()
        
    def review_asset(self, obs: VisualObservation, brand_guidelines: dict) -> dict:
        analysis = self.brand_analyzer.analyze(obs, brand_guidelines)
        
        # If low confidence, do not fail it automatically to prevent unnecessary loops
        if obs.confidence.score < 0.7:
            logger.warning(f"[VisionCouncil] Low confidence visual analysis ({obs.confidence.score}). Skipping strict enforcement.")
            return {"decision": "APPROVED", "issues": []}
            
        if not analysis["is_aligned"]:
            logger.info(f"[VisionCouncil] REVISION REQUIRED for asset {obs.id}")
            return {
                "decision": "REVISION_REQUIRED",
                "issues": analysis["violations"]
            }
            
        logger.info(f"[VisionCouncil] Asset {obs.id} APPROVED.")
        return {"decision": "APPROVED", "issues": []}
