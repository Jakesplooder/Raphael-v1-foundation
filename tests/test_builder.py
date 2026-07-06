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

    def test_builder_outputs_stay_in_workspace(self) -> None:
        request = create_build_request(self.config, "simple click counter")
        build_id = section_value(request.read_text(encoding="utf-8"), "Build Request ID")
        workspace = generate_build_files(self.config, build_id)
        self.assertEqual(self.os.builder_workspace.resolve(), workspace.resolve().parent)
        with self.assertRaises(PermissionError):
            builder_safe_write_path(self.config, self.os.root / "outside-builder" / "app.py")
