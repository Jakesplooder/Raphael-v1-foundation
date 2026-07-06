"""Safe registry-driven local service management for Raphael OS."""

from __future__ import annotations

import datetime as dt
import json
import os
import shlex
import shutil
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import webbrowser
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from . import bootstrap, legacy


VALID_CATEGORIES = {"core", "ai", "creative", "voice", "workflow", "optional"}
VALID_HEALTH_TYPES = {"port", "url", "process", "file", "command"}
VALID_STOP_METHODS = {"pid", "graceful", "none"}
STACK_ALIASES = {"required", "creative", "voice", "research", "enabled", "managed"}


def registry_path(config: legacy.RaphaelConfig) -> Path:
    return bootstrap.launcher_root(config) / "service_registry.json"


def _repo_python_command(command: str) -> str:
    return subprocess.list2cmdline(
        [
            sys.executable,
            str(legacy.BASE_DIR / "raphael.py"),
            "--config",
            str(legacy.DEFAULT_SETTINGS_PATH),
            command,
        ]
    )


def default_services(config: legacy.RaphaelConfig) -> list[dict[str, Any]]:
    comfy_root = config.bootstrap_comfyui_root
    comfy_command = subprocess.list2cmdline(
        [
            str(config.bootstrap_comfyui_python),
            str(comfy_root / "main.py"),
            "--listen",
            "127.0.0.1",
            "--port",
            "8188",
        ]
    )
    return [
        {
            "service_id": "dashboard",
            "display_name": "Raphael Dashboard",
            "enabled": True,
            "required": True,
            "category": "core",
            "start_command": _repo_python_command("dashboard-start"),
            "working_directory": str(legacy.BASE_DIR),
            "health_check_type": "url",
            "health_check_target": f"http://127.0.0.1:{config.dashboard_port}/api/health",
            "stop_method": "pid",
            "auto_start": True,
            "auto_restart": True,
            "requires_confirmation": False,
            "notes": "Localhost-only Raphael dashboard.",
        },
        {
            "service_id": "comfyui",
            "display_name": "ComfyUI",
            "enabled": True,
            "required": False,
            "category": "creative",
            "start_command": comfy_command,
            "working_directory": str(comfy_root),
            "health_check_type": "url",
            "health_check_target": config.pod_comfyui_url,
            "stop_method": "pid",
            "auto_start": bool(config.bootstrap_start_comfyui),
            "auto_restart": True,
            "requires_confirmation": False,
            "notes": "Managed only when Raphael starts it.",
        },
        {
            "service_id": "ollama",
            "display_name": "Ollama",
            "enabled": True,
            "required": False,
            "category": "ai",
            "start_command": "",
            "working_directory": "",
            "health_check_type": "url",
            "health_check_target": "http://127.0.0.1:11434/api/tags",
            "stop_method": "none",
            "auto_start": False,
            "auto_restart": False,
            "requires_confirmation": False,
            "notes": "Observed only until an explicit local start command is registered.",
        },
        {
            "service_id": "qdrant",
            "display_name": "Qdrant",
            "enabled": True,
            "required": True,
            "category": "ai",
            "start_command": "",
            "working_directory": "",
            "health_check_type": "url",
            "health_check_target": "http://127.0.0.1:6333",
            "stop_method": "graceful",
            "auto_start": True,
            "auto_restart": True,
            "requires_confirmation": True,
            "notes": "Docker-backed allowlisted Qdrant service; managed only with Raphael ownership labels.",
        },
        {
            "service_id": "voice_gateway",
            "display_name": "Voice Gateway",
            "enabled": bool(config.bootstrap_start_voice_gateway),
            "required": False,
            "category": "voice",
            "start_command": subprocess.list2cmdline(
                [sys.executable, str(config.os_root / "voice_gateway.py"), "chat"]
            ),
            "working_directory": str(config.os_root),
            "health_check_type": "process",
            "health_check_target": "voice_gateway.py",
            "stop_method": "graceful",
            "auto_start": False,
            "auto_restart": False,
            "requires_confirmation": True,
            "notes": "Voice never auto-starts unless explicitly enabled.",
        },
        {
            "service_id": "piper",
            "display_name": "Piper",
            "enabled": False,
            "required": False,
            "category": "voice",
            "start_command": "",
            "working_directory": str(config.os_root / "voice"),
            "health_check_type": "file",
            "health_check_target": str(config.os_root / "voice" / "models"),
            "stop_method": "none",
            "auto_start": False,
            "auto_restart": False,
            "requires_confirmation": True,
            "notes": "Optional voice tool path check; no daemon command configured.",
        },
        {
            "service_id": "pod_helpers",
            "display_name": "POD Studio Helpers",
            "enabled": True,
            "required": False,
            "category": "creative",
            "start_command": "",
            "working_directory": str(legacy.pod_runtime_root(config)),
            "health_check_type": "file",
            "health_check_target": str(legacy.pod_runtime_root(config)),
            "stop_method": "none",
            "auto_start": False,
            "auto_restart": False,
            "requires_confirmation": False,
            "notes": "File/tool readiness group; not a persistent process.",
        },
        {
            "service_id": "n8n",
            "display_name": "n8n",
            "enabled": False,
            "required": False,
            "category": "workflow",
            "start_command": "",
            "working_directory": "",
            "health_check_type": "url",
            "health_check_target": "http://127.0.0.1:5678/healthz",
            "stop_method": "graceful",
            "auto_start": False,
            "auto_restart": False,
            "requires_confirmation": True,
            "notes": "Docker-backed but disabled by default. External integrations and credentials remain disabled.",
        },
        {
            "service_id": "postgres",
            "display_name": "Postgres",
            "enabled": False,
            "required": False,
            "category": "optional",
            "start_command": "",
            "working_directory": "",
            "health_check_type": "port",
            "health_check_target": "127.0.0.1:5432",
            "stop_method": "graceful",
            "auto_start": False,
            "auto_restart": False,
            "requires_confirmation": True,
            "notes": "Docker-backed and disabled by default. Raphael stores no database credentials.",
        },
        {
            "service_id": "redis",
            "display_name": "Redis",
            "enabled": False,
            "required": False,
            "category": "optional",
            "start_command": "",
            "working_directory": "",
            "health_check_type": "port",
            "health_check_target": "127.0.0.1:6379",
            "stop_method": "graceful",
            "auto_start": False,
            "auto_restart": False,
            "requires_confirmation": True,
            "notes": "Docker-backed and disabled by default.",
        },
        {
            "service_id": "searxng",
            "display_name": "SearXNG",
            "enabled": True,
            "required": False,
            "category": "ai",
            "start_command": "",
            "working_directory": "",
            "health_check_type": "url",
            "health_check_target": "http://127.0.0.1:8080",
            "stop_method": "graceful",
            "auto_start": False,
            "auto_restart": True,
            "requires_confirmation": True,
            "notes": "Docker-backed localhost-only headless research provider.",
        },
    ]


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temp.replace(path)


