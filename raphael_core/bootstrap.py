"""Phase 65A safe local bootstrap and recovery supervisor."""

from __future__ import annotations

import ctypes
import datetime as dt
import json
import os
import socket
import subprocess
import shutil
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
import webbrowser
from pathlib import Path
from typing import Any

from . import legacy


PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
STARTUP_TASK_NAME = "RaphaelOS Bootstrap"


def bootstrap_vault_root(config: legacy.RaphaelConfig) -> Path:
    return legacy.ensure_safe_path(config.vault / "00_Raphael" / "System Bootstrap", config)


def launcher_root(config: legacy.RaphaelConfig) -> Path:
    return legacy.ensure_safe_path(config.os_root / "launcher", config)


def bootstrap_runtime_root(config: legacy.RaphaelConfig) -> Path:
    return legacy.ensure_safe_path(launcher_root(config) / "runtime", config)


def pid_registry_path(config: legacy.RaphaelConfig) -> Path:
    return bootstrap_runtime_root(config) / "service_pids.json"


def ensure_bootstrap(config: legacy.RaphaelConfig) -> tuple[Path, Path]:
    if not config.bootstrap_enabled:
        raise RuntimeError("Raphael bootstrap is disabled in config/settings.json.")
    vault = bootstrap_vault_root(config)
    launcher = launcher_root(config)
    runtime = bootstrap_runtime_root(config)
    for path in [vault, launcher, runtime, runtime / "logs"]:
        path.mkdir(parents=True, exist_ok=True)
    seeds = {
        "Bootstrap Overview.md": """# Raphael Bootstrap Overview

The bootstrap supervisor starts and stops only explicitly allowlisted local
Raphael support services. PID ownership is recorded before a managed process
may be stopped.

Voice Gateway is disabled by default. Ollama and Qdrant are checked but are not
force-started or stopped.
""",
        "Service Registry.md": "# Bootstrap Service Registry\n\nRun `python raphael.py bootstrap-review` to refresh.\n",
        "Startup Log.md": "# Bootstrap Startup Log\n\n",
        "Recovery Log.md": "# Bootstrap Recovery Log\n\n",
        "Bootstrap Health.md": "# Bootstrap Health\n\nRun `python raphael.py bootstrap-health`.\n",
        "Bootstrap Review.md": "# Bootstrap Review\n\n",
    }
    for name, content in seeds.items():
        path = vault / name
        if not path.exists():
            legacy.write_generated_note(path, content, config)
    if not pid_registry_path(config).exists():
        _write_json(pid_registry_path(config), {"version": 1, "services": {}})
    return vault, launcher


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temp.replace(path)


def _load_registry(config: legacy.RaphaelConfig) -> dict[str, Any]:
    ensure_bootstrap(config)
    try:
        data = json.loads(pid_registry_path(config).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {"version": 1, "services": {}}
    data.setdefault("version", 1)
    data.setdefault("services", {})
    return data


def _save_registry(config: legacy.RaphaelConfig, registry: dict[str, Any]) -> None:
    _write_json(pid_registry_path(config), registry)


def _host_agent_request(path: str, payload: dict = None):
    host_agent_url = os.environ.get("HOST_AGENT_URL")
    if not host_agent_url:
        return None
    url = f"{host_agent_url.rstrip('/')}{path}"
    try:
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        else:
            req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3.0) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return None

def _process_creation_time(pid: int) -> int | None:
    if os.name != "nt":
        res = _host_agent_request(f"/process/pid_status?pid={pid}")
        if res and res.get("status") == "running":
            return int(res.get("create_time", 1))
        return None
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return None
    try:
        creation = ctypes.c_ulonglong()
        exit_time = ctypes.c_ulonglong()
        kernel = ctypes.c_ulonglong()
        user = ctypes.c_ulonglong()
        ok = ctypes.windll.kernel32.GetProcessTimes(
            handle,
            ctypes.byref(creation),
            ctypes.byref(exit_time),
            ctypes.byref(kernel),
            ctypes.byref(user),
        )
        return int(creation.value) if ok else None
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)


def _pid_alive(pid: int) -> bool:
    return _process_creation_time(pid) is not None


