from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from PIL import Image
from raphael_core.config import load_config
from raphael_core.typography import (
    pod_compose_design,
    pod_print_export,
    pod_svg_export,
    pod_typography_create,
    pod_typography_status_text,
)
from tests.support import TempRaphael


class TypographyEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.os = TempRaphael()
        self.config = load_config(self.os.config)
        self.image = self.os.runtime / "PODStudio" / "input" / "source.png"
        self.image.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (8, 8), (255, 0, 0, 128)).save(self.image)

    def tearDown(self) -> None:
        self.os.close()

    def fake_inkscape(self, config, args, timeout=300):
        output_arg = next((arg for arg in args if arg.startswith("--export-filename=")), "")
        if output_arg:
            output = Path(output_arg.split("=", 1)[1])
            output.parent.mkdir(parents=True, exist_ok=True)
            source = Path(args[0])
            if output.suffix.lower() == ".svg":
                output.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            else:
                Image.new("RGBA", (8, 8), (255, 0, 0, 128)).save(output)
        return subprocess.CompletedProcess(args, 0, stdout="Inkscape test", stderr="")

    def test_typography_composition_and_exports_preserve_source(self) -> None:
        original_hash = hashlib.sha256(self.image.read_bytes()).hexdigest()
        typography_note = pod_typography_create(self.config, "LAND OF THE FREE")
        typography_id = typography_note.name.split(" ", 1)[0]

        with patch("raphael_core.typography.run_inkscape", side_effect=self.fake_inkscape), patch.dict(
            "os.environ", {"RAPHAEL_CONFIRMED": "YES"}
        ):
            composition_note = pod_compose_design(self.config, self.image, typography_id)
            composition_id = composition_note.name.split(" ", 1)[0]
            svg_note = pod_svg_export(self.config, composition_id)
            print_note = pod_print_export(self.config, composition_id)

        self.assertEqual(original_hash, hashlib.sha256(self.image.read_bytes()).hexdigest())
        self.assertTrue(typography_note.exists())
        self.assertTrue(composition_note.exists())
        self.assertTrue(svg_note.exists())
        self.assertTrue(print_note.exists())
        typography_svg = next((self.os.runtime / "PODStudio" / "working" / "typography" / "assets").glob("*.svg"))
        self.assertIn("<text", typography_svg.read_text(encoding="utf-8"))
        composition_svg = next((self.os.runtime / "PODStudio" / "working" / "typography" / "compositions").rglob("*.svg"))
        composition_text = composition_svg.read_text(encoding="utf-8")
        self.assertIn("source-artwork", composition_text)
        self.assertIn("typography-layer", composition_text)

    def test_status_reports_configured_engine(self) -> None:
        status = pod_typography_status_text(self.config)
        self.assertIn("POD Typography Engine Status", status)
        self.assertIn("SVG exports enabled: True", status)
