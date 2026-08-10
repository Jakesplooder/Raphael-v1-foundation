import asyncio
import time
import logging
import sys

from raphael_core.kernel.providers.commerce.comfyui_adapter import ComfyUIAdapter
from raphael_core.kernel.models.media_generation import GenerationRequest

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("test_flux")

async def test_flux():
    adapter = ComfyUIAdapter()
    from raphael_core.kernel.models.commerce import AssetType
    import uuid
    req = GenerationRequest(
        request_id=str(uuid.uuid4()),
        mission_id="test-flux",
        business_id="test",
        asset_type=AssetType.PNG,
        prompt="A futuristic neon cyber city at twilight, 8k resolution, highly detailed",
        metadata={"mode": "real", "seed": 424242}
    )
    
    logger.info("Submitting job...")
    job = await adapter.submit(req)
    if job.status.value == "failed":
        logger.error(f"Job submission failed: {job.error_message}")
        sys.exit(1)
        
    job_id = job.job_id
    logger.info(f"Job queued with ID: {job_id}")
    
    start_time = time.time()
    timeout_seconds = 600 # 10 minutes
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout_seconds:
            logger.error("TIMEOUT REACHED (10 minutes). This is likely an OOM or severe swapping thrash, not a code bug. Aborting.")
            sys.exit(1)
            
        result = await adapter.retrieve_outputs(job_id)
        if result.get("status") == "completed":
            logger.info(f"Job Completed! Result: {result}")
            break
        elif result.get("status") == "failed":
            logger.error(f"Job Failed! Result: {result}")
            break
            
        logger.debug(f"Waiting... ({int(elapsed)}s elapsed)")
        await asyncio.sleep(5)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_flux())
