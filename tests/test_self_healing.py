from __future__ import annotations

import datetime as dt
import json
import unittest
from unittest.mock import patch

from raphael_core.config import load_config
from raphael_core import self_healing
from raphael_core.pod_workflow import workflow_root
from tests.support import TempRaphael


class SelfHealingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def _patch_observation_dependencies(self):
        return (
            patch("raphael_core.self_healing.service_manager.service_status", return_value={"services": []}),
            patch("raphael_core.self_healing.docker_manager.docker_list", return_value={"docker": {"available": False}, "services": []}),
            patch("raphael_core.self_healing.workflow_runner.runner_status", return_value={"enabled": True}),
            patch("raphael_core.self_healing.workflow_runner.executions", return_value=[]),
            patch("raphael_core.self_healing.shutil_which", return_value=None),
        )

    def test_observe_system_writes_notes_and_runtime_observation(self) -> None:
        with self._patch_observation_dependencies()[0], self._patch_observation_dependencies()[1], self._patch_observation_dependencies()[2], self._patch_observation_dependencies()[3], self._patch_observation_dependencies()[4], patch("raphael_core.self_healing._http_ok", return_value=(True, "HTTP 200")), patch("raphael_core.self_healing._tcp_ok", return_value=(True, "reachable")):
            result = self_healing.observe_system(self.config)
        self.assertTrue(result["observation_id"].startswith("OBS-"))
        self.assertTrue((self.config.vault / "00_Raphael" / "Self Healing" / "Health Observations.md").exists())
        self.assertTrue((self.config.os_root / "self_healing" / "observations").exists())

    def test_detect_issues_finds_offline_comfyui(self) -> None:
        def health(url: str, timeout: float = 2.0):
            if "8188" in url:
                return False, "connection refused"
            return True, "HTTP 200"

        with self._patch_observation_dependencies()[0], self._patch_observation_dependencies()[1], self._patch_observation_dependencies()[2], self._patch_observation_dependencies()[3], self._patch_observation_dependencies()[4], patch("raphael_core.self_healing._http_ok", side_effect=health), patch("raphael_core.self_healing._tcp_ok", return_value=(True, "reachable")):
            issues = self_healing.detect_issues(self.config)
        kinds = {row["kind"] for row in issues["issues"]}
        self.assertIn("comfyui_offline", kinds)
        issue = next(row for row in issues["issues"] if row["kind"] == "comfyui_offline")
        self.assertEqual("approval_required", issue["repairability"])
        self.assertIn("service-start comfyui", issue["related_command"])

    def test_repair_plan_and_run_require_approval(self) -> None:
        issue = self_healing._issue(
            "comfyui_offline",
            "warning",
            "Comfyui",
            ["offline"],
            "connection refused",
            ["refused"],
            "start ComfyUI through Service Manager",
            "approval_required",
            "low",
            "python raphael.py service-start comfyui",
        )
        issue["issue_id"] = "ISSUE-20260624-ABCDEF12"
        root = self.config.os_root / "self_healing" / "issues"
        root.mkdir(parents=True, exist_ok=True)
        (root / "active_issues.json").write_text(json.dumps({"issues": [issue]}), encoding="utf-8")
        plan = self_healing.repair_plan(self.config, issue["issue_id"])
        with self.assertRaises(PermissionError):
            self_healing.repair_run(self.config, plan["repair_id"])
        approved = self_healing.repair_approve(self.config, plan["repair_id"])
        self.assertTrue(approved["approved"])
        with patch("raphael_core.self_healing.service_manager.start_service", return_value={"action": "start", "results": [{"service_id": "comfyui", "result": "started"}]}) as start:
            ran = self_healing.repair_run(self.config, plan["repair_id"])
        self.assertEqual("completed", ran["status"])
        start.assert_called_once_with(self.config, "comfyui", confirmed=True)

    def test_stale_confirmation_detection_works(self) -> None:
        old = (dt.datetime.now() - dt.timedelta(days=2)).isoformat(timespec="seconds")
        workflow_root(self.config).mkdir(parents=True, exist_ok=True)
        (workflow_root(self.config) / "PODFLOW-20260624-ABCDEF12.json").write_text(json.dumps({
            "workflow_id": "PODFLOW-20260624-ABCDEF12",
            "status": "awaiting_confirmation",
            "created": old,
            "updated": old,
            "last_error": "",
            "completed_stage": 1,
            "next_stage": 3,
            "ids": {},
            "outputs": {},
        }), encoding="utf-8")
        with self._patch_observation_dependencies()[0], self._patch_observation_dependencies()[1], self._patch_observation_dependencies()[2], self._patch_observation_dependencies()[3], self._patch_observation_dependencies()[4], patch("raphael_core.self_healing._http_ok", return_value=(True, "HTTP 200")), patch("raphael_core.self_healing._tcp_ok", return_value=(True, "reachable")):
            issues = self_healing.detect_issues(self.config)
        self.assertIn("stale_confirmation_token", {row["kind"] for row in issues["issues"]})

    def test_failed_pod_workflow_detection_works(self) -> None:
        workflow_root(self.config).mkdir(parents=True, exist_ok=True)
        (workflow_root(self.config) / "PODFLOW-20260624-BCDEF123.json").write_text(json.dumps({
            "workflow_id": "PODFLOW-20260624-BCDEF123",
            "status": "failed",
            "created": dt.datetime.now().isoformat(timespec="seconds"),
            "updated": dt.datetime.now().isoformat(timespec="seconds"),
            "last_error": "ComfyUI readiness check failed",
            "completed_stage": 5,
            "next_stage": 6,
            "ids": {},
            "outputs": {},
        }), encoding="utf-8")
        with self._patch_observation_dependencies()[0], self._patch_observation_dependencies()[1], self._patch_observation_dependencies()[2], self._patch_observation_dependencies()[3], self._patch_observation_dependencies()[4], patch("raphael_core.self_healing._http_ok", return_value=(True, "HTTP 200")), patch("raphael_core.self_healing._tcp_ok", return_value=(True, "reachable")):
            issues = self_healing.detect_issues(self.config)
        kinds = {row["kind"] for row in issues["issues"]}
        self.assertIn("failed_pod_workflow_stage", kinds)
        self.assertIn("workflow_stuck_awaiting_service", kinds)


if __name__ == "__main__":
    unittest.main()
