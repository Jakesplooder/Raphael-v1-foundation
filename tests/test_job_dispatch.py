import asyncio
import unittest
import uuid
from typing import Dict, Any

from raphael_core.kernel.agent_base import AgentService
from raphael_core.kernel.interfaces import Job, JobState
from raphael_core.kernel.observability import ObservabilityLayer
from raphael_core.kernel.registry import registry
from raphael_core.kernel.job_system import JobSystem


class MockDispatcherAgent(AgentService):
    @property
    def name(self) -> str:
        return "ProjectManagerAgent"
        
    async def process_job(self, job: Job) -> Dict[str, Any]:
        ObservabilityLayer.info(self.name, f"Processing job {job.id}", trace_id=job.trace_id)
        return {"status": "success", "processed_trace": job.trace_id}


class TestJobDispatch(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = MockDispatcherAgent()
        self.job_system = JobSystem()
        registry.register_service(self.agent)
        registry.register_service(self.job_system)
        
        # Start the job system so _process_queue begins running
        await self.job_system.start()
        
    async def asyncTearDown(self):
        await self.job_system.stop()
        
    async def test_job_dispatch_to_agent(self):
        """
        Verify that a job submitted to JobSystem is properly routed to the correct agent
        and marked as COMPLETED.
        """
        trace_id = str(uuid.uuid4())
        job = Job(
            owner="tester",
            module="ProjectManagerAgent",
            trace_id=trace_id,
            payload={"task": "test_routing"}
        )
        
        # Submit the job
        job_id = await self.job_system.submit_job(job)
        
        # Wait a short moment for the queue loop to pick it up and process it
        await asyncio.sleep(0.1)
        
        # Verify the state transition
        processed_job = self.job_system.get_job(job_id)
        self.assertIsNotNone(processed_job)
        self.assertEqual(processed_job.state, JobState.COMPLETED)
        
if __name__ == "__main__":
    unittest.main()
