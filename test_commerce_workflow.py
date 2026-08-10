import asyncio
import logging
import uuid
import sys

from raphael_core.kernel.event_bus import EventBus
from raphael_core.kernel.models.workflow_plan import (
    WorkflowTemplate, WorkflowPhase, WorkflowStep, StepStatus, WorkflowStatus
)
from raphael_core.kernel.managers.workflow_plan_manager import WorkflowPlanManager
from raphael_core.kernel.managers.media_generation_manager import MediaGenerationManager
from raphael_core.kernel.managers.commerce_manager import CommerceManager
from raphael_core.kernel.providers.workflow.image_generation_provider import ImageGenerationProvider
from raphael_core.config import RaphaelConfig
from raphael_core.kernel.interfaces import Event, EventType
from raphael_core.kernel.models.media_generation import GenerationJob, GenerationStatus

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("test_commerce_workflow")

from pathlib import Path

class MockConfig:
    os_root = Path("R:/RalphaelOS_Repo/runtime")
    vault = Path("R:/RalphaelOS_Repo/runtime/vault")
    def __getattr__(self, name):
        return None

async def test_golden_path():
    logger.info("=== Starting Test: Golden Path ===")
    config = MockConfig()
    
    # Clean up old test data
    import shutil
    if config.vault.exists():
        shutil.rmtree(config.vault, ignore_errors=True)
        
    bus = EventBus()
    await bus.initialize()
    await bus.start()
    
    from raphael_core.kernel.repositories.commerce_repository import CommerceRepository
    commerce_repo = CommerceRepository(config.os_root)
    media = MediaGenerationManager(bus, config, commerce_repo)
    await media.initialize()
    await media.start()
    
    workflow = WorkflowPlanManager(config)
    await workflow.initialize(event_bus=bus)
    
    provider = ImageGenerationProvider(media.image_service)
    workflow.registry.register(provider)
    
    await workflow.start()
    
    # Create Template
    step1 = WorkflowStep(
        step_id="step_gen",
        name="Generate Asset",
        action="generate_asset",
        required_capabilities=["ImageGenerationService"],
        parameters={"prompt": "A cute cat"}
    )
    step2 = WorkflowStep(
        step_id="step_upscale",
        name="Upscale Asset",
        action="generate_asset",
        dependencies=["step_gen"],
        required_capabilities=["ImageGenerationService"],
        parameters={"prompt": "upscale", "parent_asset_id": "${step_gen.result.asset_id}"}
    )
    
    template = WorkflowTemplate(
        template_id="tpl_linear",
        name="Linear Campaign",
        phases={"phase1": WorkflowPhase(phase_id="phase1", name="Phase 1", steps={"step_gen": step1, "step_upscale": step2})}
    )
    
    # Trigger workflow
    await bus.publish(Event(
        source="test",
        type=EventType.WORKFLOW_PLAN_REQUESTED,
        payload={"template": template.model_dump()}
    ))
    
    # Wait for completion
    for _ in range(30):
        await asyncio.sleep(1)
        plans = workflow.repository.list_plans("Running") + workflow.repository.list_plans("Completed")
        if not plans: continue
        plan = plans[0]
        logger.debug(f"Plan status: {plan.status}. Queue: {workflow.status()}")
        
        # Check Step 1
        s1 = plan.phases["phase1"].steps["step_gen"]
        s2 = plan.phases["phase1"].steps["step_upscale"]
        
        if s1.status == StepStatus.COMPLETED and s2.status == StepStatus.COMPLETED:
            logger.info("Both steps completed successfully!")
            
            # Assert parameter resolution
            assert s2.result.get("asset_id") is not None
            
            repo = media.image_service.commerce_repo
            asset1 = repo.get_asset(s1.result["asset_id"])
            asset2 = repo.get_asset(s2.result["asset_id"])
            
            assert asset1.version == 1
            assert asset2.version == 2
            assert asset2.parent_asset_id == asset1.asset_id
            logger.info("Versioning verified correctly.")
            break
            
    await workflow.stop()
    await media.stop()
    await bus.stop()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_golden_path())