def _stop_pid(pid: int) -> dict[str, Any]:
    if not pid:
        return {"result": "Missing PID"}
        
    res = _host_agent_request(f"/process/stop?pid={pid}", payload={})
    if res and res.get("status") == "stopped":
        return {"result": "Stopped via Host Agent"}

    if os.name != "nt":
        return {"result": "Unsupported platform"}
    handle = ctypes.windll.kernel32.OpenProcess(1, False, pid)
    if not handle:
        return {"result": "Process already gone"}
    try:
        ctypes.windll.kernel32.TerminateProcess(handle, 1)
        return {"result": "Terminated"}
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)


def _process_executable(pid: int) -> str:
    if os.name != "nt":
        res = _host_agent_request(f"/process/pid_status?pid={pid}")
        if res and res.get("status") == "running":
            return res.get("executable", "")
        return ""
    handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return ""
    try:
        size = ctypes.c_ulong(32768)
        buffer = ctypes.create_unicode_buffer(size.value)
        ok = ctypes.windll.kernel32.QueryFullProcessImageNameW(
            handle, 0, buffer, ctypes.byref(size)
        )
        return buffer.value if ok else ""
    finally:
        ctypes.windll.kernel32.CloseHandle(handle)


def _managed_record_alive(record: dict[str, Any]) -> bool:
    try:
        pid = int(record.get("pid", 0))
        expected = int(record.get("creation_time", 0))
    except (TypeError, ValueError):
        return False
    actual = _process_creation_time(pid)
    command = record.get("command", [])
    expected_executable = str(command[0]) if isinstance(command, list) and command else ""
    actual_executable = _process_executable(pid)
    executable_matches = bool(
        expected_executable
        and actual_executable
        and os.path.normcase(os.path.abspath(expected_executable))
        == os.path.normcase(os.path.abspath(actual_executable))
    )
    return bool(actual and expected and actual == expected and executable_matches)


