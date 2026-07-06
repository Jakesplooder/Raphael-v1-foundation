from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


def load_dashboard_module():
    path = Path("C:/RaphaelOS/dashboard/app.py")
    spec = importlib.util.spec_from_file_location("dashboard_service_api_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeBus:
    def route(self, phrase, source, state):
        state["pending_confirmation_key"] = "CONFIRM-TEST"
        state["pending_command_bus_route"] = {"phrase": phrase}
        return {
            "status": "needs_confirmation",
            "confirmation_key": "CONFIRM-TEST",
            "spoken_response": "Confirmation required.",
            "matched_command": "python raphael.py service-start comfyui",
        }

    def confirm(self, key, state):
        if key != state.get("pending_confirmation_key"):
            return {"status": "error", "safety_reason": "No matching pending confirmation."}
        state.clear()
        return {
            "status": "routed",
            "spoken_response": "Started.",
            "matched_command": "python raphael.py service-start comfyui",
            "full_response": json.dumps({
                "action": "start",
                "results": [{"service_id": "comfyui", "result": "started", "pid": 4321}],
            }),
        }


class DashboardServiceApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dashboard = load_dashboard_module()

    def setUp(self):
        self.dashboard.SERVICE_COMMAND_BUS_SESSION.clear()

    def status_data(self, running=False):
        return {
            "services": [{
                "service_id": "comfyui",
                "display_name": "ComfyUI",
                "status": "running" if running else "stopped",
                "health": "healthy" if running else "unhealthy",
                "pid": 4321 if running else None,
            }]
        }

    def test_start_uses_command_bus_confirmation_then_returns_pid_and_health(self):
        bus_module = SimpleNamespace(RaphaelCommandBus=FakeBus)
        with (
            patch.object(self.dashboard, "load_command_bus", return_value=bus_module),
            patch.object(self.dashboard, "service_manager_data", side_effect=[
                self.status_data(False), self.status_data(False), self.status_data(True),
            ]),
        ):
            pending, pending_status = self.dashboard.service_bus_action("start", {"service_id": "comfyui"})
            completed, completed_status = self.dashboard.service_bus_action(
                "start", {"service_id": "comfyui", "confirmation_key": pending["confirmation_key"]}
            )
        self.assertEqual(202, pending_status)
        self.assertTrue(pending["confirmation_required"])
        self.assertEqual(200, completed_status)
        self.assertTrue(completed["ok"])
        self.assertEqual(4321, completed["service"]["pid"])
        self.assertEqual("healthy", completed["service"]["health"])

    def test_unknown_service_id_is_rejected_before_command_bus(self):
        with patch.object(self.dashboard, "service_manager_data", return_value=self.status_data(False)):
            result, status = self.dashboard.service_bus_action("start", {"service_id": "not_registered"})
        self.assertEqual(404, status)
        self.assertFalse(result["ok"])

    def test_required_explicit_routes_and_error_banner_exist(self):
        text = Path("C:/RaphaelOS/dashboard/app.py").read_text(encoding="utf-8")
        for route in [
            "/api/services/status",
            "/api/services/start",
            "/api/services/stop",
            "/api/services/restart",
            "/api/services/health",
            "/api/services/start-stack",
        ]:
            self.assertIn(f'"{route}"', text)
        self.assertIn("Pending confirmation", text)
        self.assertIn("Action started", text)
        self.assertIn("Service action failed", text)
        self.assertIn("refreshMaintenanceServices", text)
