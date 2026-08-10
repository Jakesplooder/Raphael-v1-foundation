import asyncio
import time
import uuid
from typing import Dict, Any, Optional

from ...interfaces import Event, EventType, EventPriority
from ...event_bus import global_event_bus
from ...models.media_generation import GenerationRequest, GenerationJob, GenerationStatus
from ...providers.commerce.renderer import Renderer
from ...models.commerce import Asset, AssetType
from ...repositories.commerce_repository import CommerceRepository

class ImageGenerationService:
    """
    Orchestrates the image generation lifecycle: Submit -> Monitor -> Complete -> Register -> Emit Event
    """
    
    def __init__(self, renderer: Renderer, commerce_repo: CommerceRepository, media_repo: Any = None):
        self.renderer = renderer
        self.commerce_repo = commerce_repo
        self.media_repo = media_repo
        self.active_jobs: Dict[str, GenerationJob] = {}
        self.finished_jobs: Dict[str, GenerationJob] = {}
        self._monitoring_task: Optional[asyncio.Task] = None

    async def start(self):
        """Start the async monitoring loop and recover jobs."""
        if self.media_repo:
            for job in self.media_repo.get_jobs():
                if job.status in (GenerationStatus.QUEUED, GenerationStatus.RUNNING):
                    self.active_jobs[job.job_id] = job
                    
        if self._monitoring_task is None:
            self._monitoring_task = asyncio.create_task(self._monitor_jobs())

    async def stop(self):
        """Stop the async monitoring loop."""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            self._monitoring_task = None

    async def generate_asset(self, request: GenerationRequest) -> str:
        """
        Submit a request and begin the async lifecycle.
        Returns the request_id immediately (non-blocking).
        """
        # 1. Submit to renderer
        job = await self.renderer.submit(request)
        
        self.active_jobs[job.job_id] = job
        if self.media_repo:
            self.media_repo.upsert_job(job)
        
        # 2. Emit JOB_STARTED
        event_payload = {
            "request_id": request.request_id,
            "job_id": job.job_id,
            "renderer": self.renderer.renderer_name,
            "mission_id": request.mission_id,
            "business_id": request.business_id,
            "status": "started"
        }
        await global_event_bus.publish(
            Event(
                source="ImageGenerationService",
                type=EventType.JOB_STARTED,
                priority=EventPriority.NORMAL,
                payload=event_payload,
                mission_id=request.mission_id
            )
        )
        return job.job_id
        
    async def cancel_generation(self, job_id: str) -> bool:
        """Cancel a running generation job."""
        job = self.active_jobs.get(job_id)
        if not job:
            return False
            
        job.status = GenerationStatus.CANCELLED
        job.completed_at = time.time()
        
        # We could try to tell the renderer to stop, but ComfyUI's interrupt is global or prompt-specific.
        # For now, we just remove it from tracking so we stop polling it.
        self.finished_jobs[job.job_id] = job
        del self.active_jobs[job.job_id]
        
        if self.media_repo:
            self.media_repo.upsert_job(job)
            
        # Emit Cancelled Event
        await global_event_bus.publish(
            Event(
                source="ImageGenerationService",
                type=EventType.JOB_PROGRESS,
                priority=EventPriority.NORMAL,
                payload={
                    "job_id": job.job_id,
                    "status": "cancelled",
                    "progress": job.progress
                },
                mission_id=job.request.mission_id
            )
        )
        return True

    async def _monitor_jobs(self):
        """Background loop to monitor running jobs."""
        while True:
            await asyncio.sleep(5)  # Polling interval
            
            jobs_to_check = list(self.active_jobs.values())
            for job in jobs_to_check:
                if job.status == GenerationStatus.RUNNING:
                    # Check renderer status using renderer's specific job ID if available
                    renderer_id = job.telemetry.get("renderer_job_id", job.job_id)
                    result = await self.renderer.retrieve_outputs(renderer_id)
                    
                    status = result.get("status")
                    if status == "completed":
                        await self._handle_job_completed(job, result)
                    elif status == "failed":
                        await self._handle_job_failed(job, result)
                    else:
                        # Still running, emit progress
                        await self._emit_progress(job)

    async def _handle_job_completed(self, job: GenerationJob, result: Dict[str, Any]):
        job.status = GenerationStatus.COMPLETED
        job.completed_at = time.time()
        
        # Use adapter's real duration if available, else wall clock
        actual_render_duration = result.get("duration")
        if actual_render_duration is None:
             actual_render_duration = job.completed_at - (job.started_at or job.completed_at)
        job.telemetry["duration"] = actual_render_duration
        
        import logging
        logger = logging.getLogger("rrk.media.image_service")
        logger.info(f"[JOB COMPLETE] Parsed ComfyUI History Result: {result}")
        
        images = result.get("images", [])
        # For simplicity, just take the first generated image
        file_path = images[0].get("filename", "") if images else "unknown.png"
        
        import os
        is_verified = os.path.exists(file_path)
        if not is_verified:
            logger.warning(f"File verification failed: {file_path} does not exist on host.")
            
        if not file_path or file_path == "unknown.png":
             logger.error("Job completed but returned invalid file path. Marking as unverified.")
             is_verified = False
             # We could fail here in a strict setup.
             
        # 1. Register Asset (with Versioning)
        parent_asset_id = job.request.parent_asset_id
        version = 1
        if parent_asset_id:
             # Find parent to increment version
             parent_asset = self.commerce_repo.get_asset(parent_asset_id)
             if parent_asset:
                 version = parent_asset.version + 1
             else:
                 logger.warning(f"Requested parent_asset_id {parent_asset_id} not found. Versioning from 1.")
                 
        actual_model = result.get("model_name", job.request.metadata.get("model", "unknown"))
        asset = Asset(
            asset_id=f"ASSET-{uuid.uuid4().hex[:6].upper()}",
            mission_id=job.request.mission_id,
            business_id=job.request.business_id,
            asset_type=AssetType.PNG,
            file_path=file_path,
            workflow=self.renderer.renderer_name,
            prompt=job.request.prompt,
            model_name=actual_model,
            seed=job.request.metadata.get("seed"),
            parent_asset_id=parent_asset_id,
            version=version,
            is_verified=is_verified
        )
        self.commerce_repo.upsert_asset(asset)
        
        job.asset_id = asset.asset_id
        
        # 2. Emit ASSET_GENERATED event
        await global_event_bus.publish(
            Event(
                source="ImageGenerationService",
                type=EventType.ASSET_GENERATED,
                priority=EventPriority.NORMAL,
                payload={
                    "job_id": job.job_id,
                    "asset_id": asset.asset_id,
                    "mission_id": asset.mission_id,
                    "business_id": asset.business_id,
                    "workflow": asset.workflow,
                    "model": asset.model_name,
                    "generation_time": job.telemetry["duration"],
                    "storage_location": asset.file_path
                },
                mission_id=asset.mission_id
            )
        )
        
        # Move to finished
        self.finished_jobs[job.job_id] = job
        del self.active_jobs[job.job_id]
        if self.media_repo:
            self.media_repo.upsert_job(job)

    async def _handle_job_failed(self, job: GenerationJob, result: Dict[str, Any]):
        job.error_message = result.get("error", "Unknown error")
        
        if job.retry_count < job.max_retries:
            job.retry_count += 1
            delay = 2 ** job.retry_count
            job.status = GenerationStatus.QUEUED
            if self.media_repo:
                self.media_repo.upsert_job(job)
            
            import logging
            logger = logging.getLogger("ImageGenerationService")
            logger.warning(f"Job {job.job_id} failed with error '{job.error_message}'. Retrying ({job.retry_count}/{job.max_retries}) in {delay}s...")
            
            await global_event_bus.publish(
                Event(
                    source="ImageGenerationService",
                    type=EventType.JOB_PROGRESS,
                    priority=EventPriority.NORMAL,
                    payload={
                        "job_id": job.job_id,
                        "status": "retrying",
                        "error": job.error_message,
                        "retry_count": job.retry_count
                    },
                    mission_id=job.request.mission_id
                )
            )
            
            asyncio.create_task(self._retry_after(job, delay))
            return
            
        job.status = GenerationStatus.FAILED
        job.completed_at = time.time()
        
        # Move to finished
        self.finished_jobs[job.job_id] = job
        if job.job_id in self.active_jobs:
            del self.active_jobs[job.job_id]
        if self.media_repo:
            self.media_repo.upsert_job(job)
            
        await global_event_bus.publish(
            Event(
                source="ImageGenerationService",
                type=EventType.JOB_PROGRESS,
                priority=EventPriority.HIGH,
                payload={
                    "job_id": job.job_id,
                    "status": "failed",
                    "error": job.error_message
                },
                mission_id=job.request.mission_id
            )
        )
            
    async def _retry_after(self, job: GenerationJob, delay: int):
        await asyncio.sleep(delay)
        if job.status == GenerationStatus.CANCELLED:
            return
            
        import logging
        logger = logging.getLogger("rrk.media.image_service")
        logger.info(f"Backoff complete. Resubmitting job {job.job_id} to renderer now.")
            
        try:
            # Re-submit to renderer
            new_job_data = await self.renderer.submit(job.request)
            
            # Keep our internal job ID stable, but update the renderer ID
            job.telemetry["renderer_job_id"] = new_job_data.job_id
            job.status = GenerationStatus.RUNNING
            job.started_at = new_job_data.started_at
            
            self.active_jobs[job.job_id] = job
            if self.media_repo:
                self.media_repo.upsert_job(job)
        except Exception as e:
            # If resubmit fails immediately, mark it as failed again so it can retry or fail permanently
            await self._handle_job_failed(job, {"error": str(e)})

        
    async def _emit_progress(self, job: GenerationJob):
        await global_event_bus.publish(
            Event(
                source="ImageGenerationService",
                type=EventType.JOB_PROGRESS,
                priority=EventPriority.LOW,
                payload={
                    "job_id": job.job_id,
                    "request_id": job.request.request_id,
                    "status": "running"
                },
                mission_id=job.request.mission_id
            )
        )
