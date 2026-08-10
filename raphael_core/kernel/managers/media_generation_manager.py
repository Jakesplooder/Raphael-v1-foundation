import logging
import uuid
import time
import asyncio
from typing import Dict, Any, List
from pathlib import Path

from ..interfaces import ServiceModule, Event, EventType, ModuleHealth
from ..providers.workflow.image_generation_provider import ImageGenerationProvider

logger = logging.getLogger("rrk.managers.media")

class MediaGenerationManager(ServiceModule):
    def __init__(self, event_bus, config):
        self.event_bus = event_bus
        self.config = config
        self._is_initialized = False
        self.provider = ImageGenerationProvider()
        self.active_jobs = {}
        self.asset_registry = {}
        
        # Path for persistent job storage
        os_root = getattr(self.config, "os_root", Path("C:/RaphaelOS"))
        self.jobs_file = os_root / "runtime" / "media_jobs.json"

    @property
    def name(self) -> str:
        return "MediaGenerationManager"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus"]

    async def initialize(self) -> None:
        self.event_bus.subscribe(EventType.JOB_STARTED, self._handle_job_started)
        self._is_initialized = True
        logger.info("MediaGenerationManager initialized.")

    async def start(self) -> None:
        """
        Start the module and load any persisted jobs from disk to ensure Active Jobs panel populates.
        """
        self._load_jobs()
        logger.info(f"MediaGenerationManager started. Loaded {len(self.active_jobs)} jobs.")

    def _load_jobs(self):
        import json
        if self.jobs_file.exists():
            try:
                with open(self.jobs_file, "r") as f:
                    data = json.load(f)
                    self.active_jobs = data.get("active_jobs", {})
                    self.asset_registry = data.get("asset_registry", {})
            except Exception as e:
                logger.error(f"Failed to load media jobs: {e}")

    def _save_jobs(self):
        import json
        self.jobs_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.jobs_file, "w") as f:
            json.dump({
                "active_jobs": self.active_jobs,
                "asset_registry": self.asset_registry
            }, f)

    async def _handle_job_started(self, event: Event):
        payload = event.payload
        if payload.get("type") != "image_generation":
            return
            
        job_id = payload.get("job_id", str(uuid.uuid4()))
        prompt = payload.get("prompt", "")
        
        # Chat-triggered generation request defaults
        business_id = payload.get("business_id", "chat-adhoc")
        mission_id = payload.get("mission_id", f"chat-{int(time.time())}")
        
        self.active_jobs[job_id] = {
            "status": "running",
            "prompt": prompt,
            "business_id": business_id,
            "mission_id": mission_id,
            "start_time": time.time()
        }
        self._save_jobs()
        
        # Fire off the actual generation in a background task so we don't block the event bus
        asyncio.create_task(self._run_generation(job_id, prompt))
        
    async def _run_generation(self, job_id: str, prompt: str):
        try:
            asset_path = await self.provider.generate(prompt)
            self.active_jobs[job_id]["status"] = "completed"
            asset_id = str(uuid.uuid4())
            self.active_jobs[job_id]["asset_id"] = asset_id
            self.asset_registry[asset_id] = str(asset_path)
            logger.info(f"Job {job_id} completed successfully. Asset: {asset_id}")
        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            self.active_jobs[job_id]["status"] = "failed"
            self.active_jobs[job_id]["error"] = str(e)
            
        self._save_jobs()

    async def stop(self) -> None:
        self._save_jobs()
        
    async def shutdown(self) -> None:
        self._is_initialized = False

    def status(self) -> str:
        return "running" if self._is_initialized else "stopped"

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    def health(self) -> ModuleHealth:
        # Synchronous health check to avoid coroutine object errors in HealthMonitor
        return ModuleHealth.OK

    async def metrics(self) -> dict:
        return {}

    async def handle_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Any:
        # Serve jobs status
        if method == "GET" and endpoint == "/api/status/jobs":
            return {"jobs": self.active_jobs}
            
        # Security fix: ID-based lookup resolving real path server-side, never a client-supplied raw path
        elif method == "GET" and endpoint.startswith("/api/asset/"):
            asset_id = endpoint.split("/")[-1]
            if asset_id in self.asset_registry:
                from fastapi.responses import FileResponse
                return FileResponse(self.asset_registry[asset_id])
            
            # Return 404 cleanly
            from fastapi import Response
            return Response(content='{"error": "Asset not found"}', status_code=404, media_type="application/json")
            
        return {"error": "Unknown endpoint"}
