"""Phase 68 self-healing and observability for Raphael OS.

The module observes local health, records issues, prepares repair plans, and
executes only fixed allowlisted repairs after approval. It does not accept or
run arbitrary shell commands.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import socket
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Any

from . import bootstrap, docker_manager, legacy, pod_workflow, service_manager, workflow_runner


NOTE_FILES = {
    "Self Healing Overview.md": """# Self Healing Overview

Raphael observes local operational health, explains detected issues, prepares
safe repair plans, and only runs allowlisted local repairs after approval.

## Safety Boundary

- No repair runs without approval
- No arbitrary shell commands
- No deleting user files
- No publishing, uploading, spending, account access, or credentials
- No killing unmanaged processes
- No Docker prune
- Repairs are restricted to fixed allowlisted actions
""",
    "Health Observations.md": "# Health Observations\n\nNo observations recorded yet.\n",
    "Detected Issues.md": "# Detected Issues\n\nNo issues detected yet.\n",
    "Repair Plans.md": "# Repair Plans\n\nNo repair plans created yet.\n",
    "Repair History.md": "# Repair History\n\nNo repairs run yet.\n",
    "Observability Review.md": "# Observability Review\n\nNo observability review generated yet.\n",
    "System Reliability Brief.md": "# System Reliability Brief\n\nNo reliability brief generated yet.\n",
}

SEVERITY_WEIGHT = {"info": 3, "warning": 10, "critical": 25}
FINAL_WORKFLOW_STATUSES = {"completed", "failed", "cancelled"}
ALLOWLISTED_REPAIR_ACTIONS = {
    "start_service",
    "restart_service",
    "clear_confirmation_token",
    "refresh_pid_registry",
    "run_health_check",
    "repair_generated_notes",
    "run_route_check",
    "run_dashboard_chat_smoke_test",
    "run_system_check",
    "rerun_workflow_stage",
}


def runtime_root(config: legacy.RaphaelConfig) -> Path:
    path = legacy.ensure_safe_path(config.os_root / "self_healing", config)
    for child in ("observations", "issues", "repairs", "history"):
        (path / child).mkdir(parents=True, exist_ok=True)
    return path


def notes_root(config: legacy.RaphaelConfig) -> Path:
    path = legacy.ensure_safe_path(config.vault / "00_Raphael" / "Self Healing", config)
    path.mkdir(parents=True, exist_ok=True)
    for filename, content in NOTE_FILES.items():
        target = path / filename
        if not target.exists():
            legacy.write_file(target, content, config)
    return path


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2, default=str), encoding="utf-8")
    temp.replace(path)


def _read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def _now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _id(prefix: str, seed: str) -> str:
    digest = hashlib.sha1(f"{seed}|{_now()}".encode("utf-8")).hexdigest()[:8].upper()
    return f"{prefix}-{dt.datetime.now():%Y%m%d}-{digest}"


def _latest(path: Path, pattern: str) -> Path | None:
    rows = sorted(path.glob(pattern), key=lambda item: item.stat().st_mtime, reverse=True)
    return rows[0] if rows else None


def _http_ok(url: str, timeout: float = 2.0) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return 200 <= response.status < 500, f"HTTP {response.status}"
    except Exception as exc:
        return False, str(exc)


def _tcp_ok(host: str, port: int, timeout: float = 1.0) -> tuple[bool, str]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        ok = sock.connect_ex((host, port)) == 0
    return ok, f"{host}:{port} {'reachable' if ok else 'closed'}"


def _tool_exists(path: Path | None, fallback: str) -> tuple[bool, str, str]:
    if path and path.exists():
        return True, str(path), "configured"
    found = shutil_which(fallback)
    if found:
        return True, found, "PATH"
    return False, str(path or ""), "missing"


def shutil_which(name: str) -> str | None:
    # Wrapped for straightforward tests.
    import shutil

    return shutil.which(name)


def _safe_recent_log(path: Path) -> dict[str, str]:
    text = legacy.read_text_if_exists(path, None) if hasattr(legacy, "read_text_if_exists") else ""
    lines = text.splitlines()[-25:] if text else []
    return {"path": str(path), "tail": "\n".join(lines)[-4000:]}


def ensure_self_healing(config: legacy.RaphaelConfig) -> None:
    runtime_root(config)
    notes_root(config)


def observe_system(config: legacy.RaphaelConfig, *, write: bool = True) -> dict[str, Any]:
    ensure_self_healing(config)
    service_status = service_manager.service_status(config)
    services_by_id = {row["service_id"]: row for row in service_status.get("services", [])}
    dashboard_url = f"http://127.0.0.1:{config.dashboard_port}/api/health"
    dashboard_ok, dashboard_detail = _http_ok(dashboard_url)
    comfy_ok, comfy_detail = _http_ok(str(config.pod_comfyui_url).rstrip("/") + "/system_stats")
    qdrant_ok, qdrant_detail = _http_ok(str(config.qdrant_url).rstrip("/"))
    ollama_ok, ollama_detail = _http_ok("http://127.0.0.1:11434/api/tags")
    n8n_ok, n8n_detail = _http_ok("http://127.0.0.1:5678/healthz")
    searx_ok, searx_detail = _http_ok(str(config.searxng_url).rstrip("/"))
    internet_ok, internet_detail = _tcp_ok("1.1.1.1", 53)
    tesseract_ok, tesseract_actual, tesseract_source = _tool_exists(config.tesseract_path, "tesseract")
    inkscape_ok, inkscape_actual, inkscape_source = _tool_exists(config.pod_inkscape_path, "inkscape")
    workflows = []
    try:
        for path in sorted(pod_workflow.workflow_root(config).glob("PODFLOW-*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
            workflows.append(_read_json(path, {}))
    except Exception as exc:
        workflows = [{"error": str(exc)}]
    runner = workflow_runner.runner_status(config)
    docker = docker_manager.docker_list(config)
    observation = {
        "observation_id": _id("OBS", "system"),
        "timestamp": _now(),
        "health_checks": {
            "dashboard": {"ok": dashboard_ok, "detail": dashboard_detail, "url": dashboard_url},
            "command_bus": {"ok": (config.os_root / "command_bus.py").exists(), "detail": str(config.os_root / "command_bus.py")},
            "confirmation_system": {"ok": True, "detail": "Command Bus confirmation state is session-scoped; stale workflow confirmations are detected from workflow files."},
            "pod_workflow": {"ok": not any(row.get("status") == "failed" for row in workflows if isinstance(row, dict)), "count": len(workflows)},
            "workflow_runner": {"ok": runner.get("enabled", False), **runner},
            "comfyui": {"ok": comfy_ok, "detail": comfy_detail, "url": config.pod_comfyui_url},
            "qdrant": {"ok": qdrant_ok, "detail": qdrant_detail, "url": config.qdrant_url},
            "ollama": {"ok": ollama_ok, "detail": ollama_detail, "url": "http://127.0.0.1:11434/api/tags"},
            "n8n": {"ok": n8n_ok, "detail": n8n_detail, "url": "http://127.0.0.1:5678/healthz"},
            "searxng": {"ok": searx_ok, "detail": searx_detail, "url": config.searxng_url},
            "service_manager": {"ok": "error" not in service_status, "detail": service_status.get("error", "ok")},
            "docker_manager": docker.get("docker", {}),
            "internet_access": {"ok": internet_ok, "detail": internet_detail},
            "voice": {"ok": bool((config.os_root / "voice_gateway.py").exists()), "detail": str(config.os_root / "voice_gateway.py")},
            "ocr_tesseract": {"ok": tesseract_ok, "configured_path": str(config.tesseract_path or ""), "actual_executable": tesseract_actual, "source": tesseract_source},
            "inkscape": {"ok": inkscape_ok, "configured_path": str(config.pod_inkscape_path or ""), "actual_executable": inkscape_actual, "source": inkscape_source},
            "builder": {"ok": config.builder_workspace.exists() or config.builder_workspace.parent.exists(), "detail": str(config.builder_workspace)},
            "asset_library": {"ok": bool(config.asset_library_enabled), "detail": "enabled" if config.asset_library_enabled else "disabled"},
        },
        "services": service_status.get("services", []),
        "services_by_id": services_by_id,
        "docker": docker,
        "pod_workflows": workflows,
        "workflow_executions": workflow_runner.executions(config),
        "paths": {
            "runtime": str(runtime_root(config)),
            "notes": str(notes_root(config)),
            "service_pid_registry": str(bootstrap.pid_registry_path(config)),
        },
        "safety": {
            "auto_repair": bool(getattr(config, "self_healing_auto_repair", False)),
            "requires_confirmation": bool(getattr(config, "self_healing_requires_confirmation", True)),
            "allowlisted_repairs_only": True,
        },
    }
    if write:
        path = runtime_root(config) / "observations" / f"{observation['observation_id']}.json"
        _write_json(path, observation)
        _write_notes(config, observation=observation)
    return observation


def _issue(
    kind: str,
    severity: str,
    affected: str,
    symptoms: list[str],
    probable_cause: str,
    evidence: list[str],
    recommended_fix: str,
    repairability: str,
    risk: str,
    command: str,
    logs: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "issue_id": _id("ISSUE", f"{kind}|{affected}|{probable_cause}|{json.dumps(symptoms, sort_keys=True)}|{json.dumps(evidence, sort_keys=True)}"),
        "kind": kind,
        "severity": severity,
        "affected_system": affected,
        "symptoms": symptoms,
        "probable_cause": probable_cause,
        "evidence": evidence,
        "recommended_fix": recommended_fix,
        "repairability": repairability,
        "risk_level": risk,
        "related_logs": logs or [],
        "related_command": command,
        "detected_at": _now(),
        "status": "active",
    }


def detect_issues(config: legacy.RaphaelConfig, *, observation: dict[str, Any] | None = None, write: bool = True) -> dict[str, Any]:
    observation = observation or observe_system(config, write=True)
    checks = observation.get("health_checks", {})
    issues: list[dict[str, Any]] = []

    service_commands = {
        "comfyui": ("start ComfyUI through Service Manager", "python raphael.py service-start comfyui"),
        "qdrant": ("start Qdrant through Service Manager", "python raphael.py service-start qdrant"),
        "n8n": ("start n8n through Service Manager", "python raphael.py service-start n8n"),
        "searxng": ("start SearXNG through Service Manager", "python raphael.py service-start searxng"),
        "ollama": ("start Ollama outside Raphael or register a safe service command", "python raphael.py service-status"),
        "dashboard": ("restart Dashboard through Service Manager", "python raphael.py service-restart dashboard"),
    }
    for key in ["comfyui", "qdrant", "n8n", "searxng", "ollama", "dashboard"]:
        row = checks.get(key, {})
        if row and not row.get("ok"):
            fix, command = service_commands[key]
            issues.append(_issue(
                f"{key}_offline",
                "critical" if key in {"dashboard", "qdrant"} else "warning",
                key.upper() if key in {"n8n"} else key.capitalize(),
                [f"{key} health check failed"],
                str(row.get("detail", "Service is unavailable.")),
                [json.dumps(row, default=str)[:1000]],
                fix,
                "approval_required" if key in {"comfyui", "qdrant", "n8n", "searxng", "dashboard"} else "manual",
                "low" if key in {"comfyui", "searxng", "dashboard"} else "medium",
                command,
            ))

    for tool, label in [("ocr_tesseract", "Tesseract"), ("inkscape", "Inkscape")]:
        row = checks.get(tool, {})
        if row and not row.get("ok"):
            issues.append(_issue(
                f"{tool}_missing",
                "warning",
                label,
                [f"{label} executable was not found"],
                "Configured path is missing and executable is not on PATH.",
                [json.dumps(row, default=str)[:1000]],
                f"Install {label} locally or update config/settings.json to the installed executable path.",
                "manual",
                "low",
                "python raphael.py dependency-check",
            ))

    docker_rows = observation.get("docker", {}).get("services", [])
    seen_containers: dict[str, int] = {}
    for row in docker_rows:
        name = str(row.get("container_name", ""))
        if name:
            seen_containers[name] = seen_containers.get(name, 0) + 1
        if row.get("conflict"):
            issues.append(_issue(
                "unmanaged_docker_container",
                "warning",
                "Docker Manager",
                [f"Container {name} exists but is not Raphael-managed"],
                "Container ownership labels or image do not match the Docker registry.",
                [json.dumps(row, default=str)[:1000]],
                "Review the container manually; Raphael will not stop or adopt unmanaged containers.",
                "manual",
                "medium",
                "python raphael.py docker-status",
            ))
    for name, count in seen_containers.items():
        if count > 1:
            issues.append(_issue(
                "duplicate_service_containers",
                "warning",
                "Docker Manager",
                [f"Duplicate container registry entry for {name}"],
                "Docker registry contains duplicate container names.",
                [f"{name}: {count} entries"],
                "Review Docker service registry and keep one allowlisted Raphael-owned container entry.",
                "manual",
                "medium",
                "python raphael.py docker-status",
            ))

    managed = _read_json(bootstrap.pid_registry_path(config), {"services": {}}).get("services", {})
    for sid, record in managed.items():
        if record and not bootstrap._managed_record_alive(record):
            issues.append(_issue(
                "stale_managed_pid",
                "warning",
                "Service Manager",
                [f"Managed PID for {sid} is no longer alive"],
                "The PID registry still contains an exited process.",
                [json.dumps({"service": sid, "pid": record.get("pid"), "started": record.get("started", "")}, default=str)],
                "Refresh the Service Manager PID registry.",
                "automatic",
                "low",
                "python raphael.py service-status --json",
            ))

    now = dt.datetime.now()
    for workflow in observation.get("pod_workflows", []):
        if not isinstance(workflow, dict):
            continue
        wid = str(workflow.get("workflow_id", ""))
        status = str(workflow.get("status", ""))
        last_error = str(workflow.get("last_error", ""))
        updated_text = str(workflow.get("updated", workflow.get("created", "")))
        if status == "failed":
            issues.append(_issue(
                "failed_pod_workflow_stage",
                "warning",
                "POD Workflow",
                [f"POD workflow {wid} failed"],
                last_error or "A workflow stage recorded failure.",
                [json.dumps({"workflow_id": wid, "status": status, "last_error": last_error}, default=str)[:1000]],
                "Diagnose the failed stage, repair dependencies, then rerun the workflow stage after approval.",
                "approval_required",
                "medium",
                f"python raphael.py pod-workflow-show {wid}",
            ))
        if "comfyui" in last_error.lower() and status in {"failed", "awaiting_service"}:
            issues.append(_issue(
                "workflow_stuck_awaiting_service",
                "warning",
                "POD Workflow",
                [f"POD workflow {wid} is blocked by ComfyUI/service readiness"],
                last_error,
                [json.dumps({"workflow_id": wid, "last_error": last_error}, default=str)[:1000]],
                "Start ComfyUI through Service Manager, then rerun the current workflow stage.",
                "approval_required",
                "medium",
                f"python raphael.py pod-workflow-continue {wid}",
            ))
        try:
            updated = dt.datetime.fromisoformat(updated_text)
            if status == "awaiting_confirmation" and (now - updated).total_seconds() > 24 * 3600:
                issues.append(_issue(
                    "stale_confirmation_token",
                    "info",
                    "Confirmation System",
                    [f"POD workflow {wid} has waited for confirmation for more than 24 hours"],
                    "A previous confirmation prompt was not completed or cancelled.",
                    [json.dumps({"workflow_id": wid, "status": status, "updated": updated_text}, default=str)[:1000]],
                    "Clear or replace the stale confirmation by explicitly continuing or cancelling the workflow.",
                    "approval_required",
                    "low",
                    f"python raphael.py pod-workflow-show {wid}",
                ))
        except ValueError:
            pass

    for execution in observation.get("workflow_executions", []):
        status = str(execution.get("status", ""))
        exec_id = str(execution.get("exec_id", ""))
        if status == "failed":
            issues.append(_issue(
                "failed_workflow_execution",
                "warning",
                "Workflow Runner",
                [f"Workflow execution {exec_id} failed"],
                "; ".join(str(item) for item in execution.get("errors", [])[-2:]) or "Unknown workflow runner failure.",
                [json.dumps({"exec_id": exec_id, "workflow_id": execution.get("workflow_id"), "errors": execution.get("errors", [])}, default=str)[:1000]],
                "Review the failure, repair dependencies, then rerun the registered workflow if still needed.",
                "approval_required",
                "medium",
                f"python raphael.py workflow-result {exec_id}",
            ))
        if status in {"queued", "running"}:
            updated = str(execution.get("updated", ""))
            try:
                if (now - dt.datetime.fromisoformat(updated)).total_seconds() > 6 * 3600:
                    issues.append(_issue(
                        "failed_workflow_execution",
                        "warning",
                        "Workflow Runner",
                        [f"Workflow execution {exec_id} appears stuck"],
                        "Execution has not updated for more than 6 hours.",
                        [json.dumps({"exec_id": exec_id, "status": status, "updated": updated}, default=str)],
                        "Run workflow monitor, inspect logs, and rerun the workflow only after approval.",
                        "approval_required",
                        "medium",
                        f"python raphael.py workflow-monitor {exec_id}",
                    ))
            except ValueError:
                pass

    if not checks.get("command_bus", {}).get("ok", True):
        issues.append(_issue(
            "failed_command_bus_route",
            "critical",
            "Command Bus",
            ["Command Bus file is missing"],
            "Runtime command bus path is unavailable.",
            [json.dumps(checks.get("command_bus", {}), default=str)],
            "Run route-check and repair generated runtime notes.",
            "approval_required",
            "medium",
            "python raphael.py route-check",
        ))

    issue_set = {
        "generated": _now(),
        "observation_id": observation.get("observation_id", ""),
        "count": len(issues),
        "issues": issues,
    }
    if write:
        _write_json(runtime_root(config) / "issues" / "active_issues.json", issue_set)
        for issue in issues:
            _write_json(runtime_root(config) / "issues" / f"{issue['issue_id']}.json", issue)
        _write_notes(config, observation=observation, issues=issue_set)
    return issue_set


def _load_issue(config: legacy.RaphaelConfig, issue_id: str) -> dict[str, Any]:
    active = _read_json(runtime_root(config) / "issues" / "active_issues.json", {"issues": []})
    for row in active.get("issues", []):
        if str(row.get("issue_id", "")).upper() == issue_id.upper():
            return row
    path = runtime_root(config) / "issues" / f"{issue_id.upper()}.json"
    if path.exists():
        return _read_json(path, {})
    raise FileNotFoundError(f"Issue not found: {issue_id}")


def diagnose_issue(config: legacy.RaphaelConfig, issue_id: str) -> dict[str, Any]:
    issue = _load_issue(config, issue_id)
    diagnosis = {
        "issue": issue,
        "root_cause": issue.get("probable_cause", ""),
        "confidence": "medium" if issue.get("evidence") else "low",
        "next_step": issue.get("recommended_fix", ""),
        "safety": "Diagnosis is read-only. No repair has been run.",
    }
    _write_notes(config, diagnosis=diagnosis)
    return diagnosis


def _repair_action_for_issue(issue: dict[str, Any]) -> dict[str, Any]:
    kind = str(issue.get("kind", ""))
    affected = str(issue.get("affected_system", "")).lower()
    if kind.endswith("_offline") and affected in {"comfyui", "qdrant", "n8n", "searxng"}:
        return {"action": "start_service", "service_id": affected}
    if kind == "dashboard_offline":
        return {"action": "restart_service", "service_id": "dashboard"}
    if kind == "stale_managed_pid":
        return {"action": "refresh_pid_registry"}
    if kind == "stale_confirmation_token":
        return {"action": "clear_confirmation_token", "workflow_id": _extract_id(issue, "PODFLOW-")}
    if kind == "failed_pod_workflow_stage" or kind == "workflow_stuck_awaiting_service":
        return {"action": "rerun_workflow_stage", "workflow_id": _extract_id(issue, "PODFLOW-")}
    if kind == "failed_command_bus_route" or kind == "broken_dashboard_route":
        return {"action": "run_route_check"}
    if kind == "failed_workflow_execution":
        return {"action": "run_health_check"}
    return {"action": "run_health_check"}


def _extract_id(issue: dict[str, Any], prefix: str) -> str:
    text = json.dumps(issue, default=str)
    import re

    match = re.search(rf"\b({prefix}[A-Za-z0-9-]+)\b", text, flags=re.I)
    return match.group(1).upper() if match else ""


def repair_plan(config: legacy.RaphaelConfig, issue_id: str) -> dict[str, Any]:
    issue = _load_issue(config, issue_id)
    action = _repair_action_for_issue(issue)
    if action["action"] not in ALLOWLISTED_REPAIR_ACTIONS:
        raise RuntimeError(f"Repair action is not allowlisted: {action['action']}")
    plan = {
        "repair_id": _id("REPAIR", issue_id),
        "issue_id": issue["issue_id"],
        "created": _now(),
        "status": "draft",
        "approved": False,
        "action": action,
        "risk_level": issue.get("risk_level", "low"),
        "repairability": issue.get("repairability", "manual"),
        "summary": issue.get("recommended_fix", ""),
        "steps": _steps_for_action(action),
        "safety": {
            "allowlisted_action": True,
            "requires_approval": True,
            "arbitrary_shell": False,
            "deletes_user_files": False,
            "external_actions": False,
            "kills_unmanaged_processes": False,
            "docker_prune": False,
            "credential_access": False,
        },
        "result": None,
    }
    _write_json(runtime_root(config) / "repairs" / f"{plan['repair_id']}.json", plan)
    _write_notes(config, repair_plan=plan)
    return plan


def _steps_for_action(action: dict[str, Any]) -> list[str]:
    name = action["action"]
    if name == "start_service":
        return [f"Start allowlisted service `{action.get('service_id')}` through Service Manager.", "Refresh observations.", "Record repair result."]
    if name == "restart_service":
        return [f"Restart allowlisted Raphael-managed service `{action.get('service_id')}`.", "Verify health endpoint.", "Record repair result."]
    if name == "clear_confirmation_token":
        return ["Mark the stale confirmation as acknowledged in self-healing records only.", "Do not cancel or advance the workflow automatically."]
    if name == "refresh_pid_registry":
        return ["Run Service Manager status refresh.", "Remove stale dead PID records through existing registry refresh logic."]
    if name == "rerun_workflow_stage":
        return [f"Continue workflow `{action.get('workflow_id')}` through the existing confirmed POD workflow runner.", "Record stage result."]
    if name == "run_dashboard_chat_smoke_test":
        return ["Run safe dry-run dashboard-chat smoke test harness.", "Record failures."]
    if name == "run_route_check":
        return ["Run dashboard route-check diagnostic.", "Record route issues."]
    if name == "run_system_check":
        return ["Run system-check diagnostic.", "Record output."]
    return ["Run fixed local health diagnostic.", "Record result."]


def _load_repair(config: legacy.RaphaelConfig, repair_id: str) -> dict[str, Any]:
    path = runtime_root(config) / "repairs" / f"{repair_id.upper()}.json"
    if not path.exists():
        for candidate in (runtime_root(config) / "repairs").glob("REPAIR-*.json"):
            if candidate.stem.upper() == repair_id.upper():
                path = candidate
                break
    if not path.exists():
        raise FileNotFoundError(f"Repair plan not found: {repair_id}")
    return _read_json(path, {})


def repair_approve(config: legacy.RaphaelConfig, repair_id: str) -> dict[str, Any]:
    plan = _load_repair(config, repair_id)
    plan["approved"] = True
    plan["status"] = "approved"
    plan["approved_at"] = _now()
    _write_json(runtime_root(config) / "repairs" / f"{plan['repair_id']}.json", plan)
    _write_notes(config, repair_plan=plan)
    return plan


def repair_run(config: legacy.RaphaelConfig, repair_id: str) -> dict[str, Any]:
    plan = _load_repair(config, repair_id)
    if not plan.get("approved"):
        raise PermissionError("Repair is not approved. Run repair-approve first.")
    action = plan.get("action", {})
    name = action.get("action")
    if name not in ALLOWLISTED_REPAIR_ACTIONS:
        raise RuntimeError(f"Repair action is not allowlisted: {name}")
    result: Any
    if name == "start_service":
        result = service_manager.start_service(config, str(action.get("service_id", "")), confirmed=True)
    elif name == "restart_service":
        result = service_manager.restart_service(config, str(action.get("service_id", "")), confirmed=True)
    elif name == "refresh_pid_registry":
        result = service_manager.service_status(config)
    elif name == "clear_confirmation_token":
        result = {"cleared": False, "message": "Workflow confirmation state is persistent workflow state; no token was deleted automatically.", "workflow_id": action.get("workflow_id", "")}
    elif name == "repair_generated_notes":
        result = legacy.repair_generated_files(config)
    elif name == "rerun_workflow_stage":
        workflow_id = str(action.get("workflow_id", ""))
        if not workflow_id:
            raise RuntimeError("No workflow_id is available for rerun_workflow_stage.")
        old_confirmation = os.environ.get("RAPHAEL_CONFIRMED")
        os.environ["RAPHAEL_CONFIRMED"] = "YES"
        try:
            result = pod_workflow.pod_workflow_continue(config, workflow_id)
        finally:
            if old_confirmation is None:
                os.environ.pop("RAPHAEL_CONFIRMED", None)
            else:
                os.environ["RAPHAEL_CONFIRMED"] = old_confirmation
    elif name == "run_route_check":
        result = legacy.route_check_data(config)
    elif name == "run_dashboard_chat_smoke_test":
        from . import dashboard_chat_tests

        result = dashboard_chat_tests.run_smoke_test(config)
    elif name == "run_system_check":
        result = {"text": legacy.system_check_text(config, legacy.DEFAULT_SETTINGS_PATH)}
    else:
        result = service_manager.service_status(config)
    plan["status"] = "completed"
    plan["ran_at"] = _now()
    plan["result"] = result
    _write_json(runtime_root(config) / "repairs" / f"{plan['repair_id']}.json", plan)
    history_path = runtime_root(config) / "history" / "repair_history.jsonl"
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"timestamp": _now(), "repair_id": plan["repair_id"], "issue_id": plan["issue_id"], "action": action, "result": result}, default=str) + "\n")
    _write_notes(config, repair_plan=plan)
    return plan


def repair_history(config: legacy.RaphaelConfig) -> dict[str, Any]:
    ensure_self_healing(config)
    path = runtime_root(config) / "history" / "repair_history.jsonl"
    rows = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return {"history": rows, "count": len(rows), "path": str(path)}


def health_score(issue_set: dict[str, Any]) -> int:
    penalty = sum(SEVERITY_WEIGHT.get(str(row.get("severity", "info")), 3) for row in issue_set.get("issues", []))
    return max(0, min(100, 100 - penalty))


def self_healing_status(config: legacy.RaphaelConfig) -> dict[str, Any]:
    ensure_self_healing(config)
    active = _read_json(runtime_root(config) / "issues" / "active_issues.json", {"generated": "", "issues": []})
    history = repair_history(config)
    latest_obs = _latest(runtime_root(config) / "observations", "OBS-*.json")
    return {
        "enabled": bool(getattr(config, "self_healing_enabled", True)),
        "auto_observe": bool(getattr(config, "self_healing_auto_observe", True)),
        "auto_repair": bool(getattr(config, "self_healing_auto_repair", False)),
        "requires_confirmation": bool(getattr(config, "self_healing_requires_confirmation", True)),
        "runtime": str(runtime_root(config)),
        "notes": str(notes_root(config)),
        "latest_observation": str(latest_obs or ""),
        "health_score": health_score(active),
        "active_issue_count": len(active.get("issues", [])),
        "active_issues": active.get("issues", []),
        "repair_history_count": history["count"],
    }


def reliability_brief(config: legacy.RaphaelConfig) -> dict[str, Any]:
    observation = observe_system(config, write=True)
    issues = detect_issues(config, observation=observation, write=True)
    score = health_score(issues)
    critical = [row for row in issues["issues"] if row.get("severity") == "critical"]
    warning = [row for row in issues["issues"] if row.get("severity") == "warning"]
    brief = {
        "generated": _now(),
        "health_score": score,
        "active_issues": len(issues["issues"]),
        "critical": len(critical),
        "warning": len(warning),
        "top_recommendations": [row.get("recommended_fix", "") for row in issues["issues"][:5]],
        "safety": "Auto-repair remains disabled unless explicitly configured and repairs still require approval by default.",
    }
    _write_notes(config, observation=observation, issues=issues, reliability=brief)
    return brief


def _write_notes(
    config: legacy.RaphaelConfig,
    *,
    observation: dict[str, Any] | None = None,
    issues: dict[str, Any] | None = None,
    diagnosis: dict[str, Any] | None = None,
    repair_plan: dict[str, Any] | None = None,
    reliability: dict[str, Any] | None = None,
) -> None:
    root = notes_root(config)
    if observation:
        checks = observation.get("health_checks", {})
        rows = ["| System | OK | Detail |", "|---|---:|---|"]
        for key, row in checks.items():
            rows.append(f"| {key} | {bool(row.get('ok'))} | {legacy.redact_secrets(str(row.get('detail', row.get('url', ''))))[:180]} |")
        legacy.write_generated_note(root / "Health Observations.md", f"# Health Observations\n\nGenerated: {observation.get('timestamp')}\n\n" + "\n".join(rows), config)
    if issues:
        blocks = []
        for issue in issues.get("issues", []):
            blocks.append(
                f"## {issue['issue_id']}\n\n"
                f"- Severity: {issue['severity']}\n"
                f"- Affected system: {issue['affected_system']}\n"
                f"- Symptoms: {'; '.join(issue['symptoms'])}\n"
                f"- Probable cause: {issue['probable_cause']}\n"
                f"- Evidence: {'; '.join(issue['evidence'])}\n"
                f"- Recommended fix: {issue['recommended_fix']}\n"
                f"- Repairability: {issue['repairability']}\n"
                f"- Risk level: {issue['risk_level']}\n"
                f"- Related logs: {', '.join(issue['related_logs']) or 'None'}\n"
                f"- Related command: `{issue['related_command']}`\n"
            )
        legacy.write_generated_note(root / "Detected Issues.md", "# Detected Issues\n\n" + ("\n".join(blocks) or "No active issues detected."), config)
        score = health_score(issues)
        legacy.write_generated_note(
            root / "Observability Review.md",
            f"# Observability Review\n\nGenerated: {_now()}\n\n- Health score: {score}\n- Active issues: {len(issues.get('issues', []))}\n- Critical: {sum(1 for row in issues.get('issues', []) if row.get('severity') == 'critical')}\n- Warning: {sum(1 for row in issues.get('issues', []) if row.get('severity') == 'warning')}\n\nRepairs remain approval-gated and allowlisted.\n",
            config,
        )
    if diagnosis:
        issue = diagnosis.get("issue", {})
        legacy.write_generated_note(
            root / "Observability Review.md",
            f"# Observability Review\n\nGenerated: {_now()}\n\n## Diagnosis: {issue.get('issue_id', '')}\n\n- Root cause: {diagnosis.get('root_cause', '')}\n- Confidence: {diagnosis.get('confidence', '')}\n- Next step: {diagnosis.get('next_step', '')}\n- Safety: {diagnosis.get('safety', '')}\n",
            config,
        )
    if repair_plan:
        plans = []
        for path in sorted((runtime_root(config) / "repairs").glob("REPAIR-*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
            plan = _read_json(path, {})
            plans.append(f"## {plan.get('repair_id', path.stem)}\n\n- Issue: {plan.get('issue_id', '')}\n- Status: {plan.get('status', '')}\n- Approved: {plan.get('approved', False)}\n- Action: `{json.dumps(plan.get('action', {}), default=str)}`\n- Summary: {plan.get('summary', '')}\n")
        legacy.write_generated_note(root / "Repair Plans.md", "# Repair Plans\n\n" + ("\n".join(plans) or "No repair plans created yet."), config)
        hist = repair_history(config)
        legacy.write_generated_note(root / "Repair History.md", "# Repair History\n\n" + (json.dumps(hist["history"][-20:], indent=2, default=str) if hist["history"] else "No repairs run yet."), config)
    if reliability:
        legacy.write_generated_note(
            root / "System Reliability Brief.md",
            f"# System Reliability Brief\n\nGenerated: {reliability['generated']}\n\n- Health score: {reliability['health_score']}\n- Active issues: {reliability['active_issues']}\n- Critical: {reliability['critical']}\n- Warning: {reliability['warning']}\n\n## Top Recommendations\n\n" +
            ("\n".join(f"- {item}" for item in reliability["top_recommendations"]) or "- None.") +
            f"\n\n## Safety\n\n{reliability['safety']}\n",
            config,
        )