def ensure_registry(config: legacy.RaphaelConfig) -> Path:
    bootstrap.ensure_bootstrap(config)
    path = registry_path(config)
    if not path.exists():
        _write_json(path, {"version": 1, "services": default_services(config)})
    return path


def load_registry(config: legacy.RaphaelConfig) -> dict[str, Any]:
    path = ensure_registry(config)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Invalid service registry: {path}: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("services"), list):
        raise RuntimeError("Service registry must contain a services array.")
    seen: set[str] = set()
    for service in data["services"]:
        validate_service(service)
        service_id = service["service_id"]
        if service_id in seen:
            raise RuntimeError(f"Duplicate service_id in registry: {service_id}")
        seen.add(service_id)
    return data


def validate_service(service: dict[str, Any]) -> None:
    required_fields = {
        "service_id", "display_name", "enabled", "required", "category",
        "start_command", "working_directory", "health_check_type",
        "health_check_target", "stop_method", "auto_start", "auto_restart",
        "requires_confirmation", "notes",
    }
    missing = sorted(required_fields - set(service))
    if missing:
        raise RuntimeError(f"Service entry is missing fields: {', '.join(missing)}")
    extra = sorted(set(service) - required_fields)
    if extra:
        raise RuntimeError(f"Service entry contains unsupported fields: {', '.join(extra)}")
    service_id = str(service["service_id"])
    if not service_id or not all(ch.isalnum() or ch in "_-" for ch in service_id):
        raise RuntimeError(f"Invalid service_id: {service_id!r}")
    if service["category"] not in VALID_CATEGORIES:
        raise RuntimeError(f"Invalid category for {service_id}: {service['category']}")
    if service["health_check_type"] not in VALID_HEALTH_TYPES:
        raise RuntimeError(f"Invalid health_check_type for {service_id}")
    if service["stop_method"] not in VALID_STOP_METHODS:
        raise RuntimeError(f"Invalid stop_method for {service_id}")


