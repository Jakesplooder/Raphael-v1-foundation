import logging
from typing import Dict, Any, List

from ..interfaces import ServiceModule, Event, EventType, ModuleHealth
from ..services.media_generation.image_service import ImageGenerationService
from ..models.media_generation import GenerationRequest

logger = logging.getLogger("rrk.managers.media_generation")

class MediaGenerationManager(ServiceModule):
    """
    Manages media generation (images, video, audio) across different renderers.
    Host for ImageGenerationService.
    """
    
    def __init__(self, event_bus, config, commerce_repo):
        self.event_bus = event_bus
        self.config = config
        
        # Initialize Renderer Adapters
        from ..providers.commerce.comfyui_adapter import ComfyUIAdapter
        self.comfyui_adapter = ComfyUIAdapter()
        
        # Initialize Repositories
        from ..repositories.media_generation_repository import MediaGenerationRepository
        self.media_repo = MediaGenerationRepository(config.os_root)
        
        # Initialize Services
        self.image_service = ImageGenerationService(
            renderer=self.comfyui_adapter, 
            commerce_repo=commerce_repo,
            media_repo=self.media_repo
        )
        self._is_initialized = False

    @property
    def name(self) -> str:
        return "MediaGenerationManager"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus", "CommerceManager"]

    async def initialize(self) -> None:
        self.event_bus.subscribe(EventType.COMMERCE_IMAGE_GENERATED, self._handle_legacy_trigger)
        self._is_initialized = True
        logger.info("MediaGenerationManager initialized.")

    async def _handle_legacy_trigger(self, event: Event):
        pass

    async def start(self) -> None:
        await self.image_service.start()
        logger.info("ImageGenerationService started.")

    async def stop(self) -> None:
        await self.image_service.stop()
        
    async def shutdown(self) -> None:
        self._is_initialized = False

    def status(self) -> str:
        return f"running (active jobs: {len(self.image_service.active_jobs)})"

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK

    async def metrics(self) -> dict:
        from ..models.media_generation import GenerationStatus
        
        all_jobs = self.media_repo.get_jobs()
        queued = sum(1 for j in all_jobs if j.status == GenerationStatus.QUEUED)
        running = sum(1 for j in all_jobs if j.status == GenerationStatus.RUNNING)
        completed = sum(1 for j in all_jobs if j.status == GenerationStatus.COMPLETED)
        failed = sum(1 for j in all_jobs if j.status == GenerationStatus.FAILED)
        cancelled = sum(1 for j in all_jobs if j.status == GenerationStatus.CANCELLED)
        
        completed_durations = [j.telemetry.get("duration", 0) for j in all_jobs if j.status == GenerationStatus.COMPLETED and j.telemetry.get("duration") is not None]
        avg_render_time = sum(completed_durations) / len(completed_durations) if completed_durations else 0.0
        
        return {
            "queue_size": queued,
            "running": running,
            "completed": completed,
            "failed": failed,
            "cancelled": cancelled,
            "avg_render_time_sec": round(avg_render_time, 3),
            "total_jobs": len(all_jobs)
        }

    async def handle_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Any:
        if method == "POST" and endpoint == "/api/media/generate":
            import uuid
            req = GenerationRequest(
                request_id=f"REQ-{uuid.uuid4().hex[:6].upper()}",
                business_id=payload.get("business_id"),
                mission_id=payload.get("mission_id"),
                asset_type=payload.get("asset_type", "image"),
                prompt=payload.get("prompt", ""),
                metadata=payload.get("metadata", {})
            )
            job_id = await self.image_service.generate_asset(req)
            return {"status": "queued", "request_id": req.request_id}
            
        return {"error": "Unknown endpoint"}
