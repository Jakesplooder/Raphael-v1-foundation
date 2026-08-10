import asyncio
import logging
import sys
from fastapi.testclient import TestClient

from raphael_core.kernel.event_bus import EventBus
from raphael_core.kernel.managers.workflow_plan_manager import WorkflowPlanManager
from raphael_core.kernel.managers.media_generation_manager import MediaGenerationManager
from raphael_core.kernel.providers.workflow.image_generation_provider import ImageGenerationProvider
from raphael_core.kernel.dashboard import KernelDashboard
from raphael_core.kernel.registry import registry
from raphael_core.config import RaphaelConfig
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("test_chat_workflow")

class MockConfig:
    os_root = Path("R:/RalphaelOS_Repo/runtime")
    vault = Path("R:/RalphaelOS_Repo/runtime/vault")
    def __getattr__(self, name):
        return None

async def test_chat_trigger():
    logger.info("=== Starting Test: Chat Trigger ===")
    config = MockConfig()
    
    # Initialize components
    from raphael_core.kernel.event_bus import EventBus
    bus = EventBus()
    await bus.initialize()
    await bus.start()
    
    from raphael_core.kernel.repositories.commerce_repository import CommerceRepository
    commerce_repo = CommerceRepository(config.os_root)
    media = MediaGenerationManager(bus, config, commerce_repo)
    await media.initialize()
    await media.start()
    
    workflow = WorkflowPlanManager(bus, config)
    await workflow.initialize()
    
    provider = ImageGenerationProvider(media.image_service)
    workflow.registry.register(provider)
    
    await workflow.start()
    
    # Patch global_event_bus so dashboard uses our loop-bound instance
    import raphael_core.kernel.dashboard as dash_mod
    dash_mod.global_event_bus = bus
    import raphael_core.kernel.event_bus as eb_mod
    eb_mod.global_event_bus = bus
    
    # Setup dashboard
    dashboard = KernelDashboard()
    dashboard.app.state.event_bus = bus
    
    # Send mock message by directly calling the intent handler
    class DummyPayload:
        def __init__(self, prompt):
            self.prompt = prompt
            
    logger.info("Sending chat request by calling handle_intent directly...")
    # Find the handle_intent function from the router
    handle_intent = None
    for route in dashboard.app.routes:
        if route.path == "/api/intent" and "POST" in route.methods:
            handle_intent = route.endpoint
            break
            
    assert handle_intent is not None
    # Provide a mock request object
    class MockRequest:
        class State:
            def __init__(self):
                self.event_bus = bus
        def __init__(self):
            self.app = type("App", (), {"state": self.State()})()
            
    response_data = await handle_intent(DummyPayload(prompt="generate an image of a cyberpunk city"), MockRequest())
    logger.info(f"Chat response: {response_data}")
    assert response_data["intent"] == "execute"
    assert response_data["command"] == "generate_asset"
    
    # Wait for completion
    found_job = False
    for _ in range(10):
        await asyncio.sleep(1)
        if bus._worker_task.done():
            logger.error(f"EventBus worker task died! Exception: {bus._worker_task.exception()}")
        plans = workflow.repository.list_plans("Running") + workflow.repository.list_plans("Completed")
        if plans:
            plan = plans[0]
            logger.info(f"Found plan in persistence layer: {plan.plan_id}, status={plan.status}")
            found_job = True
            
            # Check if ImageGenerationService picked it up
            if plan.status == "completed":
                s1 = plan.phases["phase1"].steps["step_gen"]
                assert s1.result.get("asset_id") is not None
                logger.info("Job successfully completed in ImageGenerationService!")
                break
    
    if not found_job:
        logger.error("No job was created in the persistence layer!")
        raise RuntimeError("Test Failed: WorkflowPlanManager never received the request.")
            
    await workflow.stop()
    await media.stop()
    await bus.stop()
    logger.info("Test passed.")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_chat_trigger())
