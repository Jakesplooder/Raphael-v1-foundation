import asyncio
import logging

logger = logging.getLogger("rrk.comfyui.adapter")

class ComfyUIAdapter:
    def __init__(self):
        pass

    async def generate_image(self, prompt: str) -> dict:
        """
        Stub for Step 1. Full implementation with cache-busting and path resolution will be in Step 2.
        """
        logger.info(f"Stub generation for: {prompt}")
        await asyncio.sleep(1)
        return {"output_path": "stub/path.png"}