def _service_map(config: legacy.RaphaelConfig) -> dict[str, dict[str, Any]]:
    return {row["service_id"]: row for row in load_registry(config)["services"]}


def get_service(config: legacy.RaphaelConfig, service_id: str) -> dict[str, Any]:
    services = _service_map(config)
    key = service_id.strip().lower()
    if key not in services:
        raise KeyError(f"Unknown service_id: {service_id}")
    return services[key]


def _command_parts(value: Any) -> list[str]:
    if isinstance(value, list):
        parts = [str(item) for item in value]
    else:
        text = str(value or "").strip()
        if not text:
            return []
        parts = [part.strip('"') for part in shlex.split(text, posix=False)]
    if not parts or any(not part for part in parts):
        raise RuntimeError("Invalid empty service command.")
    return parts


def _managed_registry(config: legacy.RaphaelConfig) -> dict[str, Any]:
    return bootstrap._load_registry(config)


def _save_managed_registry(config: legacy.RaphaelConfig, data: dict[str, Any]) -> None:
    bootstrap._save_registry(config, data)


def _health_url(target: str) -> tuple[bool, str]:
    try:
        request = urllib.request.Request(target, headers={"User-Agent": "Raphael-Service-Manager/1"})
        with urllib.request.urlopen(request, timeout=7) as response:
            return 200 <= response.status < 500, f"HTTP {response.status}"
    except Exception as exc:
        parsed = urllib.parse.urlparse(target)
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.75)
            reachable = sock.connect_ex((parsed.hostname or "127.0.0.1", port)) == 0
        if reachable:
            return True, f"TCP reachable; URL check did not complete: {exc}"
        return False, str(exc)


def _health_port(target: str) -> tuple[bool, str]:
    parsed = urllib.parse.urlparse(target if "://" in target else f"tcp://{target}")
    host = parsed.hostname or "127.0.0.1"
    if not parsed.port:
        return False, "Port target must be host:port."
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        ok = sock.connect_ex((host, parsed.port)) == 0
    return ok, f"{host}:{parsed.port} {'reachable' if ok else 'closed'}"


def service_health(config: legacy.RaphaelConfig, service_id: str) -> dict[str, Any]:
    service = get_service(config, service_id)
    from . import docker_manager
    if docker_manager.is_docker_service(config, service_id):
        docker = docker_manager.docker_health(config, service_id)
        if not docker["services"]:
            return {
                "service_id": service_id,
                "display_name": service["display_name"],
                "healthy": False,
                "health": "unhealthy",
                "status": "stopped",
                "detail": docker["docker"].get("error", "Docker unavailable."),
                "managed": False,
                "pid": None,
                "category": service["category"],
                "backend": "docker",
                "container_name": "",
            }
        row = docker["services"][0]
        status = "running" if row["running"] and row["managed"] else "external" if row["running"] else "stopped"
        if row["conflict"]:
            status = "conflict"
        return {
            "service_id": service_id,
            "display_name": service["display_name"],
            "healthy": row["healthy"],
            "health": row["health"],
            "status": status,
            "detail": row["detail"],
            "managed": row["managed"],
            "pid": None,
            "category": service["category"],
            "backend": "docker",
            "container_name": row["container_name"],
            "container_id": row["container_id"],
            "ownership_conflict": row["conflict"],
        }
    managed = _managed_registry(config)["services"].get(service_id)
    managed_alive = bool(managed and bootstrap._managed_record_alive(managed))
    check_type = service["health_check_type"]
    target = str(service["health_check_target"])
    ok = False
    detail = ""
    if check_type == "url":
        ok, detail = _health_url(target)
    elif check_type == "port":
        ok, detail = _health_port(target)
    elif check_type == "file":
        ok = Path(target).exists()
        detail = "Path exists" if ok else "Path missing"
    elif check_type == "process":
        ok = managed_alive
        detail = "Managed process is alive" if ok else "No matching Raphael-managed process"
    elif check_type == "command":
        parts = _command_parts(target)
        completed = subprocess.run(
            parts,
            cwd=service["working_directory"] or None,
            capture_output=True,
            text=True,
            timeout=15,
            shell=False,
        )
        ok = completed.returncode == 0
        detail = (completed.stdout or completed.stderr).strip()[:500] or f"Exit {completed.returncode}"
    status = "running" if ok else "stopped"
    if ok and not managed_alive and check_type in {"url", "port", "process"}:
        status = "external"
    return {
        "service_id": service_id,
        "display_name": service["display_name"],
        "healthy": ok,
        "health": "healthy" if ok else "unhealthy",
        "status": status,
        "detail": detail,
        "managed": managed_alive,
        "pid": managed.get("pid") if managed_alive else None,
        "category": service["category"],
    }


