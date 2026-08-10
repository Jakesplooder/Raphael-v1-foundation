import asyncio
import logging
import uuid
import sys
import shutil
from pathlib import Path

from raphael_core.kernel.event_bus import EventBus
from raphael_core.kernel.models.workflow_plan import (
    WorkflowTemplate, WorkflowPhase, WorkflowStep, StepStatus, WorkflowStatus
)
from raphael_core.kernel.managers.workflow_plan_manager import WorkflowPlanManager
from raphael_core.kernel.managers.media_generation_manager import MediaGenerationManager
from raphael_core.kernel.providers.workflow.image_generation_provider import ImageGenerationProvider
from raphael_core.kernel.repositories.commerce_repository import CommerceRepository
from raphael_core.kernel.interfaces import Event, EventType

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("test_edge_cases")

class MockConfig:
    os_root = Path("R:/RalphaelOS_Repo/runtime")
    vault = Path("R:/RalphaelOS_Repo/runtime/vault")
    def __getattr__(self, name):
        return None

async def setup_environment():
    config = MockConfig()
    if config.vault.exists():
        shutil.rmtree(config.vault, ignore_errors=True)
        
    bus = EventBus()
    await bus.initialize()
    await bus.start()
    
    commerce_repo = CommerceRepository(config.os_root)
    media = MediaGenerationManager(bus, config, commerce_repo)
    await media.initialize()
    await media.start()
    
    # Mock renderer.submit so it doesn't fail connecting to ComfyUI
    import time
    from raphael_core.kernel.models.media_generation import GenerationJob, GenerationStatus
    async def mock_submit(request):
        return GenerationJob(
            job_id=f"mock-{uuid.uuid4().hex[:8]}",
            request=request,
            status=GenerationStatus.RUNNING,
            started_at=time.time(),
            telemetry={}
        )
    media.image_service.renderer.submit = mock_submit
    
    async def global_mock_retrieve(job_id):
        return {"status": "completed", "images": [{"filename": "mock.png"}], "duration": 1.0, "model_name": "mock"}
    media.image_service.renderer.retrieve_outputs = global_mock_retrieve
    
    workflow = WorkflowPlanManager(config)
    await workflow.initialize(event_bus=bus)
    
    provider = ImageGenerationProvider(media.image_service)
    workflow.registry.register(provider)
    
    await workflow.start()
    return bus, media, workflow

def create_linear_template(test_name: str) -> WorkflowTemplate:
    step1 = WorkflowStep(
        step_id="step_gen",
        name="Generate Asset",
        action="generate_asset",
        required_capabilities=["ImageGenerationService"],
        parameters={"prompt": f"{test_name} - generate"}
    )
    step2 = WorkflowStep(
        step_id="step_upscale",
        name="Upscale Asset",
        action="generate_asset",
        dependencies=["step_gen"],
        required_capabilities=["ImageGenerationService"],
        parameters={"prompt": f"{test_name} - upscale", "parent_asset_id": "${step_gen.result.asset_id}"}
    )
    return WorkflowTemplate(
        template_id=f"tpl_{test_name}",
        name=f"Template {test_name}",
        phases={"phase1": WorkflowPhase(phase_id="phase1", name="Phase 1", steps={"step_gen": step1, "step_upscale": step2})}
    )

def create_parallel_template(test_name: str) -> WorkflowTemplate:
    step1 = WorkflowStep(
        step_id="step_quick_fail",
        name="Fail Fast",
        action="generate_asset",
        required_capabilities=["ImageGenerationService"],
        parameters={"prompt": f"{test_name} - fail_fast"}
    )
    step2 = WorkflowStep(
        step_id="step_slow",
        name="Slow Step",
        action="generate_asset",
        required_capabilities=["ImageGenerationService"],
        parameters={"prompt": f"{test_name} - slow"}
    )
    return WorkflowTemplate(
        template_id=f"tpl_{test_name}",
        name=f"Template {test_name}",
        phases={"phase1": WorkflowPhase(phase_id="phase1", name="Phase 1", steps={"step_quick_fail": step1, "step_slow": step2})}
    )

