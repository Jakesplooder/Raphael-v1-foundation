# Raphael Bootstrap and Recovery

Phase 65A provides a visible, allowlisted supervisor for local Raphael support
services. It does not perform business execution.

## Commands

```bash
python raphael.py bootstrap-status
python raphael.py bootstrap-start
python raphael.py bootstrap-stop
python raphael.py bootstrap-restart
python raphael.py bootstrap-health
python raphael.py bootstrap-review
python raphael.py bootstrap-install-startup
python raphael.py bootstrap-remove-startup
python raphael.py bootstrap-open-dashboard
```

Stop, restart, startup installation, and startup removal require confirmation.

## Process Ownership

Raphael manages the Dashboard, ComfyUI, and optional Voice Gateway only when
bootstrap started them. PID, Windows process creation time, command, and log
path are recorded in:

`C:/RaphaelOS/launcher/runtime/service_pids.json`

Unknown or reused PIDs are refused. Ollama and Qdrant are checked but are not
force-started or stopped.

## Windows Startup

The startup installer creates the visible per-user scheduled task
`RaphaelOS Bootstrap`, running
`C:/RaphaelOS/launcher/start_raphael.ps1`. The remove command deletes it.
If Windows denies Scheduled Task creation without elevation, Raphael visibly
falls back to a `RaphaelOS Bootstrap.cmd` entry in the current user's Startup
folder. Removal clears either registration method.

## Safety

- Fixed service commands only.
- No arbitrary shell input.
- No unrelated process termination.
- No publishing, upload, email, spending, or credential access.
- Voice startup and failed-service auto-restart default to disabled.
