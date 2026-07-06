"""Phase 67 local, registered, confirmation-gated workflow execution."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

from . import legacy, pod_workflow


WORKFLOW_NOTES = {
    "Workflow Runner Overview.md": """# Workflow Runner Overview

Raphael executes only enabled workflows from the local workflow registry after
confirmation. Execution is limited to local files, local services, local AI
tools, native Raphael functions, and approved localhost n8n workflows.

## Boundary

- No arbitrary shell commands
- No browser automation
- No publishing, uploads, spending, messaging, account access, or credentials
- No autonomous internet actions
- Cancellation is cooperative and checked between workflow stages
""",
    "Workflow Registry.md": "# Workflow Registry\n\nNo workflows registered yet.\n",
    "Workflow Executions.md": "# Workflow Executions\n\nNo executions recorded yet.\n",
    "Workflow Results.md": "# Workflow Results\n\nNo completed results recorded yet.\n",
    "Workflow Failures.md": "# Workflow Failures\n\nNo failures recorded yet.\n",
    "Workflow Review.md": "# Workflow Review\n\nNo workflow review generated yet.\n",
}

DEFAULT_REGISTRY = [
    {
        "workflow_id": "pod-pipeline",
        "name": "POD Pipeline",
        "category": "creative",
        "description": "Concept, prompt, local generation, review, typography, composition, and local export.",
        "execution_mode": "native",
        "risk_level": "medium",
        "approval_required": True,
        "enabled": True,
        "source": "Perform a local POD Studio workflow using the configured local model. Keep all outputs local.",
    },
    {
        "workflow_id": "knowledge-processing",
        "name": "Knowledge Processing",
        "category": "knowledge",
        "description": "Import registered sources, summarize, classify, relate, and index generated knowledge.",
        "execution_mode": "native",
        "risk_level": "medium",
        "approval_required": True,
        "enabled": True,
        "source": "registered_knowledge_sources",
    },
    {
        "workflow_id": "daily-executive-brief",
        "name": "Daily Executive Brief",
        "category": "core",
        "description": "Review tasks, goals, communications, and knowledge updates, then generate local briefs.",
        "execution_mode": "native",
        "risk_level": "low",
        "approval_required": True,
        "enabled": True,
        "source": "raphael_brief_engine",
    },
]

FINAL_STATUSES = {"completed", "failed", "cancelled"}
SAFE_N8N_TRIGGER_TYPES = {
    "n8n-nodes-base.manualTrigger",
    "n8n-nodes-base.executeWorkflowTrigger",
}
BLOCKED_N8N_TERMS = {
    "httpRequest", "email", "gmail", "slack", "discord", "telegram", "facebook",
    "twitter", "shopify", "woocommerce", "stripe", "paypal", "ftp", "s3",
}


def runner_root(config: legacy.RaphaelConfig) -> Path:
    path = legacy.ensure_safe_path(config.os_root / "workflow_runner", config)
    path.mkdir(parents=True, exist_ok=True)
    for child in ("executions", "logs"):
        (path / child).mkdir(parents=True, exist_ok=True)
    return path


def notes_root(config: legacy.RaphaelConfig) -> Path:
    path = legacy.ensure_safe_path(config.vault / "00_Raphael" / "Workflow Runner", config)
    path.mkdir(parents=True, exist_ok=True)
    for name, content in WORKFLOW_NOTES.items():
        target = path / name
        if not target.exists():
            legacy.write_file(target, content, config)
    return path


def registry_path(config: legacy.RaphaelConfig) -> Path:
    return runner_root(config) / "workflow_registry.json"


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2), encoding="utf-8")
    temporary.replace(path)


def ensure_runner(config: legacy.RaphaelConfig) -> None:
    notes_root(config)
    if not registry_path(config).exists():
        _write_json(registry_path(config), {"version": 1, "workflows": DEFAULT_REGISTRY})


def load_registry(config: legacy.RaphaelConfig) -> list[dict[str, Any]]:
    ensure_runner(config)
    data = json.loads(registry_path(config).read_text(encoding="utf-8"))
    workflows = data.get("workflows", [])
    if not isinstance(workflows, list):
        raise RuntimeError("Workflow registry `workflows` must be a list.")
    seen: set[str] = set()
    for row in workflows:
        required = {
            "workflow_id", "name", "category", "description", "execution_mode",
            "risk_level", "approval_required", "enabled", "source",
        }
        missing = sorted(required - set(row))
        if missing:
            raise RuntimeError(f"Workflow registry entry is missing: {', '.join(missing)}")
        workflow_id = str(row["workflow_id"]).strip().lower()
        if not workflow_id or workflow_id in seen:
            raise RuntimeError(f"Invalid or duplicate workflow_id: {workflow_id}")
        if row["execution_mode"] not in {"native", "n8n"}:
            raise RuntimeError(f"Unsupported execution_mode for {workflow_id}.")
        if row["risk_level"] not in {"low", "medium", "high"}:
            raise RuntimeError(f"Unsupported risk_level for {workflow_id}.")
        seen.add(workflow_id)
    return workflows


def workflow_show(config: legacy.RaphaelConfig, workflow_id: str) -> dict[str, Any]:
    wanted = workflow_id.strip().lower()
    for row in load_registry(config):
        if str(row["workflow_id"]).lower() == wanted:
            return row
    raise FileNotFoundError(f"Registered workflow not found: {workflow_id}")


def _execution_id(workflow_id: str) -> str:
    seed = f"{workflow_id}|{dt.datetime.now().isoformat()}".encode("utf-8")
    return f"WFEXEC-{dt.datetime.now():%Y%m%d}-{hashlib.sha1(seed).hexdigest()[:8].upper()}"


def _execution_path(config: legacy.RaphaelConfig, exec_id: str) -> Path:
    clean = exec_id.strip().upper()
    if not clean.startswith("WFEXEC-") or any(char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" for char in clean):
        raise ValueError(f"Invalid workflow execution ID: {exec_id}")
    return runner_root(config) / "executions" / f"{clean}.json"


def _load_execution(config: legacy.RaphaelConfig, exec_id: str) -> dict[str, Any]:
    path = _execution_path(config, exec_id)
    if not path.exists():
        raise FileNotFoundError(f"Workflow execution not found: {exec_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def _save_execution(config: legacy.RaphaelConfig, state: dict[str, Any]) -> None:
    state["updated"] = dt.datetime.now().isoformat(timespec="seconds")
    _write_json(_execution_path(config, state["exec_id"]), state)
    _write_notes(config)


def _append_log(config: legacy.RaphaelConfig, state: dict[str, Any], message: str) -> None:
    timestamp = dt.datetime.now().isoformat(timespec="seconds")
    clean = legacy.redact_secrets(str(message))
    state.setdefault("logs", []).append({"time": timestamp, "message": clean})
    log_path = runner_root(config) / "logs" / f"{state['exec_id']}.log"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(f"{timestamp} {clean}\n")


def _task_id(path: Path, config: legacy.RaphaelConfig) -> str:
    return legacy.section_value(legacy.read_text_if_exists(path, config), "Task ID")


def _create_task(config: legacy.RaphaelConfig, workflow: dict[str, Any], exec_id: str) -> str:
    if not config.execution_update_tasks:
        return ""
    path = legacy.create_agent_task(
        config,
        "Operations Agent",
        f"Execute registered workflow {workflow['name']} ({workflow['workflow_id']}) as {exec_id}.",
    )
    task_id = _task_id(path, config)
    legacy.update_task_status(config, task_id, "In Progress")
    legacy.append_task_log(config, task_id, f"Workflow execution {exec_id} started.")
    return task_id


def _update_task(config: legacy.RaphaelConfig, state: dict[str, Any], status: str, note: str) -> None:
    task_id = state.get("task_id", "")
    if not task_id:
        return
    legacy.append_task_log(config, task_id, note)
    legacy.update_task_status(config, task_id, status)


def _approval(config: legacy.RaphaelConfig, workflow: dict[str, Any]) -> None:
    if workflow.get("approval_required", True):
        legacy.pod_confirmation_granted(
            f"Execute registered {workflow['risk_level']}-risk workflow {workflow['workflow_id']}?"
        )


def workflow_execute(
    config: legacy.RaphaelConfig,
    workflow_id: str,
    settings_path: Path | None = None,
) -> dict[str, Any]:
    workflow = workflow_show(config, workflow_id)
    if not workflow["enabled"]:
        raise RuntimeError(f"Workflow is disabled: {workflow_id}")
    _approval(config, workflow)
    exec_id = _execution_id(str(workflow["workflow_id"]))
    state = {
        "version": 1,
        "exec_id": exec_id,
        "workflow_id": workflow["workflow_id"],
        "workflow_name": workflow["name"],
        "execution_mode": workflow["execution_mode"],
        "risk_level": workflow["risk_level"],
        "approval_status": "approved",
        "status": "queued",
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "updated": dt.datetime.now().isoformat(timespec="seconds"),
        "start_time": "",
        "end_time": "",
        "duration_seconds": 0.0,
        "current_stage": "",
        "completed_stages": 0,
        "stage_count": 0,
        "outputs": [],
        "errors": [],
        "logs": [],
        "task_id": "",
        "worker_pid": None,
        "cancel_requested": False,
        "recoverable": True,
        "n8n_execution_id": "",
    }
    _append_log(config, state, "Execution approved and queued.")
    _save_execution(config, state)
    command = [
        sys.executable,
        str(Path(__file__).resolve().parent.parent / "raphael.py"),
        "--config",
        str(settings_path or legacy.DEFAULT_SETTINGS_PATH),
        "workflow-worker",
        exec_id,
    ]
    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    log_path = runner_root(config) / "logs" / f"{exec_id}-worker.log"
    with log_path.open("a", encoding="utf-8") as stream:
        process = subprocess.Popen(
            command,
            cwd=str(Path(__file__).resolve().parent.parent),
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=stream,
            creationflags=creationflags,
        )
    state["worker_pid"] = process.pid
    _append_log(config, state, f"Fixed internal workflow worker started with PID {process.pid}.")
    _save_execution(config, state)
    return workflow_monitor(config, exec_id)


def _cancelled(config: legacy.RaphaelConfig, exec_id: str) -> bool:
    return bool(_load_execution(config, exec_id).get("cancel_requested"))


def _run_steps(
    config: legacy.RaphaelConfig,
    state: dict[str, Any],
    steps: list[tuple[str, Callable[[], Any]]],
) -> None:
    state["stage_count"] = len(steps)
    _save_execution(config, state)
    for index, (name, function) in enumerate(steps, 1):
        if _cancelled(config, state["exec_id"]):
            raise InterruptedError("Cancellation requested between workflow stages.")
        state = _load_execution(config, state["exec_id"])
        state["current_stage"] = name
        _append_log(config, state, f"Stage {index}/{len(steps)} started: {name}")
        _save_execution(config, state)
        output = function()
        state = _load_execution(config, state["exec_id"])
        state["outputs"].append({"stage": name, "result": legacy.redact_secrets(str(output))})
        state["completed_stages"] = index
        _append_log(config, state, f"Stage {index}/{len(steps)} completed: {name}")
        _save_execution(config, state)


def _pod_steps(config: legacy.RaphaelConfig, workflow: dict[str, Any]) -> list[tuple[str, Callable[[], Any]]]:
    holder: dict[str, str] = {}

    def start() -> str:
        result = pod_workflow.pod_workflow(config, str(workflow["source"]))
        holder["id"] = result["workflow_id"]
        return json.dumps(result)

    def advance() -> str:
        result = pod_workflow.pod_workflow_continue(config, holder["id"])
        return json.dumps(result)

    return [("initialize POD workflow", start)] + [(f"POD stage {index}", advance) for index in range(3, 14)]


def _knowledge_steps(config: legacy.RaphaelConfig) -> list[tuple[str, Callable[[], Any]]]:
    def import_registered() -> str:
        sources = legacy.knowledge_registered_sources(config)
        if not sources:
            return "No registered source folders; import stage safely skipped."
        return "\n".join(legacy.knowledge_import(config, path) for path in sources)

    return [
        ("import registered sources", import_registered),
        ("summarize knowledge", lambda: legacy.knowledge_summarize(config)),
        ("classify knowledge", lambda: legacy.knowledge_classify(config)),
        ("map relationships", lambda: legacy.knowledge_relationships(config)),
        ("index generated summaries", lambda: legacy.knowledge_index(config)),
    ]


def _brief_steps(config: legacy.RaphaelConfig) -> list[tuple[str, Callable[[], Any]]]:
    return [
        ("review tasks", lambda: legacy.generate_task_review(config)),
        ("review goals", lambda: legacy.goal_review(config)),
        ("review communications", lambda: legacy.communication_review(config)),
        ("review knowledge updates", lambda: legacy.knowledge_review(config)),
        ("generate morning brief", lambda: legacy.morning_brief(config)),
        ("generate executive brief", lambda: legacy.executive_brief(config)),
    ]


def _n8n_request(config: legacy.RaphaelConfig, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
    if not config.n8n_allow_execution:
        raise RuntimeError("n8n execution is disabled in config/settings.json.")
    url = "http://127.0.0.1:5678" + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"n8n HTTP {exc.code}: {body_text[:2000]}") from exc


def _validate_n8n_workflow(config: legacy.RaphaelConfig, workflow_data: dict[str, Any]) -> None:
    nodes = workflow_data.get("nodes", [])
    if not isinstance(nodes, list) or not nodes:
        raise RuntimeError("n8n workflow has no nodes.")
    for node in nodes:
        node_type = str(node.get("type", ""))
        if node.get("credentials"):
            raise RuntimeError(f"n8n workflow node `{node.get('name', '')}` requires credentials.")
        if not config.n8n_allow_external_calls and any(term.casefold() in node_type.casefold() for term in BLOCKED_N8N_TERMS):
            raise RuntimeError(f"n8n workflow contains blocked external-action node type: {node_type}")
    triggers = {str(node.get("type", "")) for node in nodes}
    if not triggers.intersection(SAFE_N8N_TRIGGER_TYPES):
        raise RuntimeError("n8n workflow must use a local manual or execute-workflow trigger.")


def n8n_run_registered(config: legacy.RaphaelConfig, workflow: dict[str, Any], state: dict[str, Any]) -> None:
    n8n_id = str(workflow["source"]).strip()
    if not n8n_id:
        raise RuntimeError("Registered n8n workflow is missing its source workflow ID.")
    details = _n8n_request(config, "GET", f"/rest/workflows/{n8n_id}")
    workflow_data = details.get("data", details)
    _validate_n8n_workflow(config, workflow_data)
    response = _n8n_request(config, "POST", f"/rest/workflows/{n8n_id}/run", {"workflowData": workflow_data})
    execution = response.get("data", response)
    execution_id = str(execution.get("executionId") or execution.get("id") or "")
    if not execution_id:
        raise RuntimeError(f"n8n did not return an execution ID: {response}")
    state["n8n_execution_id"] = execution_id
    state["stage_count"] = 1
    state["current_stage"] = "n8n execution"
    _append_log(config, state, f"n8n execution started: {execution_id}")
    _save_execution(config, state)
    while True:
        if _cancelled(config, state["exec_id"]):
            try:
                _n8n_request(config, "DELETE", f"/rest/executions-current/{execution_id}")
            except Exception as exc:
                state = _load_execution(config, state["exec_id"])
                _append_log(config, state, f"n8n stop request could not be confirmed: {exc}")
                _save_execution(config, state)
            raise InterruptedError("Cancellation requested while monitoring n8n.")
        payload = _n8n_request(config, "GET", f"/rest/executions/{execution_id}")
        record = payload.get("data", payload)
        status = str(record.get("status") or ("completed" if record.get("finished") else "running")).lower()
        if status in {"success", "completed"}:
            state = _load_execution(config, state["exec_id"])
            state["completed_stages"] = 1
            state["outputs"].append({"stage": "n8n execution", "result": legacy.redact_secrets(json.dumps(record))})
            _save_execution(config, state)
            return
        if status in {"error", "failed", "crashed"}:
            raise RuntimeError(f"n8n execution failed: {json.dumps(record)[:3000]}")
        time.sleep(2)


def workflow_worker(config: legacy.RaphaelConfig, exec_id: str) -> dict[str, Any]:
    state = _load_execution(config, exec_id)
    if state["status"] == "cancelled" or state.get("cancel_requested"):
        return workflow_monitor(config, exec_id)
    workflow = workflow_show(config, state["workflow_id"])
    started = dt.datetime.now()
    state["status"] = "running"
    state["start_time"] = started.isoformat(timespec="seconds")
    state["task_id"] = _create_task(config, workflow, exec_id)
    _append_log(config, state, "Workflow worker entered running state.")
    _save_execution(config, state)
    old_confirmation = os.environ.get("RAPHAEL_CONFIRMED")
    os.environ["RAPHAEL_CONFIRMED"] = "YES"
    try:
        if workflow["execution_mode"] == "n8n":
            n8n_run_registered(config, workflow, state)
        elif workflow["workflow_id"] == "pod-pipeline":
            _run_steps(config, state, _pod_steps(config, workflow))
        elif workflow["workflow_id"] == "knowledge-processing":
            _run_steps(config, state, _knowledge_steps(config))
        elif workflow["workflow_id"] == "daily-executive-brief":
            _run_steps(config, state, _brief_steps(config))
        else:
            raise RuntimeError(f"No native implementation for registered workflow: {workflow['workflow_id']}")
        state = _load_execution(config, exec_id)
        state["status"] = "completed"
        state["recoverable"] = False
        _append_log(config, state, "Workflow completed successfully.")
        _update_task(config, state, "Done", f"Workflow execution {exec_id} completed.")
    except InterruptedError as exc:
        state = _load_execution(config, exec_id)
        state["status"] = "cancelled"
        state["errors"].append(str(exc))
        _append_log(config, state, str(exc))
        _update_task(config, state, "Blocked", f"Workflow execution {exec_id} was cancelled.")
    except Exception as exc:
        state = _load_execution(config, exec_id)
        state["status"] = "failed"
        state["errors"].append(legacy.redact_secrets(str(exc)))
        _append_log(config, state, f"Workflow failed: {exc}")
        _update_task(config, state, "Blocked", f"Workflow execution {exec_id} failed: {exc}")
    finally:
        if old_confirmation is None:
            os.environ.pop("RAPHAEL_CONFIRMED", None)
        else:
            os.environ["RAPHAEL_CONFIRMED"] = old_confirmation
    ended = dt.datetime.now()
    state["end_time"] = ended.isoformat(timespec="seconds")
    state["duration_seconds"] = round((ended - started).total_seconds(), 3)
    state["current_stage"] = ""
    _save_execution(config, state)
    return workflow_monitor(config, exec_id)


def workflow_monitor(config: legacy.RaphaelConfig, exec_id: str) -> dict[str, Any]:
    state = _load_execution(config, exec_id)
    if state["status"] in {"queued", "running"} and state.get("worker_pid") and not state.get("start_time"):
        state["monitor_note"] = "Worker is starting."
    else:
        state["monitor_note"] = ""
    return state


def workflow_result(config: legacy.RaphaelConfig, exec_id: str) -> dict[str, Any]:
    state = workflow_monitor(config, exec_id)
    if state["status"] not in FINAL_STATUSES:
        return {"exec_id": exec_id, "status": state["status"], "ready": False, "message": "Execution is not finished."}
    return {
        "exec_id": state["exec_id"],
        "workflow_id": state["workflow_id"],
        "status": state["status"],
        "ready": True,
        "start_time": state["start_time"],
        "end_time": state["end_time"],
        "duration_seconds": state["duration_seconds"],
        "outputs": state["outputs"],
        "errors": state["errors"],
        "logs": state["logs"],
        "task_id": state["task_id"],
        "recoverable": state["recoverable"],
        "n8n_execution_id": state.get("n8n_execution_id", ""),
    }


def workflow_cancel(config: legacy.RaphaelConfig, exec_id: str) -> dict[str, Any]:
    legacy.pod_confirmation_granted(f"Cancel registered workflow execution {exec_id}?")
    state = _load_execution(config, exec_id)
    if state["status"] in FINAL_STATUSES:
        return state
    state["cancel_requested"] = True
    if state["status"] == "queued" and not state.get("start_time"):
        state["status"] = "cancelled"
        state["end_time"] = dt.datetime.now().isoformat(timespec="seconds")
    _append_log(config, state, "Cancellation requested; no unrelated process will be terminated.")
    _save_execution(config, state)
    return state


def executions(config: legacy.RaphaelConfig) -> list[dict[str, Any]]:
    ensure_runner(config)
    rows = []
    for path in sorted((runner_root(config) / "executions").glob("WFEXEC-*.json"), key=lambda value: value.stat().st_mtime, reverse=True):
        try:
            rows.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return rows


def workflow_failures(config: legacy.RaphaelConfig) -> dict[str, Any]:
    rows = [row for row in executions(config) if row["status"] == "failed"]
    return {"count": len(rows), "failures": rows}


def runner_status(config: legacy.RaphaelConfig) -> dict[str, Any]:
    rows = executions(config)
    n8n_healthy = False
    n8n_error = ""
    try:
        with urllib.request.urlopen("http://127.0.0.1:5678/healthz", timeout=3) as response:
            n8n_healthy = response.status == 200
    except Exception as exc:
        n8n_error = str(exc)
    return {
        "enabled": True,
        "registry": str(registry_path(config)),
        "runtime": str(runner_root(config)),
        "workflow_count": len(load_registry(config)),
        "active": sum(1 for row in rows if row["status"] == "running"),
        "queued": sum(1 for row in rows if row["status"] == "queued"),
        "completed": sum(1 for row in rows if row["status"] == "completed"),
        "failed": sum(1 for row in rows if row["status"] == "failed"),
        "cancelled": sum(1 for row in rows if row["status"] == "cancelled"),
        "n8n_url": "http://127.0.0.1:5678",
        "n8n_healthy": n8n_healthy,
        "n8n_error": n8n_error,
        "safety": {
            "registered_only": True,
            "arbitrary_shell": False,
            "browser_automation": False,
            "external_actions": False,
            "credentials": False,
        },
    }


def workflow_review(config: legacy.RaphaelConfig) -> Path:
    rows = executions(config)
    content = f"""# Workflow Review

