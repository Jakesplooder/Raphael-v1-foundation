from __future__ import annotations

import json
import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from raphael_core.config import load_config
from raphael_core import workflow_runner
from tests.support import TempRaphael


class WorkflowRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def _queue(self, workflow_id: str) -> dict:
        process = Mock(pid=43210)
        with (
            patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}),
            patch("raphael_core.workflow_runner.subprocess.Popen", return_value=process),
        ):
            return workflow_runner.workflow_execute(self.config, workflow_id, self.os.config)

    def test_registry_status_and_required_notes_exist(self) -> None:
        status = workflow_runner.runner_status(self.config)
        self.assertEqual(3, status["workflow_count"])
        self.assertTrue(Path(status["registry"]).exists())
        for name in workflow_runner.WORKFLOW_NOTES:
            self.assertTrue((workflow_runner.notes_root(self.config) / name).exists())

    def test_daily_brief_workflow_executes_and_updates_task(self) -> None:
        queued = self._queue("daily-executive-brief")
        exec_id = queued["exec_id"]
        with (
            patch("raphael_core.workflow_runner.legacy.generate_task_review", return_value="tasks.md"),
            patch("raphael_core.workflow_runner.legacy.goal_review", return_value="goals.md"),
            patch("raphael_core.workflow_runner.legacy.communication_review", return_value="communications.md"),
            patch("raphael_core.workflow_runner.legacy.knowledge_review", return_value="knowledge.md"),
            patch("raphael_core.workflow_runner.legacy.morning_brief", return_value="morning.md"),
            patch("raphael_core.workflow_runner.legacy.executive_brief", return_value="executive.md"),
        ):
            result = workflow_runner.workflow_worker(self.config, exec_id)
        self.assertEqual("completed", result["status"])
        self.assertEqual(6, result["completed_stages"])
        self.assertTrue(result["task_id"])
        task = workflow_runner.legacy.find_task_by_id(self.config, result["task_id"])
        self.assertEqual("Done", task["status"])

    def test_knowledge_workflow_executes_registered_native_steps(self) -> None:
        queued = self._queue("knowledge-processing")
        with (
            patch("raphael_core.workflow_runner.legacy.knowledge_registered_sources", return_value=[]),
            patch("raphael_core.workflow_runner.legacy.knowledge_summarize", return_value="summarized"),
            patch("raphael_core.workflow_runner.legacy.knowledge_classify", return_value="classified"),
            patch("raphael_core.workflow_runner.legacy.knowledge_relationships", return_value="related"),
            patch("raphael_core.workflow_runner.legacy.knowledge_index", return_value="indexed"),
        ):
            result = workflow_runner.workflow_worker(self.config, queued["exec_id"])
        self.assertEqual("completed", result["status"])
        self.assertEqual(5, result["completed_stages"])

    def test_pod_workflow_runs_only_through_registered_orchestrator(self) -> None:
        queued = self._queue("pod-pipeline")
        with (
            patch("raphael_core.workflow_runner.pod_workflow.pod_workflow", return_value={"workflow_id": "PODFLOW-20260621-ABCDEF12"}),
            patch("raphael_core.workflow_runner.pod_workflow.pod_workflow_continue", return_value={"status": "completed"}) as advance,
        ):
            result = workflow_runner.workflow_worker(self.config, queued["exec_id"])
        self.assertEqual("completed", result["status"])
        self.assertGreaterEqual(advance.call_count, 11)

    def test_n8n_execution_validates_and_captures_local_result(self) -> None:
        workflow_runner.ensure_runner(self.config)
        path = workflow_runner.registry_path(self.config)
        registry = json.loads(path.read_text(encoding="utf-8"))
        registry["workflows"].append({
            "workflow_id": "n8n-local-test",
            "name": "n8n Local Test",
            "category": "workflow",
            "description": "Credential-free local manual workflow.",
            "execution_mode": "n8n",
            "risk_level": "medium",
            "approval_required": True,
            "enabled": True,
            "source": "42",
        })
        path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        queued = self._queue("n8n-local-test")

        def fake_request(_config, method, request_path, body=None):
            if method == "GET" and request_path == "/rest/workflows/42":
                return {"data": {"nodes": [{"name": "Manual", "type": "n8n-nodes-base.manualTrigger", "parameters": {}}]}}
            if method == "POST":
                return {"data": {"executionId": "9001"}}
            return {"data": {"id": "9001", "status": "success", "finished": True, "data": {"local": True}}}

        with patch("raphael_core.workflow_runner._n8n_request", side_effect=fake_request):
            result = workflow_runner.workflow_worker(self.config, queued["exec_id"])
        self.assertEqual("completed", result["status"])
        self.assertEqual("9001", result["n8n_execution_id"])
        self.assertEqual(1, result["completed_stages"])

    def test_cancel_is_confirmation_gated_and_does_not_kill_processes(self) -> None:
        queued = self._queue("daily-executive-brief")
        with patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}):
            cancelled = workflow_runner.workflow_cancel(self.config, queued["exec_id"])
        self.assertEqual("cancelled", cancelled["status"])
        self.assertTrue(cancelled["cancel_requested"])

    def test_failure_is_persisted_recoverable_and_updates_task(self) -> None:
        queued = self._queue("knowledge-processing")
        with patch("raphael_core.workflow_runner.legacy.knowledge_registered_sources", side_effect=RuntimeError("local test failure")):
            result = workflow_runner.workflow_worker(self.config, queued["exec_id"])
        self.assertEqual("failed", result["status"])
        self.assertTrue(result["recoverable"])
        failures = workflow_runner.workflow_failures(self.config)
        self.assertEqual(1, failures["count"])
        task = workflow_runner.legacy.find_task_by_id(self.config, result["task_id"])
        self.assertEqual("Blocked", task["status"])
