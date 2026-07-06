from __future__ import annotations

import datetime as dt
import unittest

from raphael_core.config import load_config
from raphael_core.daily import (
    daily_checkin,
    daily_end,
    daily_focus,
    daily_plan,
    daily_review,
    daily_start,
)
from raphael_core.tasks import all_agent_tasks
from tests.support import TempRaphael


class DailyOperatingLoopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def test_daily_loop_generates_notes_without_creating_tasks(self) -> None:
        before = len(all_agent_tasks(self.config))
        outputs = [
            daily_start(self.config),
            daily_focus(self.config),
            daily_plan(self.config),
            daily_checkin(self.config, "Finished the first focus block; no blocker."),
            daily_end(self.config),
            daily_review(self.config),
        ]
        after = len(all_agent_tasks(self.config))

        self.assertEqual(before, after)
        self.assertTrue(all(path.exists() for path in outputs))
        self.assertTrue(all(self.os.vault.resolve() in path.resolve().parents for path in outputs))
        self.assertIn("advisory", outputs[0].read_text(encoding="utf-8").lower())
        self.assertIn("Finished the first focus block", outputs[3].read_text(encoding="utf-8"))

    def test_cli_daily_commands(self) -> None:
        commands = [
            ("daily-start",),
            ("daily-focus",),
            ("daily-plan",),
            ("daily-checkin", "Priority moved; waiting on a decision."),
            ("daily-end",),
            ("daily-review",),
        ]
        for command in commands:
            with self.subTest(command=command):
                result = self.os.run(*command)
                self.assertEqual(0, result.returncode, result.stderr or result.stdout)

        date = dt.date.today().isoformat()
        self.assertTrue(
            (self.os.vault / "00_Raphael" / "Daily Operating Loop" / f"{date} Daily Start.md").exists()
        )