Generated: {dt.datetime.now().isoformat(timespec="seconds")}

- Registered workflows: {len(load_registry(config))}
- Active: {sum(1 for row in rows if row["status"] == "running")}
- Queued: {sum(1 for row in rows if row["status"] == "queued")}
- Completed: {sum(1 for row in rows if row["status"] == "completed")}
- Failed: {sum(1 for row in rows if row["status"] == "failed")}
- Cancelled: {sum(1 for row in rows if row["status"] == "cancelled")}

## Recoverable Failures

{chr(10).join(f"- `{row['exec_id']}` {row['workflow_name']}: {row['errors'][-1] if row['errors'] else 'Unknown error'}" for row in rows if row["status"] == "failed") or "- None."}

## Safety

Only registered local workflows execute. External business actions, browser
automation, credentials, arbitrary commands, publishing, uploads, spending, and
messaging remain blocked.
"""
    output = notes_root(config) / "Workflow Review.md"
    legacy.write_generated_note(output, content, config)
    return output


def _write_notes(config: legacy.RaphaelConfig) -> None:
    root = notes_root(config)
    workflows = json.loads(registry_path(config).read_text(encoding="utf-8")).get("workflows", []) if registry_path(config).exists() else DEFAULT_REGISTRY
    rows = []
    for item in workflows:
        rows.append(
            f"| {item['workflow_id']} | {item['name']} | {item['category']} | {item['execution_mode']} | "
            f"{item['risk_level']} | {item['approval_required']} | {item['enabled']} | {item['source']} |"
        )
    legacy.write_generated_note(
        root / "Workflow Registry.md",
        "# Workflow Registry\n\n| Workflow ID | Name | Category | Mode | Risk | Approval | Enabled | Source |\n"
        "|---|---|---|---|---|---|---|---|\n" + "\n".join(rows),
        config,
    )
    execution_rows = executions(config) if (runner_root(config) / "executions").exists() else []
    blocks = []
    for row in execution_rows:
        blocks.append(
            f"## {row['exec_id']}\n\n- Workflow: {row['workflow_name']} (`{row['workflow_id']}`)\n"
            f"- Status: {row['status']}\n- Approval: {row['approval_status']}\n"
            f"- Started: {row['start_time'] or 'Not started'}\n- Ended: {row['end_time'] or 'Not ended'}\n"
            f"- Duration: {row['duration_seconds']} seconds\n- Task: {row['task_id'] or 'None'}\n"
        )
    legacy.write_generated_note(root / "Workflow Executions.md", "# Workflow Executions\n\n" + ("\n".join(blocks) or "No executions recorded yet."), config)
    result_blocks = [
        f"## {row['exec_id']}\n\n```json\n{json.dumps(row['outputs'], indent=2)}\n```"
        for row in execution_rows if row["status"] == "completed"
    ]
    failure_blocks = [
        f"## {row['exec_id']}\n\n- Workflow: {row['workflow_name']}\n- Recoverable: {row['recoverable']}\n"
        f"- Error: {row['errors'][-1] if row['errors'] else 'Unknown'}\n"
        for row in execution_rows if row["status"] == "failed"
    ]
    legacy.write_generated_note(root / "Workflow Results.md", "# Workflow Results\n\n" + ("\n".join(result_blocks) or "No completed results recorded yet."), config)
    legacy.write_generated_note(root / "Workflow Failures.md", "# Workflow Failures\n\n" + ("\n".join(failure_blocks) or "No failures recorded yet."), config)
