# Bootstrap Review

Generated: 2026-06-19T03:33:36

## Overall

Healthy

## Configuration

- Open dashboard on start: True
- Generate morning brief: True
- Start dashboard: True
- Start ComfyUI: True
- Start Voice Gateway: False
- Auto-restart failed services: False
- Restart confirmation required: True

## Managed Processes

- comfyui: PID 70296 (alive)

## Recommendations

- Keep Voice Gateway disabled at startup unless always-on microphone behavior is wanted.
- Treat Ollama and Qdrant as checked external local services, not bootstrap-owned processes.
- Use `bootstrap-health` after crashes before restarting anything.

## Boundary

Bootstrap manages only known local support services. It performs no business
execution, publishing, upload, email, spending, or credential access.
