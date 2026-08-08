import logging
from typing import Dict, Any

from .comfyui_client import ComfyUIClient
from .job_store import JobStore, JobState
from .health_monitor import ComfyUIHealthMonitor
from .artifact_downloader import ArtifactDownloader
from .verifier import ArtifactVerifier
from .workflow_registry import WorkflowRegistry
from .recovery import MediaGenerationRecoveryManager
from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore

logger = logging.getLogger("kernel.media_generation")

class MediaGenerationResult:
    def __init__(self, status: str, artifact_path: str = None, error: str = None):
        self.status = status
        self.artifact_path = artifact_path
        self.error = error

class MediaGenerationService:
    def __init__(self, idempotency_store: IdempotencyStore, workflows_dir: str):
        self.client = ComfyUIClient()
        self.store = JobStore(idempotency_store)
        self.health = ComfyUIHealthMonitor(self.client)
        self.registry = WorkflowRegistry(workflows_dir)
        self.downloader = ArtifactDownloader(self.client.base_url)
        self.verifier = ArtifactVerifier()
        
        self.recovery_manager = MediaGenerationRecoveryManager(
            self.client, self.store, self.health, self.registry, self.downloader, self.verifier
        )

    def generate(self, workflow: str, concept: Dict, request_id: str, target_artifact_path: str) -> MediaGenerationResult:
        """
        High-level interface for business domains to request media generation.
        """
        logger.info(f"Received media generation request {request_id} using workflow {workflow}")
        
        success = self.recovery_manager.run_job(workflow, concept, request_id, target_artifact_path)
        
        job = self.store.get_job(request_id)
        if success and job and job["state"] == JobState.COMPLETE:
            return MediaGenerationResult("COMPLETE", artifact_path=job.get("artifact_path"))
            
        error = job.get("error", "Unknown error") if job else "No job created"
        return MediaGenerationResult("FAILED", error=error)
