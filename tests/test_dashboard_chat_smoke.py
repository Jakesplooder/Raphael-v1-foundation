from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from raphael_core import dashboard_chat_tests
from raphael_core.config import load_config
from tests.support import TempRaphael


def load_dashboard_module():
    path = Path("C:/RaphaelOS/dashboard/app.py")
    spec = importlib.util.spec_from_file_location("dashboard_chat_smoke_test_app", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DashboardChatSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dashboard = load_dashboard_module()

    def test_test_mode_routes_pod_without_real_execution(self) -> None:
        result = self.dashboard.dashboard_chat_response(
            "create me a POD t shirt with an elephant picture on it",
            test_mode=True,
            test_session_id="pod-route",
            reset_test_session=True,
        )
        self.assertEqual("pod_workflow", result["intent"])
        self.assertIn("pod-workflow-continue", result["command"])
        self.assertTrue(result["test_mode"])
        self.assertEqual(1, result["test_state"]["workflow_stage"])

    def test_duplicate_dashboard_confirms_advance_only_once(self) -> None:
        session = "duplicate-confirm"
        self.dashboard.dashboard_chat_response(
            "create me a POD t shirt with an elephant picture on it",
            test_mode=True,
            test_session_id=session,
            reset_test_session=True,
        )
        first = self.dashboard.dashboard_chat_response("confirm", test_mode=True, test_session_id=session)
        stage = first["test_state"]["workflow_stage"]
        duplicates = [
            self.dashboard.dashboard_chat_response("confirm", test_mode=True, test_session_id=session)
            for _ in range(3)
        ]
        self.assertTrue(all(item["test_state"]["workflow_stage"] == stage for item in duplicates))
        self.assertTrue(all(item["intent"] == "confirmation_debounced" for item in duplicates))
        self.assertTrue(all("Done." not in item["response"] for item in duplicates))

    def test_comfyui_offline_queues_service_start_without_permanent_failure(self) -> None:
        session = "comfy-offline"
        self.dashboard.dashboard_chat_response(
            "create a POD shirt using ComfyUI",
            test_mode=True,
            test_session_id=session,
            reset_test_session=True,
            test_scenario="comfyui_offline",
        )
        result = self.dashboard.dashboard_chat_response(
            "confirm",
            test_mode=True,
            test_session_id=session,
            test_scenario="comfyui_offline",
        )
        self.assertIn("service-start", result["command"])
        self.assertIn("comfyui", result["command"])
        self.assertEqual("Confirmation Required", result["status"])
        self.assertEqual("awaiting_service", result["test_state"]["workflow_status"])

    def test_report_writer_records_required_fields(self) -> None:
        fixture = TempRaphael()
        try:
            config = load_config(fixture.config)
            payload = {
                "response": "Hello Aaron. I'm online.",
                "intent": "greeting",
                "command": "",
                "status": "Success",
            }
            row = dashboard_chat_tests._record(
                "Basic health",
                "hello Raphael",
                "greeting",
                payload,
                True,
            )
            result = dashboard_chat_tests._save(config, [row], "Dashboard Chat Smoke Test Report")
            report = Path(result["report"])
            text = report.read_text(encoding="utf-8")
            for field in [
                "Input message:",
                "Expected route:",
                "Actual route:",
                "Status:",
                "Response snippet:",
                "Result:",
                "Timestamp:",
            ]:
                self.assertIn(field, text)
            self.assertTrue(Path(result["history"]).exists())
        finally:
            fixture.close()

    def test_dashboard_panel_and_api_routes_exist(self) -> None:
        text = Path("C:/RaphaelOS/dashboard/app.py").read_text(encoding="utf-8")
        self.assertIn("Dashboard Chat Tests", text)
        self.assertIn("Run smoke test", text)
        self.assertIn("View latest report", text)
        self.assertIn('"/api/dashboard-chat-tests/run"', text)
        self.assertIn('"/api/dashboard-chat-tests/report"', text)

    def test_cli_commands_are_registered(self) -> None:
        text = Path("raphael_core/legacy.py").read_text(encoding="utf-8")
        for command in [
            "dashboard-chat-smoke-test",
            "dashboard-chat-test",
            "dashboard-chat-test-suite",
            "dashboard-chat-test-report",
        ]:
            self.assertIn(command, text)
