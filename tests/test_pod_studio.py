from __future__ import annotations

import json
import io
import os
from pathlib import Path
import urllib.error
import unittest
from unittest.mock import patch

from raphael_core.config import load_config
from raphael_core import legacy
from raphael_core.pod_studio import (
    pod_concept,
    pod_generate,
    pod_generation_request,
    pod_ocr_typography_scan,
    pod_prompt_specs,
    pod_review_design,
    pod_runtime_root,
    pod_status_text,
    pod_tool_status,
)
from tests.support import TempRaphael


class FakeResponse:
    def __init__(self, payload: object = None, raw: bytes | None = None) -> None:
        self.payload = payload
        self.raw = raw

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self) -> bytes:
        if self.raw is not None:
            return self.raw
        return json.dumps(self.payload).encode("utf-8")


class PodStudioTests(unittest.TestCase):
    @staticmethod
    def flux_ui_template() -> dict:
        return {
            "nodes": [
                {"id": 30, "type": "CheckpointLoaderSimple", "inputs": [], "widgets_values": ["flux1-schnell-fp8.safetensors"]},
                {"id": 6, "type": "CLIPTextEncode", "inputs": [{"name": "clip", "link": 45}], "widgets_values": ["old positive"]},
                {"id": 33, "type": "CLIPTextEncode", "inputs": [{"name": "clip", "link": 54}], "widgets_values": ["old negative"]},
                {"id": 27, "type": "EmptySD3LatentImage", "inputs": [], "widgets_values": [512, 512, 1]},
                {"id": 31, "type": "KSampler", "inputs": [
                    {"name": "model", "link": 47},
                    {"name": "positive", "link": 58},
                    {"name": "negative", "link": 55},
                    {"name": "latent_image", "link": 51},
                ], "widgets_values": [1, "randomize", 4, 1.0, "euler", "simple", 1.0]},
                {"id": 8, "type": "VAEDecode", "inputs": [{"name": "samples", "link": 52}, {"name": "vae", "link": 46}], "widgets_values": []},
                {"id": 9, "type": "SaveImage", "inputs": [{"name": "images", "link": 9}], "widgets_values": ["ComfyUI"]},
                {"id": 39, "type": "CheckpointLoaderSimple", "inputs": [], "widgets_values": ["disconnected-missing.safetensors"]},
            ],
            "links": [
                [45, 30, 1, 6, 0, "CLIP"], [54, 30, 1, 33, 0, "CLIP"],
                [47, 30, 0, 31, 0, "MODEL"], [58, 6, 0, 31, 1, "CONDITIONING"],
                [55, 33, 0, 31, 2, "CONDITIONING"], [51, 27, 0, 31, 3, "LATENT"],
                [52, 31, 0, 8, 0, "LATENT"], [46, 30, 2, 8, 1, "VAE"],
                [9, 8, 0, 9, 0, "IMAGE"],
            ],
        }

    def test_pod_runtime_is_under_runtime_root(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            root = pod_runtime_root(config).resolve()
            self.assertIn(config.os_root.resolve(), root.parents)
            self.assertIn("POD Design Studio Status", pod_status_text(config))
        finally:
            os_fixture.close()

    def test_generation_prompts_enforce_no_typography_directives(self) -> None:
        concept = """## Product Idea

Original mountain emblem

## Visual Style

Bold vintage screen print

## Color Palette

- black
- cream
"""
        specs = pod_prompt_specs(concept)
        for spec in specs:
            if spec["model"] not in {"flux", "sdxl"}:
                continue
            positive = str(spec["positive"])
            for directive in ["NO TEXT", "NO LETTERS", "NO WORDS", "NO TYPOGRAPHY", "NO WRITING", "NO LOGOS"]:
                self.assertIn(directive, positive)
        self.assertNotIn("Typography", {str(spec["name"]) for spec in specs})

    def test_comfyui_bridge_copies_reported_image_to_request_folder(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            concept_path = pod_concept(config, "4th of July original fireworks shirt")
            concept_id = concept_path.name.split(" ", 1)[0]
            request_path = pod_generation_request(config, concept_id, "sdxl")
            request_id = request_path.name.split(" ", 1)[0]

            def fake_urlopen(request, timeout=0):
                url = request.full_url if hasattr(request, "full_url") else str(request)
                if "/object_info/CheckpointLoaderSimple" in url:
                    return FakeResponse({
                        "CheckpointLoaderSimple": {
                            "input": {"required": {"ckpt_name": [["sd_xl_base_1.0.safetensors"]]}}
                        }
                    })
                if url.endswith("/prompt"):
                    return FakeResponse({"prompt_id": "prompt-test-1"})
                if "/history/prompt-test-1" in url:
                    return FakeResponse({
                        "prompt-test-1": {
                            "outputs": {
                                "7": {"images": [{"filename": "RaphaelPOD_test_00001_.png", "subfolder": "", "type": "output"}]}
                            },
                            "status": {"messages": []},
                        }
                    })
                if "/view?" in url:
                    return FakeResponse(raw=b"\x89PNG\r\n\x1a\nmock-image")
                raise AssertionError(f"Unexpected URL: {url}")

            with patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}), patch(
                "raphael_core.legacy.urllib.request.urlopen", side_effect=fake_urlopen
            ), patch(
                "raphael_core.legacy.pod_ocr_typography_scan",
                return_value={"available": True, "detected": False, "rejected": False, "max_confidence": 0, "tokens": [], "penalty": 0, "status": "No typography detected."},
            ):
                result = pod_generate(config, request_id)

            generated = os_fixture.runtime / "PODStudio" / "generated" / request_id
            images = list(generated.glob("*.png"))
            self.assertEqual(1, len(images))
            text = result.read_text(encoding="utf-8")
            self.assertIn("\nGenerated\n", text)
            self.assertIn("prompt-test-1", text)
            self.assertIn(str(images[0]), text)
        finally:
            os_fixture.close()

    def test_empty_comfyui_output_is_failed_not_generated(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            concept_path = pod_concept(config, "original simple camping badge")
            concept_id = concept_path.name.split(" ", 1)[0]
            request_path = pod_generation_request(config, concept_id, "sdxl")
            request_id = request_path.name.split(" ", 1)[0]

            def fake_urlopen(request, timeout=0):
                url = request.full_url if hasattr(request, "full_url") else str(request)
                if "/object_info/CheckpointLoaderSimple" in url:
                    return FakeResponse({
                        "CheckpointLoaderSimple": {
                            "input": {"required": {"ckpt_name": [["sd_xl_base_1.0.safetensors"]]}}
                        }
                    })
                if url.endswith("/prompt"):
                    return FakeResponse({"prompt_id": "prompt-empty"})
                if "/history/prompt-empty" in url:
                    return FakeResponse({
                        "prompt-empty": {
                            "outputs": {},
                            "status": {"messages": [["execution_error", {"exception_message": "No image output"}]]},
                        }
                    })
                raise AssertionError(f"Unexpected URL: {url}")

            with patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}), patch(
                "raphael_core.legacy.urllib.request.urlopen", side_effect=fake_urlopen
            ):
                with self.assertRaises(RuntimeError):
                    pod_generate(config, request_id)

            text = request_path.read_text(encoding="utf-8")
            self.assertIn("\nFailed\n", text)
            self.assertNotIn("\nGenerated\n", text)
            self.assertIn("No image output", text)
        finally:
            os_fixture.close()

    def test_high_confidence_ocr_rejects_generated_image_and_requires_regeneration(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            concept_path = pod_concept(config, "original camping illustration")
            concept_id = concept_path.name.split(" ", 1)[0]
            request_path = pod_generation_request(config, concept_id, "sdxl")
            request_id = request_path.name.split(" ", 1)[0]

            def fake_urlopen(request, timeout=0):
                url = request.full_url if hasattr(request, "full_url") else str(request)
                if "/object_info/CheckpointLoaderSimple" in url:
                    return FakeResponse({"CheckpointLoaderSimple": {"input": {"required": {"ckpt_name": [["sd_xl_base_1.0.safetensors"]]}}}})
                if url.endswith("/prompt"):
                    return FakeResponse({"prompt_id": "prompt-text"})
                if "/history/prompt-text" in url:
                    return FakeResponse({"prompt-text": {"outputs": {"7": {"images": [{"filename": "text.png", "subfolder": "", "type": "output"}]}}, "status": {"messages": []}}})
                if "/view?" in url:
                    return FakeResponse(raw=b"\x89PNG\r\n\x1a\nmock-image")
                raise AssertionError(f"Unexpected URL: {url}")

            scan = {
                "available": True,
                "detected": True,
                "rejected": True,
                "max_confidence": 96.5,
                "tokens": [{"text": "SALE", "confidence": 96.5}],
                "penalty": 40,
                "status": "Typography contamination detected.",
            }
            with patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}), patch(
                "raphael_core.legacy.urllib.request.urlopen", side_effect=fake_urlopen
            ), patch("raphael_core.legacy.pod_ocr_typography_scan", return_value=scan):
                with self.assertRaisesRegex(RuntimeError, "Typography contamination detected"):
                    pod_generate(config, request_id)

            text = request_path.read_text(encoding="utf-8")
            self.assertIn("\nRejected\n", text)
            self.assertIn("Typography contamination detected.", text)
            self.assertIn("Regeneration required", text)
            self.assertNotIn("\nGenerated\n", text)
        finally:
            os_fixture.close()

    def test_flux_ui_template_is_converted_and_submitted_payload_is_saved(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            template = os_fixture.runtime / "PODStudio" / "templates" / "flux_schnell_workflow.json"
            template.parent.mkdir(parents=True, exist_ok=True)
            template.write_text(json.dumps(self.flux_ui_template()), encoding="utf-8")
            concept_path = pod_concept(config, "original patriotic mountain shirt")
            concept_id = concept_path.name.split(" ", 1)[0]
            request_path = pod_generation_request(config, concept_id, "flux")
            request_id = request_path.name.split(" ", 1)[0]
            submitted: dict = {}

            def fake_urlopen(request, timeout=0):
                url = request.full_url if hasattr(request, "full_url") else str(request)
                if "/object_info/CheckpointLoaderSimple" in url:
                    return FakeResponse({"CheckpointLoaderSimple": {"input": {"required": {"ckpt_name": [["flux1-schnell-fp8.safetensors"]]}}}})
                if url.endswith("/prompt"):
                    submitted.update(json.loads(request.data.decode("utf-8")))
                    return FakeResponse({"prompt_id": "flux-prompt-1"})
                if "/history/flux-prompt-1" in url:
                    return FakeResponse({"flux-prompt-1": {"outputs": {"9": {"images": [{"filename": "flux.png", "subfolder": "", "type": "output"}]}}, "status": {"messages": []}}})
                if "/view?" in url:
                    return FakeResponse(raw=b"\x89PNG\r\n\x1a\nflux-image")
                raise AssertionError(f"Unexpected URL: {url}")

            with patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}), patch(
                "raphael_core.legacy.urllib.request.urlopen", side_effect=fake_urlopen
            ), patch(
                "raphael_core.legacy.pod_ocr_typography_scan",
                return_value={"available": True, "detected": False, "rejected": False, "max_confidence": 0, "tokens": [], "penalty": 0, "status": "No typography detected."},
            ):
                pod_generate(config, request_id)

            self.assertIn("prompt", submitted)
            self.assertNotIn("nodes", submitted["prompt"])
            self.assertNotIn("39", submitted["prompt"])
            self.assertEqual("flux1-schnell-fp8.safetensors", submitted["prompt"]["30"]["inputs"]["ckpt_name"])
            self.assertEqual(1024, submitted["prompt"]["27"]["inputs"]["width"])
            submitted_positive = submitted["prompt"]["6"]["inputs"]["text"]
            self.assertIn("NO TEXT", submitted_positive)
            self.assertIn("NO LOGOS", submitted_positive)
            self.assertTrue((os_fixture.runtime / "PODStudio" / "logs" / f"{request_id}-submitted-payload.json").exists())
            self.assertTrue((os_fixture.runtime / "PODStudio" / "generated" / request_id / "flux.png").exists())
        finally:
            os_fixture.close()

    def test_ocr_detection_applies_review_score_penalty(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            config.pod_review_with_vision_model = False
            image = os_fixture.runtime / "sample.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\nmock-image")
            scan = {
                "available": True,
                "detected": True,
                "rejected": False,
                "max_confidence": 55.0,
                "tokens": [{"text": "7", "confidence": 55.0}],
                "penalty": 40,
                "status": "Typography contamination detected.",
            }
            with patch("raphael_core.legacy.pod_ocr_typography_scan", return_value=scan):
                review = pod_review_design(config, image)
            text = review.read_text(encoding="utf-8")
            self.assertIn("\n10/100\n", text)
            self.assertIn("\n50/100\n", text)
            self.assertIn("\n-40\n", text)
            self.assertIn("Typography contamination detected.", text)
        finally:
            os_fixture.close()

    def test_configured_tesseract_path_is_used_when_not_on_path(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            executable = os_fixture.root / "Tesseract-OCR" / "tesseract.exe"
            executable.parent.mkdir(parents=True)
            executable.write_bytes(b"test executable")
            config.tesseract_path = executable
            image = os_fixture.runtime / "ocr-source.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\nmock-image")
            completed = type("Completed", (), {
                "returncode": 0,
                "stdout": "level\tpage_num\tblock_num\tpar_num\tline_num\tword_num\tleft\ttop\twidth\theight\tconf\ttext\n5\t1\t1\t1\t1\t1\t0\t0\t10\t10\t88.5\tSALE\n",
                "stderr": "",
            })()

            with patch("raphael_core.legacy.shutil.which", return_value=None), patch(
                "raphael_core.legacy.subprocess.run", return_value=completed
            ) as run:
                scan = pod_ocr_typography_scan(config, image)

            self.assertTrue(scan["available"])
            self.assertEqual(str(executable), scan["executable"])
            self.assertEqual("configured path", scan["executable_source"])
            self.assertEqual(str(executable), run.call_args.args[0][0])

            with patch("raphael_core.legacy.shutil.which", return_value=None), patch(
                "raphael_core.legacy.pod_comfyui_status", return_value=(False, "offline", [])
            ), patch(
                "raphael_core.legacy.pod_vision_model", return_value=("vision", False, "offline")
            ):
                status_note = pod_tool_status(config)
            status_text = status_note.read_text(encoding="utf-8")
            self.assertIn(f"Configured Tesseract path: `{executable}`", status_text)
            self.assertIn(f"Actual executable used: `{executable}`", status_text)
            self.assertIn("Resolution source: configured path", status_text)
        finally:
            os_fixture.close()

    def test_sdxl_ui_workflow_conversion_remains_valid(self) -> None:
        data = self.flux_ui_template()
        data["nodes"][0]["widgets_values"] = ["sd_xl_base_1.0.safetensors"]
        data["nodes"][3]["type"] = "EmptyLatentImage"
        payload, detected = legacy.pod_normalize_comfy_payload(data)
        legacy.pod_inject_comfy_request(
            payload,
            request_id="PODGEN-SDXLTEST",
            positive="positive",
            negative="negative",
            width=1024,
            height=1024,
            seed=42,
            variants=2,
        )
        self.assertEqual("ui_workflow_converted", detected)
        self.assertEqual([], legacy.pod_validate_comfy_payload(payload))
        self.assertEqual("sd_xl_base_1.0.safetensors", payload["prompt"]["30"]["inputs"]["ckpt_name"])

    def test_http_400_body_is_saved_and_debuggable(self) -> None:
        os_fixture = TempRaphael()
        try:
            config = load_config(os_fixture.config)
            concept_path = pod_concept(config, "original simple shirt design")
            concept_id = concept_path.name.split(" ", 1)[0]
            request_path = pod_generation_request(config, concept_id, "sdxl")
            request_id = request_path.name.split(" ", 1)[0]
            body = b'{"error":{"type":"prompt_outputs_failed_validation","message":"bad sampler"}}'

            def fake_urlopen(request, timeout=0):
                url = request.full_url if hasattr(request, "full_url") else str(request)
                if "/object_info/CheckpointLoaderSimple" in url:
                    return FakeResponse({"CheckpointLoaderSimple": {"input": {"required": {"ckpt_name": [["sd_xl_base_1.0.safetensors"]]}}}})
                if url.endswith("/prompt"):
                    raise urllib.error.HTTPError(url, 400, "Bad Request", {}, io.BytesIO(body))
                raise AssertionError(f"Unexpected URL: {url}")

            with patch.dict(os.environ, {"RAPHAEL_CONFIRMED": "YES"}), patch(
                "raphael_core.legacy.urllib.request.urlopen", side_effect=fake_urlopen
            ):
                with self.assertRaisesRegex(RuntimeError, "ComfyUI HTTP 400"):
                    pod_generate(config, request_id)
            error_path = os_fixture.runtime / "PODStudio" / "logs" / f"{request_id}-comfyui-error.json"
            payload_path = os_fixture.runtime / "PODStudio" / "logs" / f"{request_id}-submitted-payload.json"
            self.assertTrue(error_path.exists())
            self.assertTrue(payload_path.exists())
            self.assertIn("bad sampler", error_path.read_text(encoding="utf-8"))
            debug = __import__("raphael_core.legacy", fromlist=["pod_generation_debug"]).pod_generation_debug(config, request_id)
            self.assertEqual("400", debug["http_status"])
            self.assertIn("bad sampler", debug["response_body"])
        finally:
            os_fixture.close()
