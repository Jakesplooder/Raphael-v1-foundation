from __future__ import annotations

import unittest

from raphael_core import pandas_analysis
from raphael_core.config import load_config
from tests.support import TempRaphael


class PandasAnalysisTests(unittest.TestCase):
    def test_status_and_csv_analysis(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            status = pandas_analysis.pandas_status()
            self.assertEqual("READY", status["status"])
            csv_path = os_fixture.root / "research.csv"
            csv_path.write_text("niche,demand,competition\ncamping,82,55\npets,90,80\n", encoding="utf-8")
            result = pandas_analysis.analyze_csv(config, csv_path)
            self.assertEqual(2, result["rows"])
            self.assertIn("demand", result["numeric_summary"])
        finally:
            os_fixture.close()
