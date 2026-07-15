from .vision_provider import VisionProvider
from ..models.visual_observation import VisualObservation

class MockVisionProvider(VisionProvider):
    def __init__(self):
        self.mocked_responses = {}
        
    def inject_response(self, image_path: str, response: VisualObservation):
        self.mocked_responses[image_path] = response
        
    async def analyze_image(self, image_path: str, context: str) -> VisualObservation:
        return self.mocked_responses.get(image_path, None)
