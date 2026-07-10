from __future__ import annotations

import unittest

from raphael_core.builder import (
    builder_safe_write_path,
    classify_build_request,
    create_build_request,
    generate_build_files,
)
from raphael_core.config import load_config
from raphael_core.markdown import section_value
from tests.support import TempRaphael

from unittest.mock import patch
from raphael_core.llm.providers.base_provider import ReasoningResult

class BuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def test_complexity_classification(self) -> None:
        self.assertEqual(1, classify_build_request("simple click counter")["complexity_level"])
        self.assertEqual(2, classify_build_request("internal CRUD dashboard app")["complexity_level"])
        self.assertEqual(3, classify_build_request("SaaS marketplace with users and payments")["complexity_level"])

    @patch("raphael_core.builder_engine.OllamaProvider.reason")
    def test_builder_outputs_stay_in_workspace(self, mock_reason) -> None:
        mock_reason.return_value = ReasoningResult(
            provider_name="mock",
            model_name="mock",
            response='{"index.html": "<html></html>", "app.py": "print(1)"}',
            latency_sec=0.1,
            token_count=10,
            raw_output={}
        )
        request = create_build_request(self.config, "simple click counter")
        build_id = section_value(request.read_text(encoding="utf-8"), "Build Request ID")
        workspace = generate_build_files(self.config, build_id)
        self.assertEqual(self.os.builder_workspace.resolve(), workspace.resolve().parent)
        with self.assertRaises(PermissionError):
            builder_safe_write_path(self.config, self.os.root / "outside-builder" / "app.py")
