import unittest
import asyncio
from unittest.mock import patch, MagicMock

from raphael_core.kernel.registry import registry
from raphael_core.kernel.interfaces import ModuleHealth
from raphael_core.world_model import WorldModelService, world_model_answer_legacy

class TestWorldModelService(unittest.TestCase):
    def setUp(self):
        self.svc = WorldModelService()

    def test_service_contract(self):
        """Verify the service implements the ServiceModule contract correctly."""
        self.assertEqual(self.svc.name, "WorldModelService")
        self.assertIn("EventBus", self.svc.depends_on)
        self.assertIn("RuntimeStateStore", self.svc.depends_on)
        self.assertEqual(self.svc.health(), ModuleHealth.FAILED) # Failed because it's not running
        
    @patch('raphael_core.world_model._world_model_answer_internal')
    def test_query_delegation(self, mock_internal):
        """Verify the service delegates correctly and handles trace IDs."""
        mock_internal.return_value = {"answer": "test", "allowed": True}
        
        result = self.svc.query("Aaron", "test_purpose", "test_question")
        
        self.assertEqual(result["answer"], "test")
        self.assertTrue(self.svc._queries_handled > 0)
        
        # Verify trace_id was passed down
        mock_internal.assert_called_once()
        kwargs = mock_internal.call_args.kwargs
        self.assertIn("trace_id", kwargs)
        self.assertIsNotNone(kwargs["trace_id"])
        
    @patch('raphael_core.world_model.WorldModelService.query')
    def test_legacy_bridge_with_kernel(self, mock_query):
        """Verify the legacy bridge uses the RRK if the kernel is running and healthy."""
        mock_query.return_value = {"answer": "rrk_path"}
        
        registry.register_service(self.svc)
        self.svc._running = True # Mock healthy state
        
        result = world_model_answer_legacy(None, "Aaron", "test_purpose", "test_question")
        self.assertEqual(result["answer"], "rrk_path")
        mock_query.assert_called_once()
        
    @patch('raphael_core.world_model._world_model_answer_internal')
    def test_legacy_bridge_without_kernel(self, mock_internal):
        """Verify the legacy bridge falls back to internal if kernel is not running."""
        mock_internal.return_value = {"answer": "legacy_path"}
        
        # Remove it from registry to simulate kernel not running
        registry._services.pop("WorldModelService", None)
        
        result = world_model_answer_legacy(None, "Aaron", "test_purpose", "test_question")
        self.assertEqual(result["answer"], "legacy_path")
        mock_internal.assert_called_once()

if __name__ == '__main__':
    unittest.main()
