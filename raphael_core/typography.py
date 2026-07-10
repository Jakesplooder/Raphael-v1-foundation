"""POD Typography & Vector Composition Engine."""

from __future__ import annotations

import datetime as dt
import html
import json
import re
import subprocess
from pathlib import Path

from . import legacy


CANVAS_WIDTH = 4500
CANVAS_HEIGHT = 5400
PRINT_DPI = 300


def typography_vault_root(config: legacy.RaphaelConfig) -> Path:
    return legacy.ensure_safe_path(
        legacy.pod_vault_root(config) / "Typography Engine", config
    )


def typography_runtime_root(config: legacy.RaphaelConfig) -> Path:
    return legacy.ensure_safe_path(
        legacy.pod_runtime_root(config) / "working" / "typography", config
    )


def ensure_typography_engine(config: legacy.RaphaelConfig) -> tuple[Path, Path]:
    legacy.ensure_pod_studio(config)
    if not config.pod_typography_enabled:
        raise RuntimeError("POD Typography Engine is disabled.")
    vault = typography_vault_root(config)
    runtime = typography_runtime_root(config)
    for folder in [
        vault,
        vault / "Assets",
        vault / "Compositions",
        vault / "SVG Exports",
        vault / "Print Exports",
        runtime,
        runtime / "assets",
        runtime / "compositions",
        runtime / "svg_exports",
        runtime / "print_exports",
    ]:
        folder.mkdir(parents=True, exist_ok=True)
    seed_files = {
        "Typography Engine Overview.md": """# Typography Engine Overview

Raphael creates editable SVG typography, composes it with local artwork, and
uses configured local Inkscape for transparent SVG/PNG exports.

No publishing, upload, credential use, spending, or source-image modification
is permitted.
""",
        "Typography Reviews.md": "# Typography Reviews\n\n",
        "Typography Templates.md": """# Typography Templates

## Bold Center Stack

- Uppercase display text
- Center alignment
- High contrast
- Two-line wrapping when needed
- Editable SVG text layers
""",
        "Composition Reviews.md": "# Composition Reviews\n\n",
        "Typography Brief.md": "# Typography Brief\n\nRun `python raphael.py pod-typography-review` to refresh.\n",
    }
    for name, content in seed_files.items():
        path = vault / name
        if not path.exists():
            legacy.write_generated_note(path, content, config)
    return vault, runtime


def inkscape_path(config: legacy.RaphaelConfig) -> Path:
    if not config.pod_inkscape_enabled:
        raise RuntimeError("POD Inkscape integration is disabled.")
    if not config.pod_inkscape_path:
        raise RuntimeError("Set pod_inkscape_path in config/settings.json.")
    path = config.pod_inkscape_path.expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Configured Inkscape executable not found: {path}")
    return path


def run_inkscape(config: legacy.RaphaelConfig, args: list[str], timeout: int = 300) -> subprocess.CompletedProcess[str]:
    executable = inkscape_path(config)
    completed = legacy.host_aware_run(
        [str(executable), *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "Unknown Inkscape error").strip()
        raise RuntimeError(f"Inkscape failed: {detail}")
    return completed


def _find_note(root: Path, ref: str, prefix: str) -> Path:
    target = ref.strip().upper()
    files = sorted(root.glob(f"{prefix}*.md"), key=lambda path: path.stat().st_mtime, reverse=True)
    if target in {"", "LATEST"}:
        if not files:
            raise FileNotFoundError(f"No {prefix} records exist.")
        return files[0]
    for path in files:
        if path.name.upper().startswith(target):
            return path
    raise FileNotFoundError(f"Record not found: {ref}")


def _typography_lines(phrase: str) -> list[str]:
    words = phrase.strip().split()
    if len(phrase) <= 18 or len(words) <= 2:
        return [phrase.strip().upper()]
    midpoint = max(1, len(words) // 2)
    return [" ".join(words[:midpoint]).upper(), " ".join(words[midpoint:]).upper()]


def _typography_score(phrase: str) -> int:
    score = 92
    if len(phrase) > 28:
        score -= 12
    if len(phrase) > 42:
        score -= 15
    if len(phrase.split()) > 7:
        score -= 8
    return max(45, score)


def pod_typography_create(config: legacy.RaphaelConfig, phrase: str) -> Path:
    vault, runtime = ensure_typography_engine(config)
    clean = legacy.redact_secrets(phrase.strip())
    if not clean:
        raise ValueError("Typography phrase cannot be empty.")
    typography_id = legacy.pod_make_id("PODTYPE", clean)
    lines = _typography_lines(clean)
    font = "DejaVu Sans"
    fill = "#F7F1DF"
    stroke = "#1A1A1A"
    font_size = 690 if len(lines) == 1 else 570
    start_y = 2500 if len(lines) == 1 else 2200
    line_gap = 720
    text_nodes = []
    for index, line in enumerate(lines):
        y = start_y + index * line_gap
        text_nodes.append(
            f'<text id="text-{index + 1}" x="{CANVAS_WIDTH / 2}" y="{y}" '
            f'text-anchor="middle" font-family="{html.escape(font)}" '
            f'font-size="{font_size}" font-weight="900" letter-spacing="18" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="22" paint-order="stroke fill">'
            f'{html.escape(line)}</text>'
        )
    svg_path = runtime / "assets" / f"{typography_id}.svg"
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}"
     viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}">
  <g id="typography-layer" aria-label="{html.escape(clean)}">
    {chr(10).join(text_nodes)}
  </g>
