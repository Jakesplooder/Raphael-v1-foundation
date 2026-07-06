from __future__ import annotations

import unittest

from raphael_core.config import load_config
from tests.support import TempRaphael


class ConfigTests(unittest.TestCase):
    def test_temp_config_preserves_required_safety_defaults(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            self.assertFalse(config.external_execution_enabled)
            self.assertTrue(config.n8n_allow_execution)
            self.assertFalse(config.n8n_store_credentials)
            self.assertTrue(config.internet_headless_search_enabled)
            self.assertTrue(config.internet_ai_overview_enabled)
            self.assertTrue(config.internet_ai_overview_default)
            self.assertEqual(3, config.internet_ai_overview_source_count)
            self.assertTrue(config.internet_ai_overview_include_sources)
            self.assertTrue(config.internet_raw_json_on_request_only)
            self.assertTrue(config.internet_analysis_with_pandas)
            self.assertEqual("http://127.0.0.1:8080", config.searxng_url)
            self.assertIn(os_fixture.vault.resolve(), config.approved_write_roots)
        finally:
            os_fixture.close()
