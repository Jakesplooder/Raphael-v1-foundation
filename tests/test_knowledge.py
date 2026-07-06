from __future__ import annotations

import unittest

from raphael_core.config import load_config
from raphael_core.knowledge import knowledge_review
from tests.support import TempRaphael


class KnowledgeTests(unittest.TestCase):
    def test_knowledge_review_stays_in_temp_vault(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            output = knowledge_review(config).resolve()
            self.assertIn(config.vault.resolve(), output.parents)
        finally:
            os_fixture.close()
