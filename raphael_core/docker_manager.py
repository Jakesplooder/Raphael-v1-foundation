"""Allowlisted Docker service management for Raphael OS."""

from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import threading
import time
import urllib.request
from pathlib import Path
from typing import Any

from . import legacy


MANAGED_LABEL = "raphael.managed=true"
SERVICE_LABEL_PREFIX = "raphael.service_id="
_REGISTRY_LOCK = threading.Lock()


def docker_root(config: legacy.RaphaelConfig) -> Path:
    return config.os_root / "docker"


def registry_path(config: legacy.RaphaelConfig) -> Path:
    return docker_root(config) / "docker_service_registry.json"


def default_services(config: legacy.RaphaelConfig) -> list[dict[str, Any]]:
    root = docker_root(config)
    return [
        {
            "service_id": "qdrant",
            "display_name": "Qdrant",
            "enabled": True,
            "image": "qdrant/qdrant",
            "container_name": "raphael-qdrant",
            "ports": ["127.0.0.1:6333:6333"],
            "volumes": [f"{root / 'qdrant'}:/qdrant/storage"],
            "health_check": os.environ.get("QDRANT_URL", "http://127.0.0.1:6333"),
            "notes": "Local vector memory service.",
        },
        {
            "service_id": "n8n",
            "display_name": "n8n",
            "enabled": True,
            "image": "n8nio/n8n",
            "container_name": "raphael-n8n",
            "ports": ["127.0.0.1:5678:5678"],
            "volumes": [f"{root / 'n8n'}:/home/node/.n8n"],
            "health_check": "http://127.0.0.1:5678",
            "notes": "Disabled by default. External integrations remain blocked.",
        },
        {
            "service_id": "postgres",
            "display_name": "Postgres",
            "enabled": False,
            "image": "postgres",
            "container_name": "raphael-postgres",
            "ports": ["127.0.0.1:5432:5432"],
            "volumes": [f"{root / 'postgres'}:/var/lib/postgresql/data"],
            "health_check": "127.0.0.1:5432",
            "notes": "Disabled by default; credentials are not stored by Raphael.",
        },
        {
            "service_id": "redis",
            "display_name": "Redis",
            "enabled": False,
            "image": "redis",
            "container_name": "raphael-redis",
            "ports": ["127.0.0.1:6379:6379"],
            "volumes": [f"{root / 'redis'}:/data"],
            "health_check": "127.0.0.1:6379",
            "notes": "Disabled by default.",
        },
        {
            "service_id": "searxng",
            "display_name": "SearXNG",
            "enabled": True,
            "image": "searxng/searxng",
            "container_name": "raphael-searxng",
            "ports": ["127.0.0.1:8080:8080"],
            "volumes": [f"{root / 'searxng'}:/etc/searxng"],
            "health_check": "http://127.0.0.1:8080",
            "notes": "Localhost-only headless public-web search provider.",
        },
    ]


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    temp.replace(path)


def ensure_registry(config: legacy.RaphaelConfig) -> Path:
    path = registry_path(config)
    with _REGISTRY_LOCK:
        if not path.exists():
            _write_json(path, {"version": 1, "services": default_services(config)})
    return path


def load_registry(config: legacy.RaphaelConfig) -> dict[str, Any]:
    path = ensure_registry(config)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("services"), list):
        raise RuntimeError("Docker registry must contain a services array.")
    allowed = set(config.docker_allowed_services)
    seen: set[str] = set()
    for row in data["services"]:
        required = {"service_id", "display_name", "enabled", "image", "container_name", "ports", "volumes", "health_check", "notes"}
        if set(row) != required:
            raise RuntimeError(f"Invalid Docker registry fields for {row.get('service_id', 'unknown')}.")
        sid = str(row["service_id"]).lower()
        if sid not in allowed:
            raise RuntimeError(f"Docker service is not config-allowlisted: {sid}")
        if sid in seen:
            raise RuntimeError(f"Duplicate Docker service_id: {sid}")
        if any(not str(port).startswith("127.0.0.1:") for port in row["ports"]):
            raise RuntimeError(f"Public Docker port binding is blocked for {sid}.")
        if not str(row["container_name"]).startswith("raphael-"):
            raise RuntimeError(f"Container name must use the raphael- prefix: {sid}")
        seen.add(sid)
    return data


