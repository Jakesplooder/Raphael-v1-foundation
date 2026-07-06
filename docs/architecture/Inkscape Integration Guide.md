# Inkscape Integration Guide

## Status

Raphael uses configured local Inkscape for POD typography composition and
exports. The executable path comes from `pod_inkscape_path`; command
implementations do not hardcode an installation path.

## Configuration

```json
{
  "pod_typography_enabled": true,
  "pod_inkscape_enabled": true,
  "pod_inkscape_path": "C:/Program Files/Inkscape/bin/inkscape.exe",
  "pod_svg_exports_enabled": true,
  "pod_print_ready_exports_enabled": true,
  "pod_composition_requires_confirmation": true
}
```

## Commands

```bash
python raphael.py pod-typography-status
python raphael.py pod-typography-create "LAND OF THE FREE"
python raphael.py pod-compose-design "C:\path\artwork.png" "PODTYPE-ID"
python raphael.py pod-svg-export "PODCOMP-ID"
python raphael.py pod-print-export "PODCOMP-ID"
python raphael.py pod-typography-review
```

Composition, SVG export, and print export require confirmation. Dashboard and
voice requests route through Command Bus.

## Outputs

Runtime assets:

```text
C:/RaphaelOS/PODStudio/working/typography/
├── assets/
├── compositions/
├── svg_exports/
└── print_exports/
```

Vault metadata:

```text
05_Business/Commerce/POD Design Studio/Typography Engine/
├── Typography Engine Overview.md
├── Typography Reviews.md
├── Typography Templates.md
├── Composition Reviews.md
├── Typography Brief.md
├── Assets/
├── Compositions/
├── SVG Exports/
└── Print Exports/
```

Typography SVGs retain editable `<text>` layers. Compositions reference source
artwork without changing it. Print exports are transparent 4500 × 5400 RGBA
PNGs, corresponding to a 15 × 18 inch design at 300 DPI.

## Preferred POD Workflow

```text
Concept → Prompt → Generate Artwork → Review Artwork
→ Remove Background → Create Typography → Compose Design
→ Export SVG → Export Print-Ready PNG → Listing Draft → Export Package
```

## Safety

- No source image overwrite.
- No publishing or upload.
- No Etsy or Printify credentials.
- No spending.
- No arbitrary shell execution.
- Inkscape receives only fixed Raphael-controlled CLI arguments.
