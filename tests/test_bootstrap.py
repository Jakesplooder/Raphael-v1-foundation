from __future__ import annotations

import json
from pathlib import Path
import unittest
from unittest.mock import patch

from raphael_core.bootstrap import (
    _stop_managed_service,
    bootstrap_health_data,
    bootstrap_start,
    bootstrap_status_text,
    pid_registry_path,
)
from raphael_core.config import load_config
from tests.support import TempRaphael


class BootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        raw = json.loads(self.os.config.read_text(encoding="utf-8"))
        raw.update(
            {
                "bootstrap_enabled": True,
                "bootstrap_open_dashboard_on_start": False,
                "bootstrap_generate_morning_brief": False,
                "bootstrap_start_dashboard": False,
                "bootstrap_start_voice_gateway": False,
                "bootstrap_start_comfyui": False,
                "bootstrap_comfyui_root": str(self.os.root / "ComfyUI"),
                "bootstrap_comfyui_python": str(self.os.root / "ComfyUI" / "python.exe"),
            }
        )
        self.os.config.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def test_status_health_and_disabled_start_are_safe(self) -> None:
        with patch("raphael_core.bootstrap._http", return_value=(False, "offline", None)):
            data = bootstrap_health_data(self.config)
            result = bootstrap_start(self.config, open_browser=False)
        self.assertIn("Raphael Bootstrap Status", bootstrap_status_text(self.config))
        self.assertTrue((self.os.vault / "00_Raphael" / "System Bootstrap" / "Bootstrap Health.md").exists())
        self.assertTrue(pid_registry_path(self.config).exists())
        self.assertEqual({}, json.loads(pid_registry_path(self.config).read_text(encoding="utf-8"))["services"])
        self.assertTrue(all(row["result"] == "Disabled by config" for row in result["results"]))
        self.assertIn("groups", data)

    def test_ownership_mismatch_never_calls_taskkill(self) -> None:
        record = {"pid": 999999, "creation_time": 1}
        with patch("raphael_core.bootstrap.subprocess.run") as run:
            result = _stop_managed_service(self.config, "dashboard", record)
        self.assertEqual("Not running or ownership mismatch", result["result"])
        run.assert_not_called()

    def test_launcher_scripts_exist(self) -> None:
        names = [
            "start_raphael.ps1",
            "stop_raphael.ps1",
            "restart_raphael.ps1",
            "health_check.ps1",
            "open_dashboard.ps1",
            "install_startup_task.ps1",
            "remove_startup_task.ps1",
        ]
        for name in names:
            self.assertTrue((Path("C:/RaphaelOS/launcher") / name).exists(), name)

