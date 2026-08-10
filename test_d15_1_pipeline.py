import asyncio
import logging
import os
import sys

# Configure path so we can import from raphael_core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from raphael_core.kernel.event_bus import global_event_bus
from raphael_core.kernel.interfaces import EventType
from raphael_core.kernel.repositories.commerce_repository import CommerceRepository
from raphael_core.kernel.managers.media_generation_manager import MediaGenerationManager
from raphael_core.kernel.providers.workflow.image_generation_provider import ImageGenerationProvider

from pathlib import Path

class MockConfig:
    os_root = Path("R:/RalphaelOS_Repo/runtime")
    
async def run_end_to_end_test():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("d15.test")
    
    config = MockConfig()
    commerce_repo = CommerceRepository(config.os_root)
    
    manager = MediaGenerationManager(
        event_bus=global_event_bus,
        config=config,
        commerce_repo=commerce_repo
    )
    
    await global_event_bus.initialize()
    await global_event_bus.start()
    await manager.initialize()
    await manager.start()
    
    # Listen to events to verify Matrix updates
    events_received = []
    async def event_listener(event):
        logger.info(f"Received Event: {event.type} - {event.payload}")
        events_received.append(event.type)
        
    global_event_bus.subscribe(EventType.JOB_STARTED, event_listener)
    global_event_bus.subscribe(EventType.JOB_PROGRESS, event_listener)
    global_event_bus.subscribe(EventType.ASSET_GENERATED, event_listener)
    
    logger.info("Triggering Image Generation via Workflow Provider...")
    provider = ImageGenerationProvider(manager.image_service)
    
    try:
        result = await provider.execute_step(
            action="generate_asset",
            parameters={
                "mission_id": "TEST-MISSION-1",
                "business_id": "TEST-BIZ-1",
                "asset_type": "shirt_design",
                "prompt": "A cool cyberpunk aesthetic t-shirt design with neon lights, highly detailed",
                "metadata": {"seed": 42, "model": "flux1-schnell"}
            },
            idempotency_key="test-job-123"
        )
        logger.info(f"Provider returned: {result}")
        
        # Verify events
        assert EventType.JOB_STARTED in events_received, "Failed to emit JOB_STARTED"
        assert EventType.ASSET_GENERATED in events_received, "Failed to emit ASSET_GENERATED"
        
        logger.info("End-to-End Test Passed!")
    except Exception as e:
        logger.error(f"Test failed: {e}")
        
    finally:
        await manager.stop()
        await global_event_bus.stop()

if __name__ == "__main__":
    asyncio.run(run_end_to_end_test())
