# POD Studio Tool Registry

Generated: 2026-06-24T23:30:00

| Tool | Status | Configured/Detected Path | Notes |
|---|---|---|---|
| ComfyUI | Unavailable | `http://127.0.0.1:8188` | Unavailable: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it> |
| SDXL Base | Missing | `` |  |
| Flux Schnell | Missing | `` |  |
| Local Vision | Available | `qwen2.5vl` | available by base name |
| rembg | Configured | `C:\AI_Tools\venv\Scripts\rembg.exe` | Background removal CLI |
| Upscayl | Detected, not configured | `C:\Program Files\Upscayl\Upscayl.exe` | GUI detected; CLI path remains blank unless explicitly configured |
| Inkscape | Configured | `C:\Program Files\Inkscape\bin\inkscape.exe` | Configured local typography, SVG composition, and print export engine |
| Krita | Missing | `` | Raster editing |
| n8n Workflow Studio | Enabled | `C:\Users\cyber\Downloads\RalphaelOS\Ralphael\00_Raphael\n8n Workflow Studio` | Draft suggestions only; no activation |

## OCR Enforcement

- Configured Tesseract path: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Actual executable used: `C:\Program Files\Tesseract-OCR\tesseract.exe`
- Resolution source: configured path

## Execution Policy

- Detection does not authorize execution.
- ComfyUI, rembg, and upscaling require confirmation where configured.
- Inkscape execution is available only through the configured path and confirmation-gated POD typography/composition commands.
- Krita remains documented for manual editing.
- No external platform or credential access is permitted.
