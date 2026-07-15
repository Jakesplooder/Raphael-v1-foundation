import asyncio
import unittest
import uuid
from typing import Dict, Any

from raphael_core.kernel.agent_base import AgentService
from raphael_core.kernel.interfaces import Job, JobState
from raphael_core.kernel.observability import ObservabilityLayer
from raphael_core.kernel.registry import registry
from raphael_core.kernel.job_system import JobSystem


class MockAgent(AgentService):
    @property
    def name(self) -> str:
        return "MockAgent"
        
    async def process_job(self, job: Job) -> Dict[str, Any]:
        ObservabilityLayer.info(self.name, f"Processing job {job.id}", trace_id=job.trace_id)
        return {"status": "success", "processed_trace": job.trace_id}


class TestAgentService(unittest.TestCase):
    def setUp(self):
        self.agent = MockAgent()
        self.job_system = JobSystem()
        registry.register_service(self.job_system)
        
    def test_agent_job_trace_propagation(self):
        """
        Verify that an agent correctly receives a Job and propagates its trace_id
        through its execution logic.
        """
        trace_id = str(uuid.uuid4())
        job = Job(
            owner="tester",
            module="MockAgent",
            trace_id=trace_id,
            payload={"task": "test_trace"}
        )
        
        result = asyncio.run(self.agent.process_job(job))
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["processed_trace"], trace_id)
        
if __name__ == "__main__":
    unittest.main()