</svg>
"""
    svg_path.write_text(svg, encoding="utf-8")
    score = _typography_score(clean)
    note = f"""# POD Typography {typography_id}

## Typography ID

{typography_id}

## Phrase

{clean}

## SVG Path

{svg_path}

## Font Recommendation

{font} Bold or another licensed bold condensed display sans.

## Layout Recommendation

Centered {'single-line' if len(lines) == 1 else 'two-line'} stack with generous tracking and high-contrast outline.

## Color Recommendation

- Fill: {fill}
- Outline: {stroke}
- Preserve transparent canvas.

## POD Suitability Score

{score}/100

## Status

Ready for Composition

## Suggested Next Command

`python raphael.py pod-compose-design "IMAGE-PATH" "{typography_id}"`

## Safety

Generated locally. No source artwork was modified and no external action occurred.
"""
    note_path = vault / "Assets" / f"{typography_id} - {legacy.slugify(clean)[:60]}.md"
    legacy.write_generated_note(note_path, note, config)
    return note_path


def pod_compose_design(config: legacy.RaphaelConfig, image_path: Path, typography_ref: str) -> Path:
    vault, runtime = ensure_typography_engine(config)
    if config.pod_composition_requires_confirmation:
        legacy.pod_confirmation_granted("Compose local POD artwork and typography with Inkscape?")
    image = legacy.pod_validate_image(config, image_path)
    typography_note = _find_note(vault / "Assets", typography_ref, "PODTYPE-")
    typography_text = legacy.read_text_if_exists(typography_note, config, 30000)
    typography_id = legacy.section_value(typography_text, "Typography ID")
    typography_svg = Path(legacy.section_value(typography_text, "SVG Path"))
    phrase = legacy.section_value(typography_text, "Phrase")
    if not typography_svg.exists():
        raise FileNotFoundError(f"Typography SVG not found: {typography_svg}")
    type_svg_text = typography_svg.read_text(encoding="utf-8")
    group_match = re.search(r'<g id="typography-layer".*?</g>', type_svg_text, flags=re.S)
    if not group_match:
        raise RuntimeError("Typography SVG does not contain an editable typography layer.")
    composition_id = legacy.pod_make_id("PODCOMP", f"{image}|{typography_id}")
    request_id, concept_id = legacy.pod_image_context(config, image)
    folder = runtime / "compositions" / composition_id
    folder.mkdir(parents=True, exist_ok=True)
    svg_path = folder / f"{composition_id}.svg"
    png_path = folder / f"{composition_id}.png"
    image_uri = image.resolve().as_uri()
    svg = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{CANVAS_WIDTH}" height="{CANVAS_HEIGHT}" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}">
  <g id="artwork-layer">
    <image id="source-artwork" x="450" y="300" width="3600" height="3600"
           preserveAspectRatio="xMidYMid meet" opacity="1"
           href="{html.escape(image_uri)}" xlink:href="{html.escape(image_uri)}"/>
  </g>
  <g id="composition-typography" transform="translate(0,900)">
    {group_match.group(0)}
  </g>
</svg>
"""
    svg_path.write_text(svg, encoding="utf-8")
    run_inkscape(
        config,
        [
            str(svg_path),
            "--export-type=png",
            f"--export-filename={png_path}",
            f"--export-width={CANVAS_WIDTH}",
            f"--export-height={CANVAS_HEIGHT}",
            "--export-background-opacity=0",
        ],
    )
    if not png_path.exists() or png_path.stat().st_size == 0:
        raise RuntimeError("Inkscape did not create the composed PNG.")
    note = f"""# POD Composition {composition_id}

## Composition ID

{composition_id}

## Typography ID

{typography_id}

## Concept ID

{concept_id or "Unlinked"}

## Generation Request ID

{request_id or "Unlinked"}

## Phrase

{phrase}

## Source Image

{image}

## Composed SVG

{svg_path}

## Composed PNG

{png_path}

## Canvas

{CANVAS_WIDTH} x {CANVAS_HEIGHT} transparent

## Status

Composed

## Composition Review

- Artwork is referenced without modifying the source file.
- Artwork is centered and proportionally fitted.
- Typography remains editable in the SVG.
- PNG is rendered with a transparent background.

## Suggested Next Command

`python raphael.py pod-svg-export "{composition_id}"`

## Safety

Local configured Inkscape only. No publishing, upload, credential use, or spending occurred.
"""
    note_path = vault / "Compositions" / f"{composition_id} - {typography_id}.md"
    legacy.write_generated_note(note_path, note, config)
    legacy.append_unique_section(
        vault / "Composition Reviews.md",
        f"## {composition_id}",
        f"- Source: `{image}`\n- SVG: `{svg_path}`\n- PNG: `{png_path}`\n- Status: Composed\n",
        config,
    )
    return note_path


