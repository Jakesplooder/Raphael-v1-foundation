# Bootstrap Service Registry

| Service | Startup | Explicit Allowlisted Command | Ownership |
|---|---|---|---|
| Raphael Dashboard | Enabled | `C:\Users\cyber\AppData\Local\Python\pythoncore-3.14-64\python.exe C:\Users\cyber\Downloads\RalphaelOS\raphael.py --config C:\Users\cyber\Downloads\RalphaelOS\config\settings.json dashboard-start` | Managed only if bootstrap starts it |
| ComfyUI | Enabled | `C:\ComfyUI\venv\Scripts\python.exe C:\ComfyUI\main.py --listen 127.0.0.1 --port 8188` | Managed only if bootstrap starts it |
| Voice Gateway | Disabled | `C:\Users\cyber\AppData\Local\Python\pythoncore-3.14-64\python.exe C:\RaphaelOS\voice_gateway.py wake-chat` | Disabled by default |
| Command Bus | Required core | `C:\RaphaelOS\command_bus.py` | Imported and routed; not a separate process |
| Vault path | Required core | `C:\Users\cyber\Downloads\RalphaelOS\Ralphael` | Critical path |
| Runtime path | Required core | `C:\RaphaelOS` | Critical path |
| Config | Required core | `C:\Users\cyber\Downloads\RalphaelOS\config\settings.json` | Validated before service work |
| Ollama | Recommended local AI | `http://127.0.0.1:11434` | Checked only; never force-started or stopped |
| Qdrant | Recommended local AI | `http://localhost:6333` | Checked only; never force-started or stopped |
| rembg | Creative/POD | `C:\AI_Tools\venv\Scripts\rembg.exe` | Local tool path check |
| Upscayl | Creative/POD | `` | Optional warning when missing |
| Inkscape | Creative/POD | `C:\Program Files\Inkscape\bin\inkscape.exe` | Local tool path check |
| Krita | Creative/POD | `` | Optional warning when missing |
| Piper executable | Voice | `C:/Users/cyber/AppData/Local/Python/pythoncore-3.14-64/Scripts/piper.exe` | Local path check |
| Piper voice model | Voice | `C:/RaphaelOS/voice/models/en_GB-semaine-medium.onnx` | Local path check |
| Browser dashboard voice | Voice | `dashboard_voice_input_enabled=True` | Browser-managed microphone; no audio storage |
| n8n local server | Optional | Not configured | Files remain available; no server start command registered |
| Builder workspace | Optional | `C:\RaphaelOS\builder\workspace` | Path check only |

## Checked, Not Force-Started

- Ollama
- Qdrant
- n8n local server

## Safety

Unknown processes are not adopted or killed.
