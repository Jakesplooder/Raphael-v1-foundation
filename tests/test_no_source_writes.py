from __future__ import annotations

import unittest

from tests.support import TempRaphael, source_hashes


class NoSourceWriteTests(unittest.TestCase):
    def test_status_and_review_commands_do_not_modify_source_files(self) -> None:
        before = source_hashes()
        os_fixture = TempRaphael()
        try:
            for command in [
                ("pod-status",),
                ("n8n-status",),
                ("asset-status",),
                ("build-task-review",),
                ("command-bus-test", "publish this app to Etsy"),
            ]:
                result = os_fixture.run(*command)
                self.assertEqual(0, result.returncode, result.stderr or result.stdout)
        finally:
            os_fixture.close()
        self.assertEqual(before, source_hashes())
