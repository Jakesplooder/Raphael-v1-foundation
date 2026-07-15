from abc import ABC, abstractmethod
from ..models.visual_observation import VisualObservation

class VisionProvider(ABC):
    @abstractmethod
    async def analyze_image(self, image_path: str, context: str) -> VisualObservation:
        pass