async def test_guard_trigger():
    logger.info("=== Starting Test: Guard Trigger ===")
    bus, media, workflow = await setup_environment()
    
    # Mock retrieve_outputs so it returns an unverified asset
    original_retrieve = media.image_service.renderer.retrieve_outputs
    async def mock_retrieve(job_id):
        result = await original_retrieve(job_id)
        if result["status"] == "completed":
            pass
        return result
        
    original_get_asset = media.image_service.commerce_repo.get_asset
    def mock_get_asset(asset_id):
        asset = original_get_asset(asset_id)
        if asset:
            asset.is_verified = False
        return asset
    media.image_service.commerce_repo.get_asset = mock_get_asset
    # We already have a global mock for retrieve_outputs, but wait!
    # I can just remove this local mock since I made it global!
    # Or keep it as `retrieve_outputs` just to be safe.
    original_retrieve = media.image_service.renderer.retrieve_outputs
    async def mock_retrieve(job_id):
        return {"status": "completed", "images": [{"filename": "mock.png"}], "duration": 1.0, "model_name": "mock"}
    media.image_service.renderer.retrieve_outputs = mock_retrieve
    
    template = create_linear_template("guard")
    await bus.publish(Event(source="test", type=EventType.WORKFLOW_PLAN_REQUESTED, payload={"template": template.model_dump()}))
    
    plan_failed = False
    step2_dispatched = False
    for _ in range(30):
        await asyncio.sleep(1)
        plans = workflow.repository.list_plans("Running") + workflow.repository.list_plans("Archived") + workflow.repository.list_plans("Completed") + workflow.repository.list_plans("Failed")
        if not plans: continue
        plan = plans[0]
        
        s1 = plan.phases["phase1"].steps["step_gen"]
        s2 = plan.phases["phase1"].steps["step_upscale"]
        
        if s2.status in (StepStatus.STARTED, StepStatus.COMPLETED):
            step2_dispatched = True
            
        if plan.status == WorkflowStatus.FAILED:
            plan_failed = True
            assert s1.status == StepStatus.FAILED
            assert s2.status == StepStatus.PENDING
            break
            
    assert plan_failed, "Plan did not fail upon guard trigger"
    assert not step2_dispatched, "Step 2 was dispatched despite guard failure in Step 1"
    logger.info("Guard Trigger test passed!")
    
    media.image_service.commerce_repo.get_asset = original_get_asset
    media.image_service.renderer.retrieve_outputs = original_retrieve
    await workflow.stop()
    await media.stop()
    await bus.stop()

async def test_retry_recovery():
    logger.info("=== Starting Test: Retry Recovery ===")
    bus, media, workflow = await setup_environment()
    
    # Actually, we need to bypass the renderer throwing immediately if not running,
    # or mock it precisely. By replacing retrieve_outputs, we only simulate failing
    # during the polling. But generate_asset throws if submit throws.
    # The previous test mocked retrieve_outputs successfully.
    
    original_retrieve = media.image_service.renderer.retrieve_outputs
    fail_count = 0
    async def mock_retrieve(job_id):
        nonlocal fail_count
        if fail_count < 1:
            fail_count += 1
            return {"status": "failed", "error": "Simulated transient failure"}
        return await original_retrieve(job_id)
    media.image_service.renderer.retrieve_outputs = mock_retrieve
    
    template = create_linear_template("retry")
    await bus.publish(Event(source="test", type=EventType.WORKFLOW_PLAN_REQUESTED, payload={"template": template.model_dump()}))
    
    plan_completed = False
    for _ in range(30):
        await asyncio.sleep(1)
        plans = workflow.repository.list_plans("Running") + workflow.repository.list_plans("Completed")
        if not plans: continue
        plan = plans[0]
        
        if plan.status == WorkflowStatus.COMPLETED:
            plan_completed = True
            break
            
    assert plan_completed, "Plan did not complete successfully after retry recovery"
    assert fail_count == 1, "Mock fail was never triggered"
    logger.info("Retry Recovery test passed!")
    
    media.image_service.renderer.retrieve_outputs = original_retrieve
    await workflow.stop()
    await media.stop()
    await bus.stop()