def _selected_services(config: legacy.RaphaelConfig, selector: str) -> list[dict[str, Any]]:
    services = list(_service_map(config).values())
    key = selector.strip().lower()
    if key == "required":
        return [row for row in services if row["required"]]
    if key in {"creative", "voice"}:
        return [row for row in services if row["category"] == key]
    if key == "research":
        wanted = {"searxng", "qdrant", "ollama"}
        return [row for row in services if row["service_id"] in wanted and row["enabled"]]
    if key == "enabled":
        return [row for row in services if row["enabled"]]
    if key == "managed":
        managed_ids = set(_managed_registry(config)["services"])
        return [row for row in services if row["service_id"] in managed_ids]
    return [get_service(config, key)]


def _append_runtime_event(config: legacy.RaphaelConfig, service_id: str, action: str, result: dict[str, Any]) -> None:
    path = bootstrap.bootstrap_runtime_root(config) / "logs" / "service_manager.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
        "service_id": service_id,
        "action": action,
        "result": result,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, default=str) + "\n")


def start_service(config: legacy.RaphaelConfig, service_id: str, *, confirmed: bool = False) -> dict[str, Any]:
    results = []
    for service in _selected_services(config, service_id):
        sid = service["service_id"]
        from . import docker_manager
        if not service["enabled"]:
            row = {"service_id": sid, "result": "disabled", "error": "Service is disabled."}
        elif service["requires_confirmation"] and not confirmed and not os.environ.get("RAPHAEL_CONFIRMED"):
            row = {"service_id": sid, "result": "confirmation_required", "error": "Confirmation required."}
        elif docker_manager.is_docker_service(config, sid):
            row = docker_manager.docker_start(config, sid, confirmed=confirmed)
        else:
            health = service_health(config, sid)
            if health["healthy"]:
                row = {
                    "service_id": sid,
                    "result": "already_running",
                    "managed": health["managed"],
                    "pid": health["pid"],
                    "error": "" if health["managed"] else "Running externally; Raphael will not stop it.",
                }
            else:
                command = _command_parts(service["start_command"])
                if not command:
                    row = {"service_id": sid, "result": "not_configured", "error": "No allowlisted start_command is configured."}
                else:
                    spec = {
                        "command": command,
                        "cwd": service["working_directory"],
                        "identity": command[1] if len(command) > 1 else command[0],
                    }
                    spawned = bootstrap._spawn_service(config, sid, spec)
                    row = {
                        "service_id": sid,
                        "result": spawned["result"].lower().replace(" ", "_"),
                        "pid": spawned.get("pid"),
                        "error": spawned.get("error", ""),
                    }
                    if spawned.get("result") == "Started":
                        deadline = time.monotonic() + 60
                        while time.monotonic() < deadline:
                            if service_health(config, sid)["healthy"]:
                                break
                            time.sleep(0.75)
                        final = service_health(config, sid)
                        row["healthy"] = final["healthy"]
                        if not final["healthy"]:
                            row["error"] = f"Started but health check failed: {final['detail']}"
        _append_runtime_event(config, sid, "start", row)
        results.append(row)
    return {"action": "start", "selector": service_id, "results": results}


