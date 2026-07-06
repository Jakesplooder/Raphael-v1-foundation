# Bootstrap Health

Generated: 2026-07-05T20:18:08

## Overall

Needs Attention

## Health Pill

- Core: Warning
- AI: Warning
- Creative: Online
- Voice: Off

## Services

- dashboard: Warning - timed out
- command_bus: OK - Imported and classified: bootstrap_health
- ollama: OK - HTTP OK: http://127.0.0.1:11434/api/tags
- qdrant: Warning - <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
- comfyui: OK - HTTP OK: http://127.0.0.1:8188/system_stats
- voice: OK - 

## Paths and Tools

- vault: OK - `C:\Users\cyber\Downloads\RalphaelOS\Ralphael`
- runtime: OK - `C:\RaphaelOS`
- config: OK - `C:\Users\cyber\Downloads\RalphaelOS\config\settings.json`
- podstudio: OK - `C:\RaphaelOS\PODStudio`
- brandlibrary: OK - `C:\RaphaelOS\BrandLibrary`
- builder_workspace: OK - `C:\RaphaelOS\builder\workspace`
- inkscape: OK - `C:\Program Files\Inkscape\bin\inkscape.exe`
- rembg: OK - `C:\AI_Tools\venv\Scripts\rembg.exe`
- upscayl: Missing - ``
- krita: Missing - ``
- piper_exe: OK - `C:\Users\cyber\AppData\Local\Python\pythoncore-3.14-64\Scripts\piper.exe`
- piper_model: OK - `C:\RaphaelOS\voice\models\en_GB-semaine-medium.onnx`
- piper_config: OK - `C:\RaphaelOS\voice\models\en_GB-semaine-medium.onnx.json`
- comfyui_root: OK - `C:\ComfyUI`
- comfyui_python: OK - `C:\ComfyUI\venv\Scripts\python.exe`

## Managed Processes

- dashboard: PID 23852 - alive
- comfyui: PID 13504 - alive

## Safety

Only PID-owned Raphael-managed dashboard, ComfyUI, and optional voice processes
may be stopped. Ollama, Qdrant, unknown processes, and unrelated terminals are
never terminated.