async def test_in_flight_cancellation():
    logger.info("=== Starting Test: In-flight Cancellation ===")
    bus, media, workflow = await setup_environment()
    
    # Allow 2 concurrent jobs
    workflow.scheduler.max_concurrent_jobs = 2
    
    original_retrieve = media.image_service.renderer.retrieve_outputs
    
    async def mock_retrieve(job_id):
        job = next((j for j in media.image_service.active_jobs.values() if j.telemetry.get("renderer_job_id", j.job_id) == job_id), None)
        if job and "fail_fast" in job.request.prompt:
            return {"status": "failed", "error": "Fatal quick error"}
        if job and "slow" in job.request.prompt:
            await asyncio.sleep(10)
            return await original_retrieve(job_id)
        return await original_retrieve(job_id)
        
    media.image_service.renderer.retrieve_outputs = mock_retrieve
    
    # The retry logic means 'fail_fast' will actually retry 3 times, which might take 10s.
    # Let's set max_retries = 0 so it fails instantly.
    # (By default max_retries is 3 in GenerationJob, but we can't easily change it here except by intercepting it).
    # Instead, we'll let fail_fast fail 4 times rapidly.
    # Track loops for the slow step
    slow_loops = 0
    async def mock_retrieve_fast_fail(job_id):
        nonlocal slow_loops
        job = next((j for j in media.image_service.active_jobs.values() if j.telemetry.get("renderer_job_id", j.job_id) == job_id), None)
        if job and "fail_fast" in job.request.prompt:
            return {"status": "failed", "error": "Fatal quick error"}
        if job and "slow" in job.request.prompt:
            slow_loops += 1
            if slow_loops < 10:
                # Keep it running while fail_fast goes through retries
                return {"status": "running"}
            return await original_retrieve(job_id)
        return await original_retrieve(job_id)
    media.image_service.renderer.retrieve_outputs = mock_retrieve_fast_fail

    template = create_parallel_template("cancel")
    await bus.publish(Event(source="test", type=EventType.WORKFLOW_PLAN_REQUESTED, payload={"template": template.model_dump()}))
    
    plan_failed = False
    for _ in range(45):
        await asyncio.sleep(1)
        plans = workflow.repository.list_plans("Running") + workflow.repository.list_plans("Archived") + workflow.repository.list_plans("Failed")
        if not plans: continue
        plan = plans[0]
        
        if plan.status == WorkflowStatus.FAILED:
            plan_failed = True
            slow_step = plan.phases["phase1"].steps["step_slow"]
            assert slow_step.status == StepStatus.CANCELLED, f"Expected CANCELLED, got {slow_step.status}"
            
            await asyncio.sleep(1)
            found_job = None
            for j in list(media.image_service.active_jobs.values()) + list(media.image_service.finished_jobs.values()):
                if "slow" in j.request.prompt:
                    found_job = j
            if found_job:
                from raphael_core.kernel.models.media_generation import GenerationStatus
                assert found_job.status in (GenerationStatus.CANCELLED, GenerationStatus.FAILED), f"Job status was {found_job.status}, expected CANCELLED"
            break
            
    assert plan_failed, "Plan did not fail"
    logger.info("In-flight Cancellation test passed!")
    
    media.image_service.renderer.retrieve_outputs = original_retrieve
    await workflow.stop()
    await media.stop()
    await bus.stop()

async def run_all():
    await test_guard_trigger()
    await test_retry_recovery()
    await test_in_flight_cancellation()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(run_all())
