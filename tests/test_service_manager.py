from __future__ import annotations

import json
import unittest
from unittest.mock import patch

from raphael_core.config import load_config
from raphael_core.service_manager import (
    registry_path,
    restart_service,
    service_health,
    service_list,
    service_status,
    start_service,
    stop_service,
)
from tests.support import TempRaphael


class ServiceManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def test_registry_list_and_status_exist(self) -> None:
        rows = service_list(self.config)
        self.assertTrue(registry_path(self.config).exists())
        self.assertTrue({"dashboard", "comfyui", "ollama", "qdrant", "voice_gateway"}.issubset(
            {row["service_id"] for row in rows}
        ))
        with patch("raphael_core.service_manager._health_url", return_value=(False, "offline")):
            data = service_status(self.config)
        self.assertEqual(len(rows), len(data["services"]))

    def test_duplicate_start_does_not_spawn(self) -> None:
        with (
            patch("raphael_core.service_manager.service_health", return_value={
                "healthy": True, "managed": False, "pid": None
            }),
            patch("raphael_core.service_manager.bootstrap._spawn_service") as spawn,
        ):
            result = start_service(self.config, "comfyui")
        self.assertEqual("already_running", result["results"][0]["result"])
        spawn.assert_not_called()

    def test_stop_never_kills_unmanaged_service(self) -> None:
        with patch("raphael_core.service_manager.bootstrap._stop_managed_service") as stop:
            result = stop_service(self.config, "comfyui")
        self.assertEqual("not_managed", result["results"][0]["result"])
        stop.assert_not_called()

    def test_restart_never_adopts_or_restarts_unmanaged_service(self) -> None:
        with (
            patch("raphael_core.service_manager.bootstrap._managed_record_alive", return_value=False),
            patch("raphael_core.service_manager.stop_service") as stop,
            patch("raphael_core.service_manager.start_service") as start,
        ):
            result = restart_service(self.config, "comfyui", confirmed=True)
        self.assertEqual("not_managed", result["results"][0]["result"])
        self.assertIn("Use Start instead", result["results"][0]["error"])
        stop.assert_not_called()
        start.assert_not_called()

    def test_url_health_reports_reachable_service(self) -> None:
        with patch("raphael_core.service_manager._health_url", return_value=(True, "HTTP 200")):
            result = service_health(self.config, "comfyui")
        self.assertTrue(result["healthy"])
        self.assertEqual("external", result["status"])

    def test_registry_contains_no_credentials(self) -> None:
        text = json.dumps(service_list(self.config)).lower()
        for key in ["password", "api_key", "secret", "token"]:
            self.assertNotIn(f'"{key}"', text)

    def test_qdrant_service_actions_delegate_to_docker_allowlist(self) -> None:
        self.config.docker_enabled = True
        with patch(
            "raphael_core.docker_manager.docker_start",
            return_value={"service_id": "qdrant", "result": "started", "error": ""},
        ) as start:
            result = start_service(self.config, "qdrant", confirmed=True)
        self.assertEqual("started", result["results"][0]["result"])
        start.assert_called_once_with(self.config, "qdrant", confirmed=True)
