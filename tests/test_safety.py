from __future__ import annotations

import unittest
from pathlib import Path
import hashlib
import os

from raphael_core.asset_library import asset_import
from raphael_core.config import load_config
from raphael_core.safety import ensure_safe_path
from tests.support import TempRaphael


class SafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def test_k_drive_is_not_writable(self) -> None:
        with self.assertRaises(PermissionError):
            ensure_safe_path(Path("K:/RaphaelSafetyProbe.txt"), self.config)

    def test_external_and_install_boundaries_remain_disabled(self) -> None:
        self.assertFalse(self.config.external_execution_enabled)
        self.assertFalse(self.config.safety.get("allow_install"))
        self.assertFalse(self.config.safety.get("allow_upload"))
        self.assertFalse(self.config.safety.get("allow_email"))
        self.assertTrue(self.config.internet_requires_confirmation)
        self.assertFalse(self.config.internet_allow_autonomous_browsing)
        self.assertFalse(self.config.internet_allow_account_login)
        self.assertFalse(self.config.internet_allow_external_actions)

    def test_command_bus_blocks_arbitrary_shell_and_publishing(self) -> None:
        result = self.os.run("command-bus-test", "run arbitrary shell command npm install and publish to Etsy")
        self.assertEqual(0, result.returncode)
        self.assertIn('"status": "blocked"', result.stdout)

    def test_local_pod_language_is_not_treated_as_money_movement(self) -> None:
        result = self.os.run("command-bus-test", "perform a local POD Studio test")
        self.assertEqual(0, result.returncode)
        self.assertNotIn("Spending or moving money is blocked", result.stdout)
        self.assertIn('"pod-workflow"', result.stdout)
        self.assertIn("Stage 1/13 complete", result.stdout)

    def test_asset_import_does_not_modify_original(self) -> None:
        original = self.os.root / "approved-read" / "sample.txt"
        original.parent.mkdir(parents=True, exist_ok=True)
        original.write_text("original asset content", encoding="utf-8")
        before = hashlib.sha256(original.read_bytes()).hexdigest()
        previous = os.environ.get("RAPHAEL_CONFIRMED")
        os.environ["RAPHAEL_CONFIRMED"] = "YES"
        try:
            output = asset_import(self.config, original)
        finally:
            if previous is None:
                os.environ.pop("RAPHAEL_CONFIRMED", None)
            else:
                os.environ["RAPHAEL_CONFIRMED"] = previous
        self.assertTrue(output.exists())
        self.assertEqual(before, hashlib.sha256(original.read_bytes()).hexdigest())
