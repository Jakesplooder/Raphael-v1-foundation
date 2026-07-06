from __future__ import annotations

import unittest

from tests.support import TempRaphael


class CliSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.os = TempRaphael()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.os.close()

    def test_required_smoke_commands(self) -> None:
        commands = [
            ("system-check",),
            ("command-bus-status",),
            ("executive-brief",),
            ("notification-status",),
            ("activity-status",),
            ("portfolio-status",),
            ("finance-status",),
            ("knowledge-review",),
            ("deliberation-status",),
            ("execution-plan-review",),
            ("pod-status",),
            ("pod-typography-status",),
            ("pod-typography-review",),
            ("pod-workflow-status",),
            ("pod-template-status",),
            ("pod-template-inspect", "flux"),
            ("pod-template-inspect", "sdxl"),
            ("n8n-status",),
            ("asset-status",),
            ("build-task-review",),
            ("daily-start",),
            ("daily-focus",),
            ("daily-plan",),
            ("daily-checkin", "Smoke test check-in."),
            ("daily-end",),
            ("daily-review",),
            ("bootstrap-status",),
            ("bootstrap-health",),
            ("bootstrap-review",),
            ("internet-status",),
            ("internet-review",),
            ("internet-brief",),
            ("pandas-status",),
            ("searxng-status",),
            ("workflow-runner-status",),
            ("workflow-list",),
            ("workflow-failures",),
            ("workflow-review",),
            ("docker-status",),
            ("docker-list",),
            ("docker-health",),
            ("docker-compose-plan",),
            ("docker-review",),
        ]
        failures: list[str] = []
        for command in commands:
            result = self.os.run(*command)
            if result.returncode != 0:
                failures.append(f"{' '.join(command)}: {result.stderr or result.stdout}")
        self.assertEqual([], failures)

    def test_representative_compatibility_commands(self) -> None:
        commands = [
            ("command-center",),
            ("deliberate", "Should I focus on Agency or Commerce?"),
            ("execution-plan", "Agency"),
            ("build-request", "simple react app"),
        ]
        for command in commands:
            with self.subTest(command=command):
                result = self.os.run(*command)
                self.assertEqual(0, result.returncode, result.stderr or result.stdout)