def get_service(config: legacy.RaphaelConfig, service_id: str) -> dict[str, Any]:
    sid = service_id.strip().lower()
    for row in load_registry(config)["services"]:
        if row["service_id"] == sid:
            return row
    raise KeyError(f"Unknown or disallowed Docker service_id: {service_id}")


def is_docker_service(config: legacy.RaphaelConfig, service_id: str) -> bool:
    try:
        get_service(config, service_id)
        return True
    except (KeyError, RuntimeError):
        return False


def _run(args: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    if not args or args[0] != "docker":
        raise RuntimeError("Only fixed Docker CLI operations are allowed.")
    forbidden = {"exec", "prune", "rm", "rmi", "volume", "system"}
    if len(args) > 1 and args[1] in forbidden:
        raise RuntimeError(f"Docker operation is blocked: {args[1]}")
    try:
        if os.name != "nt":
            # Force using Host Agent when running inside the Linux container
            windows_args = ["docker.exe"] + args[1:]
            from . import legacy
            return legacy.host_aware_run(windows_args, capture_output=True, text=True, timeout=timeout)
        else:
            return subprocess.run(args, capture_output=True, text=True, timeout=timeout, shell=False)
    except Exception as e:
        return subprocess.CompletedProcess(args, returncode=1, stdout="", stderr=str(e))


def docker_status(config: legacy.RaphaelConfig) -> dict[str, Any]:
    if not config.docker_enabled:
        return {"enabled": False, "available": False, "healthy": False, "error": "Docker integration is disabled in config/settings.json."}
    try:
        result = _run(["docker", "version", "--format", "{{json .Server}}"], timeout=12)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return {
            "enabled": True,
            "available": False,
            "healthy": False,
            "error": f"Docker Desktop is unavailable: {exc}. Start Docker Desktop and wait for the engine to become ready.",
        }
    if result.returncode != 0:
        return {
            "enabled": True,
            "available": False,
            "healthy": False,
            "error": f"Docker Desktop is not ready: {(result.stderr or result.stdout).strip()}. Start Docker Desktop and retry.",
        }
    try:
        server = json.loads(result.stdout)
    except json.JSONDecodeError:
        server = {"Version": result.stdout.strip()}
    return {
        "enabled": True,
        "available": True,
        "healthy": True,
        "version": server.get("Version", ""),
        "platform": (server.get("Platform") or {}).get("Name", ""),
        "context": "desktop-linux",
        "error": "",
    }


def _inspect_container(name: str) -> dict[str, Any] | None:
    result = _run(["docker", "container", "inspect", name], timeout=15)
    if result.returncode != 0:
        return None
    try:
        values = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError):
        return None
    return values[0] if values else None


def _is_owned(info: dict[str, Any] | None, service_id: str) -> bool:
    labels = ((info or {}).get("Config") or {}).get("Labels") or {}
    return labels.get("raphael.managed") == "true" and labels.get("raphael.service_id") == service_id


def _container_row(config: legacy.RaphaelConfig, service: dict[str, Any]) -> dict[str, Any]:
    info = _inspect_container(service["container_name"])
    exists = info is not None
    owned = _is_owned(info, service["service_id"])
    running = bool(exists and ((info.get("State") or {}).get("Running")))
    image = ((info or {}).get("Config") or {}).get("Image", "")
    conflict = bool(exists and (not owned or image != service["image"]))
    return {
        **service,
        "exists": exists,
        "running": running,
        "managed": owned,
        "conflict": conflict,
        "container_id": str((info or {}).get("Id", ""))[:12],
        "actual_image": image,
        "state": ((info or {}).get("State") or {}).get("Status", "missing"),
    }


def docker_list(config: legacy.RaphaelConfig) -> dict[str, Any]:
    status = docker_status(config)
    rows = []
    if status["available"]:
        rows = [_container_row(config, row) for row in load_registry(config)["services"]]
    return {"docker": status, "registry_path": str(registry_path(config)), "services": rows}


def _url_health(target: str) -> tuple[bool, str]:
    if target.startswith("http://") or target.startswith("https://"):
        try:
            with urllib.request.urlopen(target, timeout=5) as response:
                return 200 <= response.status < 500, f"HTTP {response.status}"
        except Exception as exc:
            return False, str(exc)
    host, _, port = target.rpartition(":")
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        ok = bool(host and port and sock.connect_ex((host, int(port))) == 0)
    return ok, f"{target} {'reachable' if ok else 'closed'}"


