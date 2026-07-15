import logging
from .vision_events import VisionEventBus
from ..providers.vision_provider import VisionProvider
from ..models.visual_observation import VisualObservation

logger = logging.getLogger("rrk.vision.runtime")

class VisionRuntime:
    def __init__(self, event_bus: VisionEventBus):
        self.event_bus = event_bus
        self.provider = None
        
    def set_provider(self, provider: VisionProvider):
        self.provider = provider
        
    async def process_image(self, image_path: str, context: str) -> VisualObservation:
        if not self.provider:
            raise ValueError("No VisionProvider registered")
            
        observation = await self.provider.analyze_image(image_path, context)
        if observation:
            if observation.confidence.score >= 0.7:
                logger.info(f"Processed image with high confidence: {observation.confidence.score}")
                self.event_bus.publish("VISUAL_ANALYSIS_COMPLETE", observation.model_dump())
            else:
                logger.warning(f"Low confidence visual analysis ({observation.confidence.score}), discarding to prevent unnecessary revisions.")
        return observation
