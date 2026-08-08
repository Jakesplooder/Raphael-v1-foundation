import json
import logging
from typing import Dict, Any, Optional
from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore

logger = logging.getLogger("kernel.media_generation.job_store")

class JobState:
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    WAITING_FOR_HISTORY = "WAITING_FOR_HISTORY"
    DOWNLOADING = "DOWNLOADING"
    VERIFYING = "VERIFYING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class JobStore:
    def __init__(self, idempotency_store: IdempotencyStore):
        self.store = idempotency_store

    def _get_key(self, request_id: str) -> str:
        return f"media_job_{request_id}"

    def get_job(self, request_id: str) -> Optional[Dict[str, Any]]:
        return self.store.get(self._get_key(request_id))

    def create_job(self, request_id: str, workflow_hash: str, request_hash: str, workflow_version: str) -> None:
        data = {
            "state": JobState.QUEUED,
            "prompt_id": None,
            "workflow_hash": workflow_hash,
            "workflow_version": workflow_version,
            "request_hash": request_hash,
            "artifact_path": None,
            "error": None
        }
        self.store.set(self._get_key(request_id), data)

    def update_state(self, request_id: str, new_state: str, **kwargs) -> None:
        job = self.get_job(request_id)
        if not job:
            logger.error(f"Attempted to update non-existent job {request_id}")
            return
        
        job["state"] = new_state
        for k, v in kwargs.items():
            job[k] = v
            
        self.store.set(self._get_key(request_id), job)
        logger.debug(f"Job {request_id} transitioned to {new_state}")