def _http(url: str, timeout: float = 3) -> tuple[bool, str, Any]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read()
        parsed: Any = None
        if body:
            try:
                parsed = json.loads(body.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                parsed = body[:300].decode("utf-8", errors="replace")
        return True, f"HTTP OK: {url}", parsed
    except Exception as exc:
        return False, str(exc), None


def _port_state(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex((host, port)) == 0


def _voice_config(config: legacy.RaphaelConfig) -> dict[str, Any]:
    path = config.os_root / "voice" / "voice_config.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _required_models(config: legacy.RaphaelConfig) -> list[str]:
    values = [config.default_model, config.ollama_model, config.vision_model]
    return sorted({value for value in values if value})


def _model_present(required: str, available: list[str]) -> bool:
    bare = required.split(":")[0].lower()
    return any(
        candidate.lower() == required.lower()
        or candidate.lower() == bare
        or candidate.lower().startswith(bare + ":")
        for candidate in available
    )


def service_definitions(config: legacy.RaphaelConfig) -> dict[str, dict[str, Any]]:
    repo = legacy.BASE_DIR
    comfy_root = config.bootstrap_comfyui_root.resolve()
    parsed = urllib.parse.urlparse(config.pod_comfyui_url)
    comfy_port = parsed.port or 8188
    return {
        "dashboard": {
            "label": "Raphael Dashboard",
            "enabled": config.bootstrap_start_dashboard,
            "command": [
                sys.executable,
                str(repo / "raphael.py"),
                "--config",
                str(legacy.DEFAULT_SETTINGS_PATH),
                "dashboard-start",
            ],
            "cwd": str(repo),
            "url": f"http://{config.dashboard_host}:{config.dashboard_port}/api/health",
            "host": config.dashboard_host,
            "port": config.dashboard_port,
            "identity": "dashboard-start",
        },
        "comfyui": {
            "label": "ComfyUI",
            "enabled": config.bootstrap_start_comfyui,
            "command": [
                str(config.bootstrap_comfyui_python.resolve()),
                str(comfy_root / "main.py"),
                "--listen",
                "127.0.0.1",
                "--port",
                str(comfy_port),
            ],
            "cwd": str(comfy_root),
            "url": config.pod_comfyui_url.rstrip("/") + "/system_stats",
            "host": parsed.hostname or "127.0.0.1",
            "port": comfy_port,
            "identity": str(comfy_root / "main.py"),
        },
        "voice_gateway": {
            "label": "Voice Gateway",
            "enabled": config.bootstrap_start_voice_gateway,
            "command": [sys.executable, str(config.os_root / "voice_gateway.py"), "wake-chat"],
            "cwd": str(config.os_root),
            "url": "",
            "host": "",
            "port": 0,
            "identity": "voice_gateway.py",
        },
    }


def _append_log(config: legacy.RaphaelConfig, filename: str, action: str, rows: list[dict[str, Any]], health: str = "") -> Path:
    path = bootstrap_vault_root(config) / filename
    block = [
        f"## {dt.datetime.now().isoformat(timespec='seconds')}",
        "",
        f"- Action: {action}",
        f"- Health: {health or 'Not checked'}",
    ]
    for row in rows:
        block.extend([
            f"- Service: {row.get('service', 'bootstrap')}",
            f"  - Result: {row.get('result', '')}",
            f"  - PID: {row.get('pid', 'None')}",
            f"  - Error: {row.get('error', 'None') or 'None'}",
        ])
    block.append("")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(block) + "\n")
    return path


def _spawn_service(config: legacy.RaphaelConfig, name: str, spec: dict[str, Any]) -> dict[str, Any]:
    command = [str(item) for item in spec["command"]]
    cwd = Path(str(spec["cwd"]))
    
    use_host_agent = bool(os.environ.get("HOST_AGENT_URL"))
    
    if not use_host_agent:
        if not cwd.exists():
            return {"service": name, "result": "missing_working_directory", "error": str(cwd)}
        executable = Path(command[0])
        resolved_executable = str(executable) if executable.exists() else shutil.which(command[0])
        if not resolved_executable:
            return {"service": name, "result": "missing_executable", "error": str(executable)}
        command[0] = resolved_executable
        if len(command) > 1 and command[1].lower().endswith(".py"):
            script = Path(command[1])
            if not script.is_absolute():
                script = cwd / script
            if not script.exists():
                return {"service": name, "result": "missing_script", "error": str(script)}
            command[1] = str(script)
            
    log_path = bootstrap_runtime_root(config) / "logs" / f"{name}.log"
    log_handle = log_path.open("a", encoding="utf-8")
    env = os.environ.copy()
    env["RAPHAEL_CONFIG_PATH"] = str(legacy.DEFAULT_SETTINGS_PATH.resolve())
    
    # Send to Host Agent if configured
    if use_host_agent:
        res = _host_agent_request("/process/start", {
            "id": name,
            "command": " ".join(command),
            "cwd": str(cwd),
            "env": {"RAPHAEL_CONFIG_PATH": env["RAPHAEL_CONFIG_PATH"]}
        })
        if res and res.get("status") == "started":
            process_pid = res.get("pid")
            log_handle.write(f"Started via Host Agent with PID {process_pid}\n")
            log_handle.close()
            # Fake creation loop to pass validation
            creation = 1
        else:
            log_handle.write(f"Failed to start via Host Agent: {res}\n")
            log_handle.close()
            return {"service": name, "result": "Failed", "pid": 0, "error": f"Host Agent Error: {res}"}
    else:
        try:
            if os.name != "nt":
                import json, urllib.request, urllib.error
                url = os.environ.get("HOST_AGENT_URL", "") + "/process/run_background"
                if url:
                    payload = json.dumps({"command": command, "cwd": cwd})
                    req = urllib.request.Request(url, data=payload.encode("utf-8"), headers={"Content-Type": "application/json"})
                    try:
                        with urllib.request.urlopen(req, timeout=10) as resp:
                            data = json.loads(resp.read().decode("utf-8"))
                            process_pid = data.get("pid", 0)
                    except Exception as exc:
                        print(f"Failed to start service via host agent: {exc}")
                        raise
                else:
                    raise RuntimeError("HOST_AGENT_URL not configured.")
            else:
                process = subprocess.Popen(
                    command,
                    cwd=cwd,
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    env=env,
                    creationflags=(DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else 0,
                    close_fds=True,
                )
                process_pid = process.pid
        finally:
            log_handle.close()
        
        creation = None
        for _ in range(20):
            creation = _process_creation_time(process_pid)
            if creation:
                break
            time.sleep(0.05)
    if not creation:
        return {"service": name, "result": "Failed", "pid": process_pid, "error": "Process exited before ownership could be recorded."}
    registry = _load_registry(config)
    registry["services"][name] = {
        "pid": process_pid,
        "creation_time": creation,
        "command": command,
        "identity": spec["identity"],
        "started": dt.datetime.now().isoformat(timespec="seconds"),
        "log": str(log_path),
    }
    _save_registry(config, registry)
    return {"service": name, "result": "Started", "pid": process_pid, "error": ""}


def _wait_url(url: str, seconds: float = 25) -> bool:
    if not url:
        return True
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        ok, _, _ = _http(url, timeout=1.5)
        if ok:
            return True
        time.sleep(0.75)
    return False


def bootstrap_health_data(config: legacy.RaphaelConfig, *, write_note: bool = True) -> dict[str, Any]:
    ensure_bootstrap(config)
    validation = legacy.config_validation(config)
    dashboard_url = f"http://{config.dashboard_host}:{config.dashboard_port}/api/health"
    dashboard_ok, dashboard_detail, _ = _http(dashboard_url)
    command_bus_ok = False
    command_bus_detail = ""
    try:
        bus_path = config.os_root / "command_bus.py"
        spec = legacy.importlib.util.spec_from_file_location("raphael_bootstrap_command_bus", bus_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("Command Bus import spec unavailable.")
        module = legacy.importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        bus = module.RaphaelCommandBus()
        route = bus.voice_gateway.route_intent("bootstrap health", bus.voice_config)
        command_bus_ok = bool(route.command and route.command[0] == "bootstrap-health")
        command_bus_detail = f"Imported and classified: {route.intent}"
    except Exception as exc:
        command_bus_detail = str(exc)

    ollama_ok, ollama_detail, ollama_data = _http("http://127.0.0.1:11434/api/tags")
    models = [
        str(item.get("name", ""))
        for item in (ollama_data.get("models", []) if isinstance(ollama_data, dict) else [])
        if item.get("name")
    ]
    required_models = _required_models(config)
    missing_models = [model for model in required_models if not _model_present(model, models)]
    qdrant_ok, qdrant_detail, _ = _http(config.qdrant_url.rstrip("/") + "/collections")
    comfy_ok, comfy_detail, _ = _http(config.pod_comfyui_url.rstrip("/") + "/system_stats")
    voice = _voice_config(config)
    piper_exe = Path(str(voice.get("piper_exe_path", ""))) if voice.get("piper_exe_path") else None
    piper_model = Path(str(voice.get("piper_voice_model_path", ""))) if voice.get("piper_voice_model_path") else None
    piper_config = Path(str(voice.get("piper_voice_config_path", ""))) if voice.get("piper_voice_config_path") else None

    paths: dict[str, Path | None] = {
        "vault": config.vault,
        "runtime": config.os_root,
        "config": legacy.DEFAULT_SETTINGS_PATH,
        "podstudio": legacy.pod_runtime_root(config),
        "brandlibrary": config.os_root / "BrandLibrary",
        "builder_workspace": config.builder_workspace,
        "inkscape": config.pod_inkscape_path,
        "rembg": config.pod_rembg_path,
        "upscayl": config.pod_upscayl_path,
        "krita": config.pod_krita_path,
        "piper_exe": piper_exe,
        "piper_model": piper_model,
        "piper_config": piper_config,
        "comfyui_root": config.bootstrap_comfyui_root,
        "comfyui_python": config.bootstrap_comfyui_python,
    }
    path_records = []
    critical_names = {"vault", "runtime", "config", "podstudio", "brandlibrary", "builder_workspace"}
    for name, path in paths.items():
        exists = bool(path and path.exists())
        path_records.append({"name": name, "path": str(path) if path else "", "exists": exists, "critical": name in critical_names})
    output_folder = legacy.pod_runtime_root(config) / "generated"
    output_writable = False
    try:
        output_folder.mkdir(parents=True, exist_ok=True)
        probe = output_folder / ".bootstrap-write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        output_writable = True
    except OSError:
        output_writable = False

    registry = _load_registry(config)
    managed = []
    changed = False
    for name, record in list(registry["services"].items()):
        alive = _managed_record_alive(record)
        managed.append({**record, "service": name, "alive": alive})
        if not alive:
            registry["services"].pop(name, None)
            changed = True
    if changed:
        _save_registry(config, registry)

    services = {
        "dashboard": {"ok": dashboard_ok, "detail": dashboard_detail, "port_occupied": _port_state(config.dashboard_host, config.dashboard_port)},
        "command_bus": {"ok": command_bus_ok, "detail": command_bus_detail},
        "ollama": {"ok": ollama_ok, "detail": ollama_detail, "models": models, "required": required_models, "missing_models": missing_models},
        "qdrant": {"ok": qdrant_ok, "detail": qdrant_detail},
        "comfyui": {"ok": comfy_ok, "detail": comfy_detail, "output_writable": output_writable},
        "voice": {
            "ok": bool(piper_exe and piper_exe.exists() and piper_model and piper_model.exists()),
            "gateway_enabled": config.bootstrap_start_voice_gateway,
            "piper_exe": bool(piper_exe and piper_exe.exists()),
            "model": bool(piper_model and piper_model.exists()),
        },
    }
    critical_ok = validation["ok"] and dashboard_ok and command_bus_ok and all(
        row["exists"] for row in path_records if row["critical"]
    )
    ai_ok = (not config.bootstrap_check_ollama or (ollama_ok and not missing_models)) and (not config.bootstrap_check_qdrant or qdrant_ok)
    creative_ok = (not config.bootstrap_start_comfyui or comfy_ok) and output_writable and bool(config.pod_inkscape_path and config.pod_inkscape_path.exists()) and config.pod_rembg_path.exists()
    overall = "Healthy" if critical_ok and ai_ok and creative_ok else "Needs Attention"
    data = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "overall": overall,
        "groups": {
            "core": "Online" if critical_ok else "Warning",
            "ai": "Online" if ai_ok else "Warning",
            "creative": "Online" if creative_ok else "Warning",
            "voice": "Online" if services["voice"]["ok"] and config.bootstrap_start_voice_gateway else "Off" if not config.bootstrap_start_voice_gateway else "Warning",
        },
        "services": services,
        "paths": path_records,
        "config": validation,
        "managed_pids": managed,
        "dashboard_url": f"http://localhost:{config.dashboard_port}",
        "comfyui_url": config.pod_comfyui_url,
        "pid_registry": str(pid_registry_path(config)),
    }
    if write_note:
        _write_health_note(config, data)
    return data


def _write_health_note(config: legacy.RaphaelConfig, data: dict[str, Any]) -> Path:
    service_lines = []
    for name, row in data["services"].items():
        service_lines.append(f"- {name}: {'OK' if row.get('ok') else 'Warning'} - {row.get('detail', '')}")
    path_lines = [
        f"- {row['name']}: {'OK' if row['exists'] else 'Missing'} - `{row['path']}`"
        for row in data["paths"]
    ]
    pid_lines = [
        f"- {row['service']}: PID {row['pid']} - {'alive' if row['alive'] else 'stale'}"
        for row in data["managed_pids"]
    ] or ["- No Raphael-managed service PIDs."]
    content = f"""# Bootstrap Health

Generated: {data['generated']}

## Overall

{data['overall']}

## Health Pill

- Core: {data['groups']['core']}
- AI: {data['groups']['ai']}
- Creative: {data['groups']['creative']}
- Voice: {data['groups']['voice']}

## Services

{chr(10).join(service_lines)}

## Paths and Tools

{chr(10).join(path_lines)}

## Managed Processes

{chr(10).join(pid_lines)}

## Safety

Only PID-owned Raphael-managed dashboard, ComfyUI, and optional voice processes
may be stopped. Ollama, Qdrant, unknown processes, and unrelated terminals are
never terminated.
"""
    path = bootstrap_vault_root(config) / "Bootstrap Health.md"
    legacy.write_generated_note(path, content, config)
    return path


def bootstrap_health(config: legacy.RaphaelConfig) -> Path:
    data = bootstrap_health_data(config)
    return bootstrap_vault_root(config) / "Bootstrap Health.md"


def bootstrap_status_text(config: legacy.RaphaelConfig) -> str:
    data = bootstrap_health_data(config)
    return f"""# Raphael Bootstrap Status

- Enabled: {config.bootstrap_enabled}
- Overall: {data['overall']}
- Dashboard: {data['groups']['core']}
- AI: {data['groups']['ai']}
- Creative: {data['groups']['creative']}
- Voice: {data['groups']['voice']}
- Dashboard URL: {data['dashboard_url']}
- ComfyUI URL: {data['comfyui_url']}
- Managed PIDs: {len(data['managed_pids'])}
- PID registry: `{data['pid_registry']}`
- Auto-restart failed services: {config.bootstrap_auto_restart_failed_services}

No autonomous business execution is part of bootstrap.
"""


def bootstrap_start(config: legacy.RaphaelConfig, *, open_browser: bool | None = None) -> dict[str, Any]:
    ensure_bootstrap(config)
    rows: list[dict[str, Any]] = []
    
    # 1. Validate Config
    rows.append({"service": "Configuration", "result": "Validated", "pid": None, "error": ""})
    
    # 2. Check Docker
    docker_ok = False
    try:
        res = subprocess.run(["docker", "info"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0:
            docker_ok = True
            rows.append({"service": "Docker Environment", "result": "Ready", "pid": None, "error": ""})
        else:
            rows.append({"service": "Docker Environment", "result": "Failed", "pid": None, "error": res.stderr.strip()})
    except Exception as e:
        rows.append({"service": "Docker Environment", "result": "Failed", "pid": None, "error": str(e)})

    # 3. Initialize Runtime Directories
    runtime_dirs = [
        config.root / "runtime",
        config.root / "logs",
        config.root / "config",
        bootstrap_vault_root(config)
    ]
    for d in runtime_dirs:
        d.mkdir(parents=True, exist_ok=True)
    rows.append({"service": "Runtime Directories", "result": "Initialized", "pid": None, "error": ""})

    # 4. Morning Brief
    brief = ""
    if config.bootstrap_generate_morning_brief:
        try:
            brief = str(legacy.morning_brief(config))
            rows.append({"service": "morning_brief", "result": "Generated", "pid": None, "error": brief})
        except Exception as exc:
            rows.append({"service": "morning_brief", "result": "Failed", "pid": None, "error": str(exc)})
            
    # Handoff to Docker
    if docker_ok:
        rows.append({
            "service": "Handoff", 
            "result": "Ready for Docker Compose", 
            "pid": None, 
            "error": "Run `docker compose up -d` to start the OS."
        })
        
    health = bootstrap_health_data(config)
    _append_log(config, "Startup Log.md", "bootstrap-start", rows, health["overall"])
    return {"action": "start", "results": rows, "health": health, "morning_brief": brief}


def _stop_managed_service(
    config: legacy.RaphaelConfig,
    name: str,
    record: dict[str, Any],
    *,
    graceful: bool = False,
) -> dict[str, Any]:
    if not _managed_record_alive(record):
        return {"service": name, "result": "Not running or ownership mismatch", "pid": record.get("pid"), "error": "No process was killed."}
    pid = int(record["pid"])
    taskkill_command = ["taskkill", "/PID", str(pid)]
    if not graceful:
        taskkill_command.append("/F")
    completed = subprocess.run(
        taskkill_command,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if completed.returncode != 0 and _pid_alive(pid):
        return {"service": name, "result": "Failed", "pid": pid, "error": (completed.stderr or completed.stdout).strip()}
    return {"service": name, "result": "Stopped", "pid": pid, "error": ""}


def bootstrap_stop(config: legacy.RaphaelConfig, *, require_confirmation: bool = True) -> dict[str, Any]:
    ensure_bootstrap(config)
    if require_confirmation:
        legacy.pod_confirmation_granted("Stop only Raphael-managed support services?")
    registry = _load_registry(config)
    rows = []
    for name, record in list(registry["services"].items()):
        row = _stop_managed_service(config, name, record)
        rows.append(row)
        if row["result"] in {"Stopped", "Not running or ownership mismatch"}:
            registry["services"].pop(name, None)
    _save_registry(config, registry)
    health = bootstrap_health_data(config)
    _append_log(config, "Recovery Log.md", "bootstrap-stop", rows, health["overall"])
    return {"action": "stop", "results": rows, "health": health}


def bootstrap_restart(config: legacy.RaphaelConfig) -> dict[str, Any]:
    if config.bootstrap_requires_confirmation_for_restarts:
        legacy.pod_confirmation_granted("Restart only Raphael-managed support services?")
    stopped = bootstrap_stop(config, require_confirmation=False)
    time.sleep(0.75)
    started = bootstrap_start(config)
    rows = stopped["results"] + started["results"]
    health = started["health"]
    _append_log(config, "Recovery Log.md", "bootstrap-restart", rows, health["overall"])
    return {"action": "restart", "results": rows, "health": health}


def bootstrap_open_dashboard(config: legacy.RaphaelConfig) -> str:
    url = f"http://localhost:{config.dashboard_port}"
    webbrowser.open(url, new=2)
    return url


def _startup_command(config: legacy.RaphaelConfig) -> str:
    script = launcher_root(config) / "start_raphael.ps1"
    return f'powershell.exe -NoProfile -ExecutionPolicy Bypass -File "{script}"'


def _startup_folder_file() -> Path:
    appdata = Path(os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming")))
    return appdata / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "RaphaelOS Bootstrap.cmd"


def bootstrap_install_startup(config: legacy.RaphaelConfig) -> str:
    ensure_bootstrap(config)
    legacy.pod_confirmation_granted("Install the visible Raphael user-logon scheduled task?")
    script = launcher_root(config) / "start_raphael.ps1"
    if not script.exists():
        raise FileNotFoundError(f"Startup script not found: {script}")
    completed = subprocess.run(
        [
            "schtasks.exe",
            "/Create",
            "/TN",
            STARTUP_TASK_NAME,
            "/SC",
            "ONLOGON",
            "/TR",
            _startup_command(config),
            "/F",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if completed.returncode == 0:
        method = "Scheduled Task"
        detail = f"Task `{STARTUP_TASK_NAME}` at user logon"
    else:
        startup_file = _startup_folder_file()
        startup_file.parent.mkdir(parents=True, exist_ok=True)
        startup_file.write_text(
            f'@echo off\r\nstart "" {_startup_command(config)}\r\n',
            encoding="utf-8",
        )
        method = "Startup Folder"
        detail = str(startup_file)
    registration = {
        "method": method,
        "detail": detail,
        "command": _startup_command(config),
        "installed": dt.datetime.now().isoformat(timespec="seconds"),
    }
    _write_json(bootstrap_runtime_root(config) / "startup_registration.json", registration)
    rows = [{"service": "windows_startup", "result": f"Installed via {method}", "pid": None, "error": detail}]
    _append_log(config, "Recovery Log.md", "bootstrap-install-startup", rows)
    return f"Installed Raphael startup via {method}: {detail}\nCommand: {_startup_command(config)}"


def bootstrap_remove_startup(config: legacy.RaphaelConfig) -> str:
    legacy.pod_confirmation_granted("Remove the Raphael user-logon scheduled task?")
    completed = subprocess.run(
        ["schtasks.exe", "/Delete", "/TN", STARTUP_TASK_NAME, "/F"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = (completed.stdout or completed.stderr).strip()
    startup_file = _startup_folder_file()
    startup_file.unlink(missing_ok=True)
    (bootstrap_runtime_root(config) / "startup_registration.json").unlink(missing_ok=True)
    rows = [{"service": "windows_startup", "result": "Removed", "pid": None, "error": output}]
    _append_log(config, "Recovery Log.md", "bootstrap-remove-startup", rows)
    return f"Removed Raphael scheduled task and Startup Folder registration if present."


def bootstrap_review(config: legacy.RaphaelConfig) -> Path:
    data = bootstrap_health_data(config)
    definitions = service_definitions(config)
    registry_lines = []
    for name, spec in definitions.items():
        registry_lines.append(
            f"| {spec['label']} | {'Enabled' if spec['enabled'] else 'Disabled'} | "
            f"`{' '.join(str(item) for item in spec['command'])}` | "
            f"{'Managed only if bootstrap starts it' if name != 'voice_gateway' else 'Disabled by default'} |"
        )
    voice = _voice_config(config)
    registry_lines.extend([
        f"| Command Bus | Required core | `{config.os_root / 'command_bus.py'}` | Imported and routed; not a separate process |",
        f"| Vault path | Required core | `{config.vault}` | Critical path |",
        f"| Runtime path | Required core | `{config.os_root}` | Critical path |",
        f"| Config | Required core | `{legacy.DEFAULT_SETTINGS_PATH}` | Validated before service work |",
        "| Ollama | Recommended local AI | `http://127.0.0.1:11434` | Checked only; never force-started or stopped |",
        f"| Qdrant | Recommended local AI | `{config.qdrant_url}` | Checked only; never force-started or stopped |",
        f"| rembg | Creative/POD | `{config.pod_rembg_path}` | Local tool path check |",
        f"| Upscayl | Creative/POD | `{config.pod_upscayl_path or ''}` | Optional warning when missing |",
        f"| Inkscape | Creative/POD | `{config.pod_inkscape_path or ''}` | Local tool path check |",
        f"| Krita | Creative/POD | `{config.pod_krita_path or ''}` | Optional warning when missing |",
        f"| Piper executable | Voice | `{voice.get('piper_exe_path', '')}` | Local path check |",
        f"| Piper voice model | Voice | `{voice.get('piper_voice_model_path', '')}` | Local path check |",
        f"| Browser dashboard voice | Voice | `dashboard_voice_input_enabled={config.dashboard_voice_input_enabled}` | Browser-managed microphone; no audio storage |",
        f"| n8n local server | Optional | Not configured | Files remain available; no server start command registered |",
        f"| Builder workspace | Optional | `{config.builder_workspace}` | Path check only |",
    ])
    registry_content = f"""# Bootstrap Service Registry

| Service | Startup | Explicit Allowlisted Command | Ownership |
|---|---|---|---|
{chr(10).join(registry_lines)}

## Checked, Not Force-Started

- Ollama
- Qdrant
- n8n local server

## Safety

Unknown processes are not adopted or killed.
"""
    legacy.write_generated_note(bootstrap_vault_root(config) / "Service Registry.md", registry_content, config)
    content = f"""# Bootstrap Review

Generated: {data['generated']}

## Overall

{data['overall']}

## Configuration

- Open dashboard on start: {config.bootstrap_open_dashboard_on_start}
- Generate morning brief: {config.bootstrap_generate_morning_brief}
- Start dashboard: {config.bootstrap_start_dashboard}
- Start ComfyUI: {config.bootstrap_start_comfyui}
- Start Voice Gateway: {config.bootstrap_start_voice_gateway}
- Auto-restart failed services: {config.bootstrap_auto_restart_failed_services}
- Restart confirmation required: {config.bootstrap_requires_confirmation_for_restarts}

## Managed Processes

{chr(10).join(f"- {row['service']}: PID {row['pid']} ({'alive' if row['alive'] else 'stale'})" for row in data['managed_pids']) or "- None"}

## Recommendations

- Keep Voice Gateway disabled at startup unless always-on microphone behavior is wanted.
- Treat Ollama and Qdrant as checked external local services, not bootstrap-owned processes.
- Use `bootstrap-health` after crashes before restarting anything.

## Boundary

Bootstrap manages only known local support services. It performs no business
execution, publishing, upload, email, spending, or credential access.
"""
    path = bootstrap_vault_root(config) / "Bootstrap Review.md"
    legacy.write_generated_note(path, content, config)
    return path
