from __future__ import annotations

import os
from pathlib import Path
import unittest
from unittest.mock import patch

from raphael_core.config import load_config
from raphael_core import pod_workflow
from tests.support import TempRaphael


class PodWorkflowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)

    def tearDown(self) -> None:
        self.os.close()

    def _note(self, relative: str, content: str = "") -> Path:
        path = self.os.vault / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_workflow_persists_ids_and_final_outputs(self) -> None:
        tool = self._note("tool.md")
        with patch("raphael_core.pod_workflow.legacy.pod_tool_status", return_value=tool):
            started = pod_workflow.pod_workflow(
                self.config,
                'Create a local POD shirt design with Flux and typography saying "WILD AND FREE"',
            )
        workflow_id = started["workflow_id"]
        self.assertEqual(1, started["completed_stage"])
        self.assertEqual("create concept", started["next_stage"])

        generated = self.os.runtime / "PODStudio" / "generated" / "PODGEN-REQ123"
        generated.mkdir(parents=True, exist_ok=True)
        image = generated / "design.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nimage")

        concept = self._note(
            "Concepts/PODCON-ABC123 - concept.md",
            "# Concept\n\n## Possible Phrases\n\n- WILD AND FREE\n",
        )
        prompt = self._note("Prompts/PODCON-ABC123 - Design Prompts.md")
        request = self._note(
            "Requests/PODGEN-REQ123 - request.md",
            f"# Request\n\n## Output Folder\n\n{generated}\n",
        )
        review = self._note(
            "Reviews/PODBATCH-BATCH123 - Batch Review.md",
            "# Review\n\n- PODREV-REV123\n",
        )
        typography = self._note("Typography/PODTYPE-TYPE123 - type.md")
        composition = self._note("Compositions/PODCOMP-COMP123 - composition.md")
        svg = self._note("Exports/PODCOMP-COMP123 - SVG.md", "# SVG\n\n## SVG Export\n\nC:/RaphaelOS/out/design.svg\n")
        print_note = self._note("Exports/PODCOMP-COMP123 - Print.md", "# Print\n\n## Print PNG\n\nC:/RaphaelOS/out/design.png\n")
        listing = self._note("Listings/PODCON-ABC123 - Listing Draft.md")
        package = self.os.runtime / "PODStudio" / "exports" / "PODCON-ABC123"
        package.mkdir(parents=True)

        side_effects = {
            "raphael_core.pod_workflow.legacy.pod_concept": concept,
            "raphael_core.pod_workflow.legacy.pod_prompt": prompt,
            "raphael_core.pod_workflow.legacy.pod_generation_request": request,
            "raphael_core.pod_workflow.legacy.pod_generate": request,
            "raphael_core.pod_workflow.legacy.pod_review_batch": review,
            "raphael_core.pod_workflow.typography.pod_typography_create": typography,
            "raphael_core.pod_workflow.typography.pod_compose_design": composition,
            "raphael_core.pod_workflow.typography.pod_svg_export": svg,
            "raphael_core.pod_workflow.typography.pod_print_export": print_note,
            "raphael_core.pod_workflow.legacy.pod_listing_draft": listing,
            "raphael_core.pod_workflow.legacy.pod_export_package": package,
        }
        patches = [patch(name, return_value=value) for name, value in side_effects.items()]
        for item in patches:
            item.start()
            self.addCleanup(item.stop)

        with patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}):
            result = None
            for _ in range(11):
                result = pod_workflow.pod_workflow_continue(self.config, workflow_id)

        self.assertEqual("completed", result["status"])
        shown = pod_workflow.pod_workflow_show(self.config, workflow_id)
        self.assertEqual("PODCON-ABC123", shown["ids"]["concept_id"])
        self.assertEqual("PODGEN-REQ123", shown["ids"]["generation_request_id"])
        self.assertEqual("PODREV-REV123", shown["ids"]["review_id"])
        self.assertEqual("PODTYPE-TYPE123", shown["ids"]["typography_id"])
        self.assertEqual("PODCOMP-COMP123", shown["ids"]["composition_id"])
        self.assertEqual("C:/RaphaelOS/out/design.svg", shown["outputs"]["svg_path"])
        self.assertEqual("C:/RaphaelOS/out/design.png", shown["outputs"]["print_png_path"])
        self.assertEqual(str(package), shown["outputs"]["export_package"])

    def test_continue_requires_confirmation(self) -> None:
        tool = self._note("tool.md")
        with patch("raphael_core.pod_workflow.legacy.pod_tool_status", return_value=tool):
            started = pod_workflow.pod_workflow(self.config, "POD shirt design")
        with self.assertRaises(PermissionError):
            pod_workflow.pod_workflow_continue(self.config, started["workflow_id"])

    def test_generation_stage_resumes_from_existing_images_without_resubmitting(self) -> None:
        tool = self._note("tool.md")
        with patch("raphael_core.pod_workflow.legacy.pod_tool_status", return_value=tool):
            started = pod_workflow.pod_workflow(self.config, "POD Flux shirt design")
        state = pod_workflow.pod_workflow_show(self.config, started["workflow_id"])
        folder = self.os.runtime / "PODStudio" / "generated" / "PODGEN-EXISTING"
        folder.mkdir(parents=True)
        image = folder / "existing.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nexisting")
        request_note = self._note("Requests/PODGEN-EXISTING - request.md")
        state["status"] = "blocked"
        state["completed_stage"] = 5
        state["next_stage"] = 6
        state["ids"]["generation_request_id"] = "PODGEN-EXISTING"
        state["outputs"]["generated_folder"] = str(folder)
        state["outputs"]["generation_request_note"] = str(request_note)
        pod_workflow._save(self.config, state)
        with (
            patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}),
            patch("raphael_core.pod_workflow.legacy.pod_generate") as generate,
        ):
            result = pod_workflow.pod_workflow_continue(self.config, started["workflow_id"])
        self.assertEqual(6, result["completed_stage"])
        self.assertEqual(str(image), result["outputs"]["selected_image"])
        generate.assert_not_called()

    def test_research_stage_uses_headless_search_and_scores_before_concept(self) -> None:
        tool = self._note("tool.md")
        with patch("raphael_core.pod_workflow.legacy.pod_tool_status", return_value=tool):
            started = pod_workflow.pod_workflow(self.config, "Research current POD camping shirt trends")
        self.assertEqual("internet research", started["next_stage"])
        with (
            patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}),
            patch("raphael_core.pod_workflow.internet_access.internet_headless_search", return_value={"request_id": "INET-TEST"}) as search,
            patch("raphael_core.pod_workflow.internet_access.internet_analyze_results", return_value={"rows": 8}) as analyze,
            patch("raphael_core.pod_workflow.internet_access.internet_niche_score", return_value={"overall_niche_score": 81}) as score,
        ):
            result = pod_workflow.pod_workflow_continue(self.config, started["workflow_id"])
        self.assertEqual(2, result["completed_stage"])
        self.assertEqual("create concept", result["next_stage"])
        self.assertEqual("INET-TEST", result["ids"]["internet_request_id"])
        self.assertEqual("81", result["outputs"]["niche_score"])
        search.assert_called_once()
        analyze.assert_called_once_with(self.config, "INET-TEST")
        score.assert_called_once_with(self.config, "INET-TEST")
