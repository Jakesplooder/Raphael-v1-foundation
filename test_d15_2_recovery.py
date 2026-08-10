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
from raphael_core.kernel.models.media_generation import GenerationJob, GenerationRequest, GenerationStatus

class MockConfig:
    os_root = Path("R:/RalphaelOS_Repo/runtime")

async def test_recovery():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("d15.recovery")
    
    config = MockConfig()
    commerce_repo = CommerceRepository(config.os_root)
    media_repo = MediaGenerationRepository(config.os_root)
    
    # 1. Inject a stalled job into the DB
    stalled_job_id = f"RECOVER-{uuid.uuid4().hex[:6].upper()}"
    stalled_req = GenerationRequest(
        request_id="test-recovery-req",
        asset_type="image",
        prompt="A lost asset",
        metadata={"model": "none/passthrough"}
    )
    stalled_job = GenerationJob(
        job_id=stalled_job_id,
        request=stalled_req,
        status=GenerationStatus.QUEUED,
        started_at=time.time() - 1000 # Started a long time ago
    )
    media_repo.upsert_job(stalled_job)
    logger.info(f"Injected stalled job {stalled_job_id} into MediaGenerationRepository")
    
    # 2. Start Manager
    manager = MediaGenerationManager(global_event_bus, config, commerce_repo)
    await global_event_bus.initialize()
    await global_event_bus.start()
    await manager.initialize()
    
    logger.info("Starting MediaGenerationManager (should trigger recovery)...")
    await manager.start()
    
    # Check if job was loaded into active_jobs
    if stalled_job_id in manager.image_service.active_jobs:
        logger.info(f"SUCCESS: Job {stalled_job_id} was successfully loaded into active_jobs on startup!")
    else:
        logger.error(f"FAILURE: Job {stalled_job_id} was NOT loaded!")
        
    metrics = await manager.metrics()
    logger.info(f"Manager Metrics: {metrics}")
    
    # Note: We won't actually wait for the adapter to pick it up in this quick test since it's just queued, 
    # but the service loaded it.
    await manager.stop()
    await global_event_bus.stop()

if __name__ == "__main__":
    asyncio.run(test_recovery())
