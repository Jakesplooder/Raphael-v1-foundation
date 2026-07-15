import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("rrk.services.commerce.capability_registry")

class ProductCapabilityRegistry:
    """
    Decouples Commerce from specific execution providers like Builder or AI.
    Maps an artifact or product generation need to the correct Provider capability.
    """
    def __init__(self):
        self.capability_map = {
            "ebook": "AIProvider",
            "notion_template": "TemplateProvider",
            "software": "BuilderProvider",
            "shirt_design": "ComfyUIProvider",
            "mockup": "MockupProvider",
            "seo": "AIProvider",
            "listing": "ListingProvider",
            "packaging": "FilesystemProvider"
        }
        
    def get_provider_for(self, artifact_type: str) -> str:
        """Returns the appropriate provider for generating a specific artifact."""
        provider = self.capability_map.get(artifact_type.lower())
        if not provider:
            logger.warning(f"No specific capability registered for '{artifact_type}', falling back to AIProvider.")
            return "AIProvider"
        return provider