def _composition(config: legacy.RaphaelConfig, ref: str) -> tuple[Path, str]:
    vault, _ = ensure_typography_engine(config)
    note = _find_note(vault / "Compositions", ref, "PODCOMP-")
    return note, legacy.read_text_if_exists(note, config, 50000)


def pod_svg_export(config: legacy.RaphaelConfig, composition_ref: str) -> Path:
    if not config.pod_svg_exports_enabled:
        raise RuntimeError("POD SVG exports are disabled.")
    if config.pod_requires_confirmation_for_tool_execution:
        legacy.pod_confirmation_granted("Export editable POD SVG with configured Inkscape?")
    vault, runtime = ensure_typography_engine(config)
    _, text = _composition(config, composition_ref)
    composition_id = legacy.section_value(text, "Composition ID")
    concept_id = legacy.section_value(text, "Concept ID")
    source = Path(legacy.section_value(text, "Composed SVG"))
    output = runtime / "svg_exports" / f"{composition_id} - editable.svg"
    run_inkscape(
        config,
        [str(source), "--export-plain-svg", f"--export-filename={output}"],
    )
    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("Inkscape did not create the SVG export.")
    note = f"""# POD SVG Export {composition_id}

## Composition ID

{composition_id}

## Concept ID

{concept_id}

## SVG Export

{output}

## Status

Exported

## Suggested Next Command

`python raphael.py pod-print-export "{composition_id}"`
"""
    path = vault / "SVG Exports" / f"{composition_id} - SVG Export.md"
    legacy.write_generated_note(path, note, config)
    return path


