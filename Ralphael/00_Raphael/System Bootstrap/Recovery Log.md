# Bootstrap Recovery Log

## 2026-06-19T03:27:26

- Action: bootstrap-install-startup
- Health: Not checked
- Service: windows_startup
  - Result: Installed via Startup Folder
  - PID: None
  - Error: C:\Users\cyber\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\RaphaelOS Bootstrap.cmd

## 2026-06-19T03:27:32

- Action: bootstrap-remove-startup
- Health: Not checked
- Service: windows_startup
  - Result: Removed
  - PID: None
  - Error: ERROR: The system cannot find the file specified.

## 2026-06-19T03:27:32

- Action: bootstrap-install-startup
- Health: Not checked
- Service: windows_startup
  - Result: Installed via Startup Folder
  - PID: None
  - Error: C:\Users\cyber\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\RaphaelOS Bootstrap.cmd

## 2026-06-19T03:28:19

- Action: bootstrap-stop
- Health: Needs Attention
- Service: comfyui
  - Result: Stopped
  - PID: 72052
  - Error: None

## 2026-06-19T03:28:35

- Action: bootstrap-restart
- Health: Healthy
- Service: comfyui
  - Result: Stopped
  - PID: 72052
  - Error: None
- Service: dashboard
  - Result: Already running (external/unmanaged)
  - PID: None
  - Error: Not adopted; bootstrap will not stop it.
- Service: comfyui
  - Result: Started
  - PID: 70296
  - Error: None
- Service: voice_gateway
  - Result: Disabled by config
  - PID: None
  - Error: None
- Service: morning_brief
  - Result: Generated
  - PID: None
  - Error: C:\Users\cyber\Downloads\RalphaelOS\Ralphael\00_Raphael\Executive Briefs\Morning Brief.md
- Service: browser
  - Result: Dashboard open requested
  - PID: None
  - Error: None

## 2026-06-19T03:33:13

- Action: bootstrap-stop
- Health: Healthy
- Service: comfyui
  - Result: Stopped
  - PID: 30968
  - Error: None

