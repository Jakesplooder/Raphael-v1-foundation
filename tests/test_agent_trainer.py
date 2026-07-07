import unittest
from raphael_core.agent_trainer import TrainingProposer, ConstitutionalViolationError, TrainingLifecycleManager, ABTestTracker

class MockRegistry:
    def __init__(self):
        self.agents = {
            "AGENT-OPERATIONS": {
                "agent_id": "AGENT-OPERATIONS",
                "current_state": "active",
                "training_version": 1
            }
        }
        
    def load_registry(self):
        return self.agents
        
    def update_agent(self, agent_id, data):
        self.agents[agent_id] = data

class AgentTrainerTests(unittest.TestCase):
    def test_proposer_valid_lever(self):
        proposer = TrainingProposer()
        proposal = proposer.propose_training("AGENT-OPERATIONS", "prompt_improvement", {"accuracy": 80.0})
        self.assertEqual(proposal["agent_id"], "AGENT-OPERATIONS")
        self.assertEqual(proposal["lever"], "prompt_improvement")
        self.assertEqual(proposal["status"], "proposed")
        self.assertTrue("TRAIN-" in proposal["training_id"])

    def test_proposer_invalid_lever(self):
        proposer = TrainingProposer()
        with self.assertRaises(ConstitutionalViolationError):
            proposer.propose_training("AGENT-OPERATIONS", "memory_injection", {"accuracy": 80.0})

    def test_ab_test_tracker(self):
        tracker = ABTestTracker()
        training_record = {"baseline_metrics": {"composite": 85.0}}
        current_metrics = {"composite": 88.0}
        
        result = tracker.evaluate_test(training_record, current_metrics)
        self.assertTrue(result["passed"])
        self.assertEqual(result["delta"], 3.0)
        
        failed_metrics = {"composite": 82.0}
        result_failed = tracker.evaluate_test(training_record, failed_metrics)
        self.assertFalse(result_failed["passed"])
        self.assertEqual(result_failed["delta"], -3.0)

    def test_lifecycle_manager(self):
        reg = MockRegistry()
        manager = TrainingLifecycleManager(reg)
        
        proposal = {
            "training_id": "TRAIN-123",
            "agent_id": "AGENT-OPERATIONS",
            "status": "proposed"
        }
        
        res = manager.activate_training("TRAIN-123", proposal)
        self.assertTrue(res)
        self.assertEqual(proposal["status"], "active")
        
        # Check that it updated the registry agent version
        agent = reg.agents["AGENT-OPERATIONS"]
        self.assertEqual(agent["training_version"], 2)
        
        # Check duplicate activation fails
        res_dup = manager.activate_training("TRAIN-123", proposal)
        self.assertFalse(res_dup)

if __name__ == "__main__":
    unittest.main()