def stop_service(config: legacy.RaphaelConfig, service_id: str) -> dict[str, Any]:
    results = []
    registry = _managed_registry(config)
    for service in _selected_services(config, service_id):
        sid = service["service_id"]
        from . import docker_manager
        record = registry["services"].get(sid)
        if docker_manager.is_docker_service(config, sid):
            row = docker_manager.docker_stop(config, sid)
        elif service["stop_method"] == "none":
            row = {"service_id": sid, "result": "not_stoppable", "error": "stop_method is none."}
        elif not record:
            row = {"service_id": sid, "result": "not_managed", "error": "No Raphael-managed PID; no process was stopped."}
        else:
            stopped = bootstrap._stop_managed_service(config, sid, record, graceful=service["stop_method"] == "graceful")
            row = {
                "service_id": sid,
                "result": stopped["result"].lower().replace(" ", "_"),
                "pid": stopped.get("pid"),
                "error": stopped.get("error", ""),
            }
            if stopped["result"] in {"Stopped", "Not running or ownership mismatch"}:
                registry["services"].pop(sid, None)
        _append_runtime_event(config, sid, "stop", row)
        results.append(row)
    _save_managed_registry(config, registry)
    return {"action": "stop", "selector": service_id, "results": results}


def restart_service(config: legacy.RaphaelConfig, service_id: str, *, confirmed: bool = False) -> dict[str, Any]:
    if not confirmed and not os.environ.get("RAPHAEL_CONFIRMED"):
        return {
            "action": "restart",
            "selector": service_id,
            "confirmation_required": True,
            "results": [],
        }
    selected_ids = [row["service_id"] for row in _selected_services(config, service_id)]
    stopped_rows = []
    restartable_ids = []
    for selected_id in selected_ids:
        from . import docker_manager
        if docker_manager.is_docker_service(config, selected_id):
            row = docker_manager.docker_restart(config, selected_id, confirmed=True)
            _append_runtime_event(config, selected_id, "restart", row)
            stopped_rows.append(row)
            continue
        managed = _managed_registry(config)["services"].get(selected_id)
        if not managed or not bootstrap._managed_record_alive(managed):
            row = {
                "service_id": selected_id,
                "result": "not_managed",
                "error": "Restart blocked: Raphael does not own a live PID for this service. Use Start instead.",
            }
            _append_runtime_event(config, selected_id, "restart", row)
            stopped_rows.append(row)
            continue
        restartable_ids.append(selected_id)
        stopped_rows.extend(stop_service(config, selected_id)["results"])
    time.sleep(0.5)
    started_rows = []
    for selected_id in restartable_ids:
        started_rows.extend(start_service(config, selected_id, confirmed=True)["results"])
    return {
        "action": "restart",
        "selector": service_id,
        "confirmation_required": False,
        "results": stopped_rows + started_rows,
    }


def restart_failed(config: legacy.RaphaelConfig, *, confirmed: bool = False) -> dict[str, Any]:
    if not confirmed and not os.environ.get("RAPHAEL_CONFIRMED"):
        return {"action": "restart_failed", "confirmation_required": True, "results": []}
    results = []
    for service in _service_map(config).values():
        if not service["enabled"] or not service["auto_restart"]:
            continue
        health = service_health(config, service["service_id"])
        if not health["healthy"]:
            results.extend(restart_service(config, service["service_id"], confirmed=True)["results"])
    return {"action": "restart_failed", "confirmation_required": False, "results": results}


def service_status(config: legacy.RaphaelConfig) -> dict[str, Any]:
    services = []
    managed = _managed_registry(config)
    changed = False
    definitions = load_registry(config)["services"]
    for service in definitions:
        sid = service["service_id"]
        record = managed["services"].get(sid)
        if record and not bootstrap._managed_record_alive(record):
            managed["services"].pop(sid, None)
            changed = True
    if changed:
        _save_managed_registry(config, managed)
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(definitions)))) as pool:
        health_rows = list(pool.map(lambda row: service_health(config, row["service_id"]), definitions))
    for service, health in zip(definitions, health_rows):
        sid = service["service_id"]
        log_path = bootstrap.bootstrap_runtime_root(config) / "logs" / f"{sid}.log"
        log_tail = ""
        from . import docker_manager
        if docker_manager.is_docker_service(config, sid):
            docker_log = docker_manager.docker_logs(config, sid, tail=100)
            log_tail = docker_log.get("logs", "")
            log_path = docker_manager.docker_root(config) / "docker_manager.log"
        elif log_path.exists():
            try:
                log_tail = "\n".join(log_path.read_text(encoding="utf-8", errors="replace").splitlines()[-25:])
            except OSError:
                pass
        services.append({
            **service,
            **health,
            "log_path": str(log_path),
            "logs": log_tail,
            "last_error": (
                "Docker ownership conflict: the named container is not Raphael-managed and will not be changed."
                if health.get("ownership_conflict")
                else "" if health["healthy"] else health["detail"]
            ),
        })
    from . import docker_manager
    return {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "registry_path": str(registry_path(config)),
        "pid_registry_path": str(bootstrap.pid_registry_path(config)),
        "docker": docker_manager.docker_status(config),
        "docker_registry_path": str(docker_manager.registry_path(config)),
        "services": services,
    }