def docker_health(config: legacy.RaphaelConfig, service_id: str | None = None) -> dict[str, Any]:
    status = docker_status(config)
    if not status["available"]:
        return {"docker": status, "healthy": False, "services": []}
    selected = [get_service(config, service_id)] if service_id else load_registry(config)["services"]
    rows = []
    for service in selected:
        container = _container_row(config, service)
        healthy, detail = _url_health(service["health_check"]) if container["running"] else (False, "Container is not running.")
        rows.append({**container, "healthy": healthy, "health": "healthy" if healthy else "unhealthy", "detail": detail})
    return {"docker": status, "healthy": all(row["healthy"] for row in rows if row["enabled"]), "services": rows}


def _confirmed(config: legacy.RaphaelConfig, confirmed: bool) -> bool:
    return confirmed or bool(os.environ.get("RAPHAEL_CONFIRMED")) or not config.docker_requires_confirmation


def _log(config: legacy.RaphaelConfig, service_id: str, action: str, result: dict[str, Any]) -> None:
    path = docker_root(config) / "docker_manager.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"timestamp": dt.datetime.now().isoformat(timespec="seconds"), "service_id": service_id, "action": action, "result": result}) + "\n")


def docker_start(config: legacy.RaphaelConfig, service_id: str, *, confirmed: bool = False) -> dict[str, Any]:
    service = get_service(config, service_id)
    if not service["enabled"]:
        return {"service_id": service_id, "result": "disabled", "error": "Docker service is disabled."}
    if not _confirmed(config, confirmed):
        return {"service_id": service_id, "result": "confirmation_required", "confirmation_required": True, "error": "Confirmation required."}
    status = docker_status(config)
    if not status["available"]:
        return {"service_id": service_id, "result": "docker_unavailable", "error": status["error"]}
    current = _container_row(config, service)
    if current["conflict"]:
        return {
            "service_id": service_id,
            "result": "ownership_conflict",
            "error": f"Container {service['container_name']} exists but is not Raphael-managed with the expected image. It was not touched.",
        }
    if current["running"]:
        return {"service_id": service_id, "result": "already_running", "container_id": current["container_id"], "error": ""}
    if current["exists"]:
        result = _run(["docker", "start", service["container_name"]], timeout=45)
        row = {"service_id": service_id, "result": "started" if result.returncode == 0 else "failed", "container_id": current["container_id"], "error": result.stderr.strip()}
    else:
        if service_id == "searxng":
            settings_path = docker_root(config) / "searxng" / "settings.yml"
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            if not settings_path.exists():
                settings_path.write_text(
                    'use_default_settings: true\n'
                    'server:\n'
                    '  bind_address: "0.0.0.0"\n'
                    '  port: 8080\n'
                    '  secret_key: "raphael-localhost-session-only"\n'
                    'search:\n'
                    '  formats:\n'
                    '    - html\n'
                    '    - json\n',
                    encoding="utf-8",
                )
        image_check = _run(["docker", "image", "inspect", service["image"]], timeout=20)
        pulled = False
        if image_check.returncode != 0:
            pull = _run(["docker", "pull", service["image"]], timeout=600)
            if pull.returncode != 0:
                return {"service_id": service_id, "result": "pull_failed", "error": pull.stderr.strip()}
            pulled = True
        for volume in service["volumes"]:
            host = volume.split(":", 1)[0] + (":" + volume.split(":", 2)[1] if len(volume.split(":")) > 2 else "")
            Path(host).mkdir(parents=True, exist_ok=True)
        args = [
            "docker", "create", "--name", service["container_name"],
            "--label", MANAGED_LABEL,
            "--label", f"{SERVICE_LABEL_PREFIX}{service_id}",
        ]
        for port in service["ports"]:
            args.extend(["--publish", port])
        for volume in service["volumes"]:
            args.extend(["--volume", volume])
        args.append(service["image"])
        created = _run(args, timeout=60)
        if created.returncode != 0:
            return {"service_id": service_id, "result": "create_failed", "error": created.stderr.strip()}
        started = _run(["docker", "start", service["container_name"]], timeout=45)
        row = {
            "service_id": service_id,
            "result": "created_and_started" if started.returncode == 0 else "created_start_failed",
            "container_id": created.stdout.strip()[:12],
            "image_pulled": pulled,
            "error": started.stderr.strip(),
        }
    if row["result"] in {"started", "created_and_started"}:
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            health = docker_health(config, service_id)["services"][0]
            if health["healthy"]:
                row["healthy"] = True
                break
            time.sleep(1)
        else:
            row["healthy"] = False
            row["error"] = f"Container started but health check failed: {health['detail']}"
    _log(config, service_id, "start", row)
    return row


