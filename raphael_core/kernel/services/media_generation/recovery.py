import time
import logging
import hashlib
from typing import Dict, Any

from .comfyui_client import ComfyUIClient, ExpectedTimeoutError, WarningTimeoutError, ServerUnreachableError, WorkflowFailureError, RestartDetectedError
from .job_store import JobStore, JobState
from .health_monitor import ComfyUIHealthMonitor
from .artifact_downloader import ArtifactDownloader
from .verifier import ArtifactVerifier
from .workflow_registry import WorkflowRegistry, WorkflowValidationError

logger = logging.getLogger("kernel.media_generation.recovery")

class MediaGenerationRecoveryManager:
    def __init__(self, 
                 client: ComfyUIClient, 
                 store: JobStore, 
                 health: ComfyUIHealthMonitor, 
                 registry: WorkflowRegistry,
                 downloader: ArtifactDownloader,
                 verifier: ArtifactVerifier):
        self.client = client
        self.store = store
        self.health = health
        self.registry = registry
        self.downloader = downloader
        self.verifier = verifier

    def run_job(self, workflow_name: str, concept: Dict, request_id: str, target_artifact_path: str) -> bool:
        """
        Executes the job through the state machine until COMPLETE or FAILED.
        """
        # Hash inputs for state verification
        workflow_hash = hashlib.md5(workflow_name.encode()).hexdigest()
        request_hash = hashlib.md5(str(concept).encode()).hexdigest()
        workflow_version = "v1"

        # 1. Check existing state
        job = self.store.get_job(request_id)
        if not job:
            self.store.create_job(request_id, workflow_hash, request_hash, workflow_version)
            job = self.store.get_job(request_id)
            
        state = job["state"]
        
        while state not in [JobState.COMPLETE, JobState.FAILED]:
            logger.info(f"[RecoveryManager] Request {request_id} currently in state: {state}")
            
            try:
                if state == JobState.QUEUED:
                    state = self._state_queued(request_id, job, workflow_name, concept)
                elif state == JobState.WAITING_FOR_HISTORY:
                    state = self._state_waiting(request_id, job)
                elif state == JobState.DOWNLOADING:
                    state = self._state_downloading(request_id, job, target_artifact_path)
                elif state == JobState.VERIFYING:
                    state = self._state_verifying(request_id, job, target_artifact_path)
                else:
                    logger.error(f"Unknown state {state}")
                    state = JobState.FAILED
            except Exception as e:
                logger.error(f"Unhandled exception in state {state}: {e}")
                self.store.update_state(request_id, JobState.FAILED, error=str(e))
                return False
                
        return state == JobState.COMPLETE

    def _state_queued(self, request_id: str, job: Dict, workflow_name: str, concept: Dict) -> str:
        workflow = self.registry.load_workflow(workflow_name)
        
        # Inject seed deterministically
        seed = int(hashlib.sha256(request_id.encode()).hexdigest(), 16) % (2**53 - 1)
        
        if workflow_name == "ltx2_i2v":
            workflow = self.registry.inject_ltx2_i2v(workflow, concept, request_id, seed)
        else:
            raise NotImplementedError(f"Unsupported workflow {workflow_name}")

        try:
            prompt_id = self.client.queue_prompt(workflow)
            if not prompt_id:
                raise Exception("No prompt_id returned from ComfyUI")
                
            self.store.update_state(request_id, JobState.WAITING_FOR_HISTORY, prompt_id=prompt_id)
            return JobState.WAITING_FOR_HISTORY
            
        except ServerUnreachableError as e:
            logger.error(f"Incident: Server Unreachable. {e}")
            if self.health.wait_for_recovery():
                return JobState.QUEUED
            return JobState.FAILED
        except WorkflowFailureError as e:
            logger.error(f"Incident: HTTP 500 Workflow Failure: {e}")
            return JobState.FAILED
        except Exception as e:
            logger.error(f"Failed to queue prompt: {e}")
            return JobState.FAILED

    def _state_waiting(self, request_id: str, job: Dict) -> str:
        prompt_id = job.get("prompt_id")
        if not prompt_id:
            logger.error("Missing prompt_id in WAITING state. Reverting to QUEUED.")
            return JobState.QUEUED

        while True:
            try:
                history = self.client.get_history(prompt_id)
                if history:
                    # Save the history data back to state for DOWNLOADING
                    self.store.update_state(request_id, JobState.DOWNLOADING, history_output=history.get("outputs", {}))
                    return JobState.DOWNLOADING
                    
                # Still waiting
                time.sleep(10)
                
            except ExpectedTimeoutError:
                logger.debug("Expected timeout (server busy). Polling again.")
            except WarningTimeoutError:
                logger.warning("Warning: Timeout took longer than expected, but continuing.")
            except RestartDetectedError as e:
                logger.error(f"Incident: {e}")
                # Server restarted mid-generation. The queue is wiped. We must recover by re-queuing!
                logger.info("Server restart wiped queue. Reverting job to QUEUED.")
                self.store.update_state(request_id, JobState.QUEUED, prompt_id=None)
                return JobState.QUEUED
            except ServerUnreachableError as e:
                logger.error(f"Incident: {e}")
                if self.health.wait_for_recovery():
                    continue
                return JobState.FAILED

    def _state_downloading(self, request_id: str, job: Dict, target_path: str) -> str:
        history_output = job.get("history_output", {})
        
        if not history_output:
            logger.error("Empty history output! Workflow silently failed or was pruned.")
            self.store.update_state(request_id, JobState.FAILED, error="WORKFLOW_VALIDATION_FAILURE")
            return JobState.FAILED
            
        success = self.downloader.download_video(history_output, target_path)
        if success:
            self.store.update_state(request_id, JobState.VERIFYING, artifact_path=target_path)
            return JobState.VERIFYING
        else:
            self.store.update_state(request_id, JobState.FAILED, error="DOWNLOAD_FAILURE")
            return JobState.FAILED

    def _state_verifying(self, request_id: str, job: Dict, target_path: str) -> str:
        if self.verifier.verify(target_path):
            self.store.update_state(request_id, JobState.COMPLETE)
            return JobState.COMPLETE
        else:
            self.store.update_state(request_id, JobState.FAILED, error="VERIFICATION_FAILURE")
            return JobState.FAILED
