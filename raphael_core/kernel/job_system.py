import asyncio
import time
from typing import Dict, Any, List, Optional
from collections import OrderedDict

from .interfaces import ServiceModule, ModuleHealth, Job, JobState
from .observability import ObservabilityLayer
from .state import store


class JobSystem(ServiceModule):
    """
    80.2 Job System
    Rich lifecycle management for asynchronous workloads.
    Provides priority queuing and worker isolation.
    """

    def __init__(self):
        self._jobs: Dict[str, Job] = OrderedDict()
        self._running = False
        self._worker_task = None
        self._queue = asyncio.PriorityQueue()
        
    @property
    def name(self) -> str:
        return "JobSystem"

    @property
    def depends_on(self) -> list[str]:
        return ["EventBus"]

    async def initialize(self) -> None:
        store.set_state(self.name, "status", "initialized")

    async def start(self) -> None:
        self._running = True
        self._worker_task = asyncio.create_task(self._process_queue())
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "JobSystem started")

    async def heartbeat(self) -> bool:
        return self._running and (self._worker_task is not None and not self._worker_task.done())

    async def stop(self) -> None:
        self._running = False
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        store.set_state(self.name, "status", "stopped")

    async def shutdown(self) -> None:
        self._jobs.clear()
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "JobSystem shut down.")

    def health(self) -> ModuleHealth:
        if self._running:
            return ModuleHealth.OK
        return ModuleHealth.FAILED

    def status(self) -> str:
        return f"Tracking {len(self._jobs)} total jobs. {self._queue.qsize()} queued."

    def metrics(self) -> Dict[str, Any]:
        states = {state.value: 0 for state in JobState}
        for job in self._jobs.values():
            states[job.state.value] += 1
            
        return {
            "total_jobs": len(self._jobs),
            "states": states,
            "queue_depth": self._queue.qsize()
        }

    async def submit_job(self, job: Job) -> str:
        """Submit a new job to the system."""
        self._jobs[job.id] = job
        job.state = JobState.QUEUED
        
        # Priority queue sorts by priority natively. We use a tuple (priority, time, job)
        # Assuming lower priority value = higher urgency, otherwise invert priority.
        await self._queue.put((-job.priority, job.created_at, job))
        
        ObservabilityLayer.info(self.name, f"Job {job.id} submitted by {job.owner}", trace_id=job.trace_id)
        return job.id

    def update_state(self, job_id: str, new_state: JobState, trace_id: Optional[str] = None) -> None:
        job = self._jobs.get(job_id)
        if job:
            job.state = new_state
            ObservabilityLayer.debug(self.name, f"Job {job_id} transitioned to {new_state}", trace_id=trace_id or job.trace_id)

    def get_job(self, job_id: str) -> Optional[Job]:
        return self._jobs.get(job_id)

    async def _process_queue(self) -> None:
        while self._running:
            try:
                # The primary dispatcher
                _priority, _time, job = await self._queue.get()
                
                if job.state != JobState.QUEUED:
                    self._queue.task_done()
                    continue

                self.update_state(job.id, JobState.RUNNING)
                
                from .registry import registry
                target_service = registry.get_service(job.module)
                
                if target_service and hasattr(target_service, "process_job"):
                    try:
                        # Yield execution to the specific module's execute_job wrapper if available,
                        # else fallback to process_job natively.
                        if hasattr(target_service, "execute_job"):
                            result = await target_service.execute_job(job)
                        else:
                            result = await target_service.process_job(job)
                        ObservabilityLayer.info(self.name, f"Job {job.id} completed by {job.module}", trace_id=job.trace_id)
                        self.update_state(job.id, JobState.COMPLETED)
                    except Exception as e:
                        ObservabilityLayer.error(self.name, f"Job {job.id} failed in {job.module}: {e}", trace_id=job.trace_id)
                        self.update_state(job.id, JobState.FAILED)
                else:
                    ObservabilityLayer.error(self.name, f"Job {job.id} failed: target module {job.module} not found or invalid", trace_id=job.trace_id)
                    self.update_state(job.id, JobState.FAILED)
                    
                self._queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                ObservabilityLayer.error(self.name, f"Job loop error: {e}")
                await asyncio.sleep(1)
