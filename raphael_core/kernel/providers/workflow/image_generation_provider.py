import asyncio
from typing import Dict, Any

from .automation_provider import AutomationProvider
from ...services.media_generation.image_service import ImageGenerationService
from ...models.media_generation import GenerationRequest

class ImageGenerationProvider(AutomationProvider):
    """
    Workflow Provider that delegates 'generate_asset' actions to the ImageGenerationService.
    This bridge allows the generic WorkflowEngine to trigger async media pipelines.
    """
    
    def __init__(self, image_service: ImageGenerationService):
        self.image_service = image_service

    @property
    def provider_name(self) -> str:
        return "ImageGenerationService"

    async def execute_step(self, action: str, parameters: Dict[str, Any], idempotency_key: str = None) -> Dict[str, Any]:
        if action != "generate_asset":
            raise NotImplementedError(f"Action '{action}' is not supported by ImageGenerationProvider.")
            
        import uuid
        request_id = idempotency_key or f"REQ-{uuid.uuid4().hex[:6].upper()}"
        
        req = GenerationRequest(
            request_id=request_id,
            business_id=parameters.get("business_id"),
            mission_id=parameters.get("mission_id"),
            asset_type=parameters.get("asset_type", "image"),
            prompt=parameters.get("prompt", ""),
            parent_asset_id=parameters.get("parent_asset_id"),
            metadata=parameters.get("metadata", {})
        )
        
        # We submit it to the service. 
        # Since this is a workflow step, we want to wait for it to finish!
        # The service is async, we will wait for the asset to be generated.
        
        # 1. Submit
        job_id = await self.image_service.generate_asset(req)
        
        # 2. Polling loop to wait for completion (bridging async service to synchronous-like workflow step)
        try:
            while True:
                # Check if job is still active
                job = self.image_service.active_jobs.get(job_id)
                if not job:
                    # Job has been moved to finished_jobs
                    finished_job = self.image_service.finished_jobs.get(job_id)
                    if not finished_job:
                        raise RuntimeError("Job vanished from both active and finished queues without trace.")
                        
                    from ...models.media_generation import GenerationStatus
                    if finished_job.status == GenerationStatus.COMPLETED:
                        asset = self.image_service.commerce_repo.get_asset(finished_job.asset_id)
                        is_verified = asset.is_verified if asset else False
                        return {"status": "success", "asset_id": finished_job.asset_id, "is_verified": is_verified}
                    elif finished_job.status == GenerationStatus.FAILED:
                        return {"status": "failed", "error": finished_job.error_message}
                    
                await asyncio.sleep(2)
        except asyncio.CancelledError:
            import logging
            logger = logging.getLogger("rrk.providers.image_generation")
            logger.warning(f"Workflow step cancelled, cancelling underlying generation job {job_id}")
            await self.image_service.cancel_generation(job_id)
            raise
