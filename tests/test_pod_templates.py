from __future__ import annotations

import json
import unittest

from raphael_core.config import load_config
from raphael_core.pod_templates import inspect_template, template_status
from tests.support import TempRaphael


def workflow(checkpoint: str, latent_type: str = "EmptyLatentImage") -> dict:
    return {
        "nodes": [
            {"id": 1, "type": "CheckpointLoaderSimple", "inputs": [], "outputs": [], "widgets_values": [checkpoint]},
            {"id": 2, "type": "CLIPTextEncode", "inputs": [{"name": "clip", "link": 10}], "outputs": [], "widgets_values": ["positive"]},
            {"id": 3, "type": "CLIPTextEncode", "inputs": [{"name": "clip", "link": 11}], "outputs": [], "widgets_values": ["negative"]},
            {"id": 4, "type": latent_type, "inputs": [], "outputs": [], "widgets_values": [1024, 1024, 1]},
            {"id": 5, "type": "KSampler", "inputs": [
                {"name": "positive", "link": 12},
                {"name": "negative", "link": 13},
            ], "outputs": [], "widgets_values": []},
            {"id": 6, "type": "SaveImage", "inputs": [], "outputs": [], "widgets_values": ["RaphaelPOD"]},
        ],
        "links": [
            [10, 1, 1, 2, 0, "CLIP"],
            [11, 1, 1, 3, 0, "CLIP"],
            [12, 2, 0, 5, 1, "CONDITIONING"],
            [13, 3, 0, 5, 2, "CONDITIONING"],
        ],
    }


class PodTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)
        self.root = self.os.runtime / "PODStudio" / "templates"
        self.root.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        self.os.close()

    def test_ready_templates_report_required_nodes(self) -> None:
        (self.root / "flux_schnell_workflow.json").write_text(
            json.dumps(workflow("flux1-schnell-fp8.safetensors", "EmptySD3LatentImage")),
            encoding="utf-8",
        )
        (self.root / "SDXL_workflow.json").write_text(
            json.dumps(workflow("sd_xl_base_1.0.safetensors")),
            encoding="utf-8",
        )
        flux = inspect_template(self.config, "flux")
        self.assertEqual("READY", flux["status"])
        self.assertEqual(1, flux["checkpoint_node_id"])
        self.assertEqual(2, flux["positive_prompt_node_id"])
        self.assertEqual(3, flux["negative_prompt_node_id"])
        self.assertEqual(6, flux["save_image_node_id"])
        self.assertEqual(4, flux["width_height_node_id"])
        self.assertTrue(flux["flux_clip_connected_to_both_prompts"])
        self.assertEqual("READY", template_status(self.config)["status"])

    def test_flux_fails_when_checkpoint_clip_does_not_feed_both_prompts(self) -> None:
        data = workflow("flux1-schnell-fp8.safetensors", "EmptySD3LatentImage")
        data["links"][1] = [11, 99, 1, 3, 0, "CLIP"]
        (self.root / "flux_schnell_workflow.json").write_text(json.dumps(data), encoding="utf-8")
        result = inspect_template(self.config, "flux")
        self.assertEqual("FAILED", result["status"])
        self.assertIn("negative prompt node 3", result["reason"])

    def test_invalid_json_reports_exact_location(self) -> None:
        (self.root / "SDXL_workflow.json").write_text('{"nodes": [}', encoding="utf-8")
        result = inspect_template(self.config, "sdxl")
        self.assertEqual("FAILED", result["status"])
        self.assertIn("line 1", result["reason"])