def docker_stop(config: legacy.RaphaelConfig, service_id: str, *, confirmed: bool = False) -> dict[str, Any]:
    service = get_service(config, service_id)
    if not _confirmed(config, confirmed):
        return {"service_id": service_id, "result": "confirmation_required", "confirmation_required": True, "error": "Confirmation required."}
    current = _container_row(config, service)
    if not current["exists"]:
        row = {"service_id": service_id, "result": "not_found", "error": "Container does not exist."}
    elif not current["managed"]:
        row = {"service_id": service_id, "result": "not_managed", "error": "Container lacks Raphael ownership labels and was not stopped."}
    elif not current["running"]:
        row = {"service_id": service_id, "result": "already_stopped", "error": ""}
    else:
        result = _run(["docker", "stop", "--time", "15", service["container_name"]], timeout=30)
        row = {"service_id": service_id, "result": "stopped" if result.returncode == 0 else "failed", "error": result.stderr.strip()}
    _log(config, service_id, "stop", row)
    return row


def docker_restart(config: legacy.RaphaelConfig, service_id: str, *, confirmed: bool = False) -> dict[str, Any]:
    service = get_service(config, service_id)
    if not _confirmed(config, confirmed):
        return {"service_id": service_id, "result": "confirmation_required", "confirmation_required": True, "error": "Confirmation required."}
    current = _container_row(config, service)
    if not current["managed"]:
        row = {"service_id": service_id, "result": "not_managed", "error": "Restart blocked because Raphael does not own this container."}
    else:
        result = _run(["docker", "restart", "--time", "15", service["container_name"]], timeout=45)
        row = {"service_id": service_id, "result": "restarted" if result.returncode == 0 else "failed", "error": result.stderr.strip()}
    _log(config, service_id, "restart", row)
    return row


def docker_logs(config: legacy.RaphaelConfig, service_id: str, *, tail: int = 100) -> dict[str, Any]:
    service = get_service(config, service_id)
    current = _container_row(config, service)
    if not current["managed"]:
        return {"service_id": service_id, "logs": "", "error": "Logs are limited to Raphael-managed containers."}
    result = _run(["docker", "logs", "--tail", str(max(1, min(tail, 500))), service["container_name"]], timeout=20)
    return {"service_id": service_id, "logs": (result.stdout + result.stderr).strip(), "error": "" if result.returncode == 0 else result.stderr.strip()}


def docker_compose_plan(config: legacy.RaphaelConfig) -> Path:
    data = load_registry(config)
    lines = ["# Docker Compose Plan", "", f"Generated: {dt.datetime.now().isoformat(timespec='seconds')}", "", "Planning only; no containers were changed.", ""]
    for row in data["services"]:
        lines.extend([
            f"## {row['display_name']} (`{row['service_id']}`)",
            "",
            f"- Enabled: {row['enabled']}",
            f"- Image: `{row['image']}`",
            f"- Container: `{row['container_name']}`",
            f"- Ports: {', '.join(row['ports'])}",
            f"- Volumes: {', '.join(row['volumes'])}",
            "",
        ])
    path = docker_root(config) / "Docker Compose Plan.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def docker_review(config: legacy.RaphaelConfig) -> Path:
    data = docker_health(config)
    lines = [
        "# Docker Service Review",
        "",
        f"Generated: {dt.datetime.now().isoformat(timespec='seconds')}",
        "",
        f"- Docker available: {data['docker']['available']}",
        f"- Docker version: {data['docker'].get('version', '')}",
        "",
        "| Service | Enabled | Container | Managed | Running | Health |",
        "|---|---:|---|---:|---:|---|",
    ]
    for row in data["services"]:
        lines.append(f"| {row['service_id']} | {row['enabled']} | {row['container_name']} | {row['managed']} | {row['running']} | {row['health']} |")
    lines.extend(["", "## Safety", "", "- No arbitrary Docker commands, exec, prune, deletion, or volume removal.", "- Mutations are restricted to registry images and Raphael-labeled containers.", "- Ports are bound to 127.0.0.1 only."])
    path = docker_root(config) / "Docker Service Review.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
