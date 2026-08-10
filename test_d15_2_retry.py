import asyncio
import logging
import os
import sys
import uuid
import time
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from raphael_core.kernel.event_bus import global_event_bus
from raphael_core.kernel.managers.media_generation_manager import MediaGenerationManager
from raphael_core.kernel.repositories.commerce_repository import CommerceRepository
from raphael_core.kernel.repositories.media_generation_repository import MediaGenerationRepository
from raphael_core.kernel.providers.workflow.image_generation_provider import ImageGenerationProvider

class MockConfig:
    os_root = Path("R:/RalphaelOS_Repo/runtime")

async def run_retry_test():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(message)s")
    logger = logging.getLogger("d15.retry_test")
    
    config = MockConfig()
    commerce_repo = CommerceRepository(config.os_root)
    manager = MediaGenerationManager(global_event_bus, config, commerce_repo)
    
    await global_event_bus.initialize()
    await global_event_bus.start()
    await manager.initialize()
    await manager.start()
    
    # Mock the submit method to fail twice then succeed
    original_submit = manager.image_service.renderer.submit
    fail_count = 0
    
    async def mock_submit(request):
        nonlocal fail_count
        if fail_count < 2:
            fail_count += 1
            raise RuntimeError(f"Simulated network error {fail_count}")
        return await original_submit(request)
        
    manager.image_service.renderer.submit = mock_submit
    
    # We also need generate_asset to handle the initial failure if we want it to retry, 
    # but generate_asset throws immediately if the FIRST submit fails.
    # So actually, patching retrieve_outputs to fail is better for testing the polling retry!
    
    original_retrieve = manager.image_service.renderer.retrieve_outputs
    retrieve_fail_count = 0
    
    async def mock_retrieve(job_id):
        nonlocal retrieve_fail_count
        if retrieve_fail_count < 2:
            retrieve_fail_count += 1
            return {"status": "failed", "error": f"Simulated execution error {retrieve_fail_count}"}
        return await original_retrieve(job_id)
        
    manager.image_service.renderer.retrieve_outputs = mock_retrieve
    manager.image_service.renderer.submit = original_submit # restore

    provider = ImageGenerationProvider(manager.image_service)

    logger.info("Triggering a job designed to fail transiently (simulated execution error)...")
    try:
        result = await provider.execute_step(
            action="generate_asset",
            parameters={
                "mission_id": "TEST-RETRY",
                "business_id": "TEST-BIZ",
                "asset_type": "image",
                "prompt": "A prompt",
                "metadata": {"seed": 1, "model": "none/passthrough"}
            },
            idempotency_key=f"retry-job-{uuid.uuid4().hex[:6]}"
        )
        logger.info(f"Final result: {result}")
    except Exception as e:
        logger.error(f"Provider raised exception: {e}")
        
    await manager.stop()
    await global_event_bus.stop()

if __name__ == "__main__":
    asyncio.run(run_retry_test())