def pod_print_export(config: legacy.RaphaelConfig, composition_ref: str) -> Path:
    if not config.pod_print_ready_exports_enabled:
        raise RuntimeError("POD print-ready exports are disabled.")
    if config.pod_requires_confirmation_for_tool_execution:
        legacy.pod_confirmation_granted("Export transparent print-ready POD PNG with configured Inkscape?")
    vault, runtime = ensure_typography_engine(config)
    _, text = _composition(config, composition_ref)
    composition_id = legacy.section_value(text, "Composition ID")
    concept_id = legacy.section_value(text, "Concept ID")
    source = Path(legacy.section_value(text, "Composed SVG"))
    output = runtime / "print_exports" / f"{composition_id} - 300dpi.png"
    run_inkscape(
        config,
        [
            str(source),
            "--export-type=png",
            f"--export-filename={output}",
            f"--export-width={CANVAS_WIDTH}",
            f"--export-height={CANVAS_HEIGHT}",
            f"--export-dpi={PRINT_DPI}",
            "--export-background-opacity=0",
        ],
        timeout=600,
    )
    if not output.exists() or output.stat().st_size == 0:
        raise RuntimeError("Inkscape did not create the print-ready PNG.")
    try:
        from PIL import Image

        with Image.open(output) as rendered:
            rgba = rendered.convert("RGBA")
            rgba.save(output, format="PNG", dpi=(PRINT_DPI, PRINT_DPI))
    except Exception as exc:
        raise RuntimeError(f"Unable to attach 300 DPI metadata to the Inkscape PNG: {exc}") from exc
    metadata = {
        "composition_id": composition_id,
        "path": str(output),
        "width": CANVAS_WIDTH,
        "height": CANVAS_HEIGHT,
        "dpi": PRINT_DPI,
        "background": "transparent",
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
    }
    metadata_path = output.with_suffix(".json")
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    note = f"""# POD Print Export {composition_id}

## Composition ID

{composition_id}

## Concept ID

{concept_id}

## Print PNG

{output}

## Export Metadata

{metadata_path}

## Dimensions

{CANVAS_WIDTH} x {CANVAS_HEIGHT}

## DPI

{PRINT_DPI}

## Background

Transparent

## Status

Print Ready
"""
    path = vault / "Print Exports" / f"{composition_id} - Print Export.md"
    legacy.write_generated_note(path, note, config)
    return path


def pod_typography_review(config: legacy.RaphaelConfig) -> Path:
    vault, _ = ensure_typography_engine(config)
    assets = sorted((vault / "Assets").glob("PODTYPE-*.md"))
    compositions = sorted((vault / "Compositions").glob("PODCOMP-*.md"))
    svg_exports = sorted((vault / "SVG Exports").glob("PODCOMP-*.md"))
    print_exports = sorted((vault / "Print Exports").glob("PODCOMP-*.md"))
    content = f"""# Typography Brief

Generated: {dt.datetime.now().isoformat(timespec="seconds")}

## Status

{'Ready' if config.pod_inkscape_enabled and config.pod_inkscape_path else 'Needs Configuration'}

## Counts

- Typography assets: {len(assets)}
- Compositions: {len(compositions)}
- SVG exports: {len(svg_exports)}
- Print exports: {len(print_exports)}

## Inkscape

- Enabled: {config.pod_inkscape_enabled}
- Configured path: `{config.pod_inkscape_path or ''}`

## Safety

Local composition and export only. Originals remain unchanged. No publishing,
upload, credentials, or spending.
"""
    path = vault / "Typography Brief.md"
    legacy.write_generated_note(path, content, config)
    legacy.write_generated_note(vault / "Typography Reviews.md", content.replace("# Typography Brief", "# Typography Reviews"), config)
    return path


def pod_typography_status_text(config: legacy.RaphaelConfig) -> str:
    vault, runtime = ensure_typography_engine(config)
    configured = bool(config.pod_inkscape_path and config.pod_inkscape_path.exists())
    version = "Unavailable"
    if configured:
        try:
            version = run_inkscape(config, ["--version"], timeout=30).stdout.strip()
        except Exception as exc:
            version = f"Error: {exc}"
    return f"""# POD Typography Engine Status

- Enabled: {config.pod_typography_enabled}
- Inkscape enabled: {config.pod_inkscape_enabled}
- Inkscape configured: {configured}
- Inkscape path: `{config.pod_inkscape_path or ''}`
- Inkscape version: {version}
- SVG exports enabled: {config.pod_svg_exports_enabled}
- Print exports enabled: {config.pod_print_ready_exports_enabled}
- Composition confirmation required: {config.pod_composition_requires_confirmation}
- Vault: `{vault}`
- Runtime: `{runtime}`

## Boundary

Local files only. No original artwork modification, publishing, upload,
credentials, or spending.
"""
