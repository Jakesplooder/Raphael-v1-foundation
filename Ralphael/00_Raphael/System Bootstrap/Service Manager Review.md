# Local Service Manager Review

Generated: 2026-06-21T00:03:46

Registry: `C:\RaphaelOS\launcher\service_registry.json`

| Service | Category | Enabled | Required | Status | Health | Managed PID |
|---|---|---:|---:|---|---|---:|
| Raphael Dashboard (`dashboard`) | core | True | True | running | healthy | 27000 |
| ComfyUI (`comfyui`) | creative | True | False | running | healthy | 13728 |
| Ollama (`ollama`) | ai | True | False | external | healthy |  |
| Qdrant (`qdrant`) | ai | True | False | stopped | unhealthy |  |
| Voice Gateway (`voice_gateway`) | voice | False | False | stopped | unhealthy |  |
| Piper (`piper`) | voice | False | False | running | healthy |  |
| POD Studio Helpers (`pod_helpers`) | creative | True | False | running | healthy |  |
| n8n (`n8n`) | workflow | False | False | stopped | unhealthy |  |

## Safety

- Commands come only from the local service registry and run without a shell.
- Only PID-owned Raphael-managed processes can be stopped.
- Restart and registry edits require confirmation.
- Voice does not auto-start unless enabled.
- No credentials or external platform integrations are stored or started.