def service_list(config: legacy.RaphaelConfig) -> list[dict[str, Any]]:
    return load_registry(config)["services"]


def set_enabled(config: legacy.RaphaelConfig, service_id: str, enabled: bool) -> dict[str, Any]:
    legacy.pod_confirmation_granted("Edit this service registry entry?")
    data = load_registry(config)
    for service in data["services"]:
        if service["service_id"] == service_id:
            service["enabled"] = enabled
            if service["category"] == "voice" and not enabled:
                service["auto_start"] = False
            _write_json(registry_path(config), data)
            return service
    raise KeyError(f"Unknown service_id: {service_id}")


def add_service(config: legacy.RaphaelConfig, service: dict[str, Any]) -> dict[str, Any]:
    validate_service(service)
    legacy.pod_confirmation_granted("Add or edit this allowlisted local service?")
    data = load_registry(config)
    existing = next((row for row in data["services"] if row["service_id"] == service["service_id"]), None)
    if existing:
        existing.clear()
        existing.update(service)
    else:
        data["services"].append(service)
    _write_json(registry_path(config), data)
    return service


def interactive_add(config: legacy.RaphaelConfig) -> dict[str, Any]:
    def ask(label: str, default: str = "") -> str:
        suffix = f" [{default}]" if default else ""
        value = input(f"{label}{suffix}: ").strip()
        return value or default

    def yes(label: str, default: bool = False) -> bool:
        return ask(label, "yes" if default else "no").lower() in {"y", "yes", "true", "1"}

    service = {
        "service_id": ask("Service ID").lower(),
        "display_name": ask("Display name"),
        "enabled": yes("Enabled", True),
        "required": yes("Required"),
        "category": ask("Category (core/ai/creative/voice/workflow/optional)", "optional").lower(),
        "start_command": ask("Start command"),
        "working_directory": ask("Working directory"),
        "health_check_type": ask("Health check type (port/url/process/file/command)", "url").lower(),
        "health_check_target": ask("Health check target"),
        "stop_method": ask("Stop method (pid/graceful/none)", "pid").lower(),
        "auto_start": yes("Auto start"),
        "auto_restart": yes("Auto restart"),
        "requires_confirmation": yes("Requires confirmation", True),
        "notes": ask("Notes"),
    }
    return add_service(config, service)


def service_review(config: legacy.RaphaelConfig) -> Path:
    data = service_status(config)
    rows = [
        "| Service | Category | Enabled | Required | Status | Health | Managed PID |",
        "|---|---|---:|---:|---|---|---:|",
    ]
    for service in data["services"]:
        rows.append(
            f"| {service['display_name']} (`{service['service_id']}`) | {service['category']} | "
            f"{service['enabled']} | {service['required']} | {service['status']} | "
            f"{service['health']} | {service['pid'] or ''} |"
        )
    content = f"""# Local Service Manager Review

Generated: {data['generated']}

Registry: `{data['registry_path']}`

{chr(10).join(rows)}

## Safety

- Commands come only from the local service registry and run without a shell.
- Only PID-owned Raphael-managed processes can be stopped.
- Docker operations use a separate allowlist; only `raphael.managed=true` containers can be stopped or restarted.
- Docker ports remain bound to `127.0.0.1`, and volumes are never pruned or deleted automatically.
- Restart and registry edits require confirmation.
- Voice does not auto-start unless enabled.
- No credentials or external platform integrations are stored or started.
"""
    path = bootstrap.bootstrap_vault_root(config) / "Service Manager Review.md"
    legacy.write_generated_note(path, content, config)
    return path


def open_service(config: legacy.RaphaelConfig, service_id: str) -> str:
    service = get_service(config, service_id)
    if service["health_check_type"] != "url":
        raise RuntimeError(f"{service_id} does not have a URL health target.")
    url = str(service["health_check_target"])
    webbrowser.open(url, new=2)
    return url
