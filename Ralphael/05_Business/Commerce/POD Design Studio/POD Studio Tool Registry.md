# POD Studio Tool Registry

Generated: 2026-07-14T05:28:57

| Tool | Status | Configured/Detected Path | Notes |
|---|---|---|---|
| ComfyUI | Reachable | `http://host.docker.internal:8188` | Reachable |
| SDXL Base | Detected | `sd_xl_base_1.0.safetensors` | FLUX1/flux1-schnell.safetensors, flux1-schnell-fp8.safetensors, ltx-2.3-22b-dev-fp8.safetensors, sd_xl_base_1.0.safetensors, sd_xl_base_1.0_0.9vae.safetensors |
| Flux Schnell | Detected | `FLUX1/flux1-schnell.safetensors` | FLUX1/flux1-schnell.safetensors, flux1-schnell-fp8.safetensors, ltx-2.3-22b-dev-fp8.safetensors, sd_xl_base_1.0.safetensors, sd_xl_base_1.0_0.9vae.safetensors |
| Local Vision | Unavailable | `qwen2.5vl` | Ollama unavailable: <urlopen error [Errno 101] Network is unreachable> |
| rembg | Missing | `C:/AI_Tools/venv/Scripts/rembg.exe` | Background removal CLI |
| Upscayl | Missing | `C:/Program Files/Upscayl/resources/bin/upscayl-bin.exe` | GUI detected; CLI path remains blank unless explicitly configured |
| Inkscape | Missing | `C:/Program Files/Inkscape/bin/inkscape.exe` | Configured local typography, SVG composition, and print export engine |
| Krita | Missing | `` | Raster editing |
| n8n Workflow Studio | Enabled | `/app/vault/00_Raphael/n8n Workflow Studio` | Draft suggestions only; no activation |

## OCR Enforcement

- Configured Tesseract path: `C:/Program Files/Tesseract-OCR/tesseract.exe`
- Actual executable used: `/usr/bin/tesseract`
- Resolution source: PATH

## Execution Policy

- Detection does not authorize execution.
- ComfyUI, rembg, and upscaling require confirmation where configured.
- Inkscape execution is available only through the configured path and confirmation-gated POD typography/composition commands.
- Krita remains documented for manual editing.
- No external platform or credential access is permitted.
