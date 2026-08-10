import logging
import asyncio

logger = logging.getLogger("rrk.providers.image")

class ImageGenerationProvider:
    def __init__(self):
        # We will fully implement ComfyUIAdapter in Step 2.
        # For now, we stub it to allow MediaGenerationManager to test its queueing logic.
        from ....action.external_connectors.comfyui.comfyui_adapter import ComfyUIAdapter
        self.adapter = ComfyUIAdapter()

    async def generate(self, prompt: str) -> str:
        """
        Generates an image via the adapter and returns the absolute path to the asset.
        """
        logger.info(f"Generating image with prompt: {prompt}")
        result = await self.adapter.generate_image(prompt)
        return result.get("output_path", "")
