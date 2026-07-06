from __future__ import annotations

import json
import os
import unittest
from unittest.mock import patch

from raphael_core.config import load_config
from raphael_core.internet_access import (
    format_ai_overview,
    format_snippets,
    internet_request,
    internet_result,
    internet_root,
    internet_search,
    internet_source_review,
    internet_status_data,
    internet_headless_search,
    internet_latest_overview,
    internet_latest_snippets,
    internet_raw_result,
    internet_save_overview_to_knowledge,
    internet_analyze_results,
    internet_niche_score,
)
from tests.support import TempRaphael


class InternetAccessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        raw = json.loads(self.os.config.read_text(encoding="utf-8"))
        raw.update({
            "internet_access_enabled": True,
            "internet_requires_confirmation": True,
            "internet_provider": "manual_or_browser",
            "internet_save_sources": True,
            "internet_allow_autonomous_browsing": False,
            "internet_allow_account_login": False,
            "internet_allow_external_actions": False,
            "internet_max_sources_per_request": 10,
        })
        self.os.config.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def test_status_and_required_notes_exist(self) -> None:
        data = internet_status_data(self.config)
        self.assertTrue(data["enabled"])
        self.assertFalse(data["allow_autonomous_browsing"])
        root = internet_root(self.config)
        for name in [
            "Internet Access Overview.md",
            "Search Requests.md",
            "Search Results.md",
            "Source Review.md",
            "Internet Safety Policy.md",
            "Internet Brief.md",
        ]:
            self.assertTrue((root / name).exists(), name)

    def test_request_and_result_save_sources_and_uncertainty(self) -> None:
        request = internet_request(self.config, "Latest FastAPI documentation")
        result = internet_result(
            self.config,
            request["request_id"],
            "FastAPI documentation reviewed. https://fastapi.tiangolo.com/ "
            "Python documentation corroborates context. https://docs.python.org/3/",
        )
        self.assertEqual(2, result["source_count"])
        self.assertTrue(result["uncertainty"].startswith("Low"))
        status = internet_status_data(self.config)
        self.assertEqual(1, len(status["completed"]))
        self.assertEqual(2, len(status["sources"]))

    def test_search_requires_confirmation_and_never_claims_results(self) -> None:
        with (
            patch("raphael_core.legacy.sys.stdin.isatty", return_value=False),
            self.assertRaises(PermissionError),
        ):
            internet_search(self.config, "current Etsy trends")
        previous = os.environ.get("RAPHAEL_CONFIRMED")
        os.environ["RAPHAEL_CONFIRMED"] = "YES"
        try:
            with patch("raphael_core.internet_access.webbrowser.open", return_value=True):
                result = internet_search(self.config, "current Etsy trends")
        finally:
            if previous is None:
                os.environ.pop("RAPHAEL_CONFIRMED", None)
            else:
                os.environ["RAPHAEL_CONFIRMED"] = previous
        self.assertTrue(result["search_opened"])
        self.assertIn("No result is claimed", result["truthfulness"])

    def test_private_url_review_is_blocked(self) -> None:
        previous = os.environ.get("RAPHAEL_CONFIRMED")
        os.environ["RAPHAEL_CONFIRMED"] = "YES"
        try:
            with self.assertRaises(PermissionError):
                internet_source_review(self.config, "http://127.0.0.1:8787/api/health")
        finally:
            if previous is None:
                os.environ.pop("RAPHAEL_CONFIRMED", None)
            else:
                os.environ["RAPHAEL_CONFIRMED"] = previous

    def test_headless_search_saves_results_without_opening_browser(self) -> None:
        self.config.internet_provider = "searxng"
        self.config.internet_headless_search_enabled = True
        payload = {
            "results": [
                {
                    "title": "Camping shirts trend report",
                    "url": "https://example.com/camping-shirts",
                    "content": "Popular evergreen camping t-shirt gift niche with growing demand.",
                    "engine": "test",
                },
                {
                    "title": "Outdoor POD competition",
                    "url": "https://example.org/outdoor-pod",
                    "content": "Competitive marketplace but strong product fit for apparel.",
                    "engine": "test",
                },
            ]
        }

        class Response:
            status = 200
            def __enter__(self):
                return self
            def __exit__(self, *_args):
                return None
            def read(self):
                return json.dumps(payload).encode()

        with (
            patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}),
            patch("raphael_core.internet_access.urllib.request.urlopen", return_value=Response()),
            patch("raphael_core.internet_access.webbrowser.open") as browser,
        ):
            result = internet_headless_search(self.config, "camping POD shirt trends")
        self.assertFalse(result["browser_opened"])
        self.assertEqual(2, result["source_count"])
        browser.assert_not_called()
        status = internet_status_data(self.config)
        self.assertEqual(2, len(status["results"][0]["items"]))
        self.assertIn("ai_overview", status["results"][0])
        self.assertIn("Answer:", format_ai_overview(status["results"][0]["ai_overview"]))
        analysis = internet_analyze_results(self.config, result["request_id"])
        self.assertEqual(2, analysis["rows"])
        score = internet_niche_score(self.config, result["request_id"])
        self.assertIn("overall_niche_score", score)

    def test_latest_overview_snippets_raw_and_knowledge_save(self) -> None:
        self.config.internet_provider = "searxng"
        self.config.internet_headless_search_enabled = True
        payload = {
            "results": [
                {
                    "title": "The White House",
                    "url": "https://www.whitehouse.gov/administration/",
                    "content": "The President is Jane Example. Official White House administration page.",
                    "engine": "test",
                },
                {
                    "title": "Government biography",
                    "url": "https://www.usa.gov/presidents",
                    "content": "Official government source about the current president.",
                    "engine": "test",
                },
                {
                    "title": "Reference profile",
                    "url": "https://example.com/president",
                    "content": "Background profile corroborating the officeholder.",
                    "engine": "test",
                },
            ]
        }

        class Response:
            status = 200
            def __enter__(self):
                return self
            def __exit__(self, *_args):
                return None
            def read(self):
                return json.dumps(payload).encode()

        with (
            patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}),
            patch("raphael_core.internet_access.urllib.request.urlopen", return_value=Response()),
        ):
            result = internet_headless_search(self.config, "who is president")
        overview = internet_latest_overview(self.config)
        self.assertEqual(result["request_id"], overview["request_id"])
        self.assertIn("president", overview["answer"].lower())
        snippets = internet_latest_snippets(self.config)
        self.assertEqual(3, len(snippets["snippets"]))
        self.assertIn("The White House", format_snippets(snippets))
        raw = internet_raw_result(self.config, "LATEST")
        self.assertEqual(3, raw["source_count"])
        self.assertEqual(3, len(raw["items"]))
        saved = internet_save_overview_to_knowledge(self.config, "LATEST")
        self.assertTrue(saved.exists())
