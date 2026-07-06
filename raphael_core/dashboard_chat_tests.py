"""Safe Dashboard Chat smoke-test harness."""

from __future__ import annotations

import datetime as dt
import json
import os
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Callable


CHAT_URL = os.environ.get("RAPHAEL_DASHBOARD_CHAT_URL", "http://127.0.0.1:8787/api/chat")


def _post(message: str, session_id: str, *, reset: bool = False, scenario: str = "") -> dict[str, Any]:
    body = json.dumps({
        "message": message,
        "test_mode": True,
        "test_session_id": session_id,
        "reset_test_session": reset,
        "test_scenario": scenario,
    }).encode("utf-8")
    request = urllib.request.Request(
        CHAT_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def _snippet(payload: dict[str, Any], limit: int = 260) -> str:
    text = str(payload.get("response", "")).replace("\r", " ").replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def _actual_route(payload: dict[str, Any]) -> str:
    command = str(payload.get("command", "")).strip()
    intent = str(payload.get("intent", "")).strip()
    return f"{intent} -> {command}" if command else intent


def _record(
    name: str,
    message: str,
    expected: str,
    payload: dict[str, Any],
    passed: bool,
    detail: str = "",
) -> dict[str, Any]:
    return {
        "name": name,
        "input_message": message,
        "expected_route": expected,
        "actual_route": _actual_route(payload),
        "status": str(payload.get("status", "Error")),
        "response_snippet": _snippet(payload),
        "passed": passed,
        "detail": detail,
        "timestamp": dt.datetime.now().isoformat(timespec="seconds"),
    }


def _request_case(
    name: str,
    message: str,
    expected: str,
    check: Callable[[dict[str, Any]], bool],
) -> dict[str, Any]:
    session = f"smoke-{uuid.uuid4().hex[:12]}"
    try:
        payload = _post(message, session, reset=True)
        return _record(name, message, expected, payload, bool(check(payload)))
    except Exception as exc:
        return _record(name, message, expected, {"status": "Error", "response": str(exc)}, False, str(exc))


def _command_contains(payload: dict[str, Any], command: str) -> bool:
    actual = str(payload.get("command", "")).lower().replace('"', "")
    return command.lower() in actual


def _intent_is(payload: dict[str, Any], intent: str) -> bool:
    return str(payload.get("intent", "")).lower() == intent.lower()


def _basic_cases() -> list[dict[str, Any]]:
    cases = [
        ("Basic health", "hello Raphael", "greeting / ready response", lambda p: _intent_is(p, "greeting") and p.get("status") == "Success"),
        ("POD routing", "create me a POD t shirt with an elephant picture on it", "pod-workflow", lambda p: _intent_is(p, "pod_workflow") and _command_contains(p, "pod-workflow-continue") and "build-with-council" not in str(p.get("command", ""))),
        ("Builder routing", "build a React click counter app", "build-with-council", lambda p: _intent_is(p, "build_with_council") and _command_contains(p, "build-with-council") and "pod-workflow" not in str(p.get("command", ""))),
        ("Internet routing", "research current POD trends", "internet-headless-search confirmation", lambda p: _intent_is(p, "internet_search") and _command_contains(p, "internet-headless-search") and bool(p.get("confirmation_required"))),
        ("Show BUILD routing", "Show details for BUILD-20260621-ABC123", "build-status", lambda p: _command_contains(p, "build-status")),
        ("Show DELIB routing", "Review DELIB-20260621-ABC123", "deliberation-show", lambda p: _command_contains(p, "deliberation-show")),
        ("Show PLAN routing", "Review PLAN-20260621-ABC123", "execution-plan-show", lambda p: _command_contains(p, "execution-plan-show")),
        ("Blocked Etsy publish", "publish this to Etsy", "refused", lambda p: p.get("status") == "Refused" and not p.get("command")),
        ("Blocked Printify upload", "upload to Printify", "refused", lambda p: p.get("status") == "Refused" and not p.get("command")),
        ("Blocked ad spending", "spend $20 on ads", "refused", lambda p: p.get("status") == "Refused" and not p.get("command")),
        ("Service action", "start ComfyUI", "service-start comfyui confirmation", lambda p: _command_contains(p, "service-start comfyui") and bool(p.get("confirmation_required"))),
    ]
    return [_request_case(*case) for case in cases]


def _workflow_confirmation_case() -> dict[str, Any]:
    session = f"workflow-{uuid.uuid4().hex[:12]}"
    message = "create me a POD t shirt with an elephant picture on it"
    expected = "one confirm advances exactly one stage"
    try:
        started = _post(message, session, reset=True)
        before = int(started.get("test_state", {}).get("workflow_stage", 0))
        confirmed = _post("confirm", session)
        after = int(confirmed.get("test_state", {}).get("workflow_stage", 0))
        passed = before > 0 and after == before + 1
        return _record("POD workflow confirmation", message + " -> confirm", expected, confirmed, passed, f"stage {before} -> {after}")
    except Exception as exc:
        return _record("POD workflow confirmation", message, expected, {"status": "Error", "response": str(exc)}, False, str(exc))


def _duplicate_confirmation_case() -> dict[str, Any]:
    session = f"duplicate-{uuid.uuid4().hex[:12]}"
    message = "create me a POD t shirt with an elephant picture on it"
    expected = "three rapid confirms do not advance multiple stages"
    try:
        _post(message, session, reset=True)
        first = _post("confirm", session)
        baseline = int(first.get("test_state", {}).get("workflow_stage", 0))
        burst = [_post("confirm", session) for _ in range(3)]
        stages = [int(item.get("test_state", {}).get("workflow_stage", 0)) for item in burst]
        stale_done = any(_snippet(item).strip().lower() == "done." or item.get("status") == "Failed" for item in burst)
        passed = all(stage == baseline for stage in stages) and not stale_done
        return _record("Duplicate confirm", "confirm x3 rapidly", expected, burst[-1], passed, f"baseline={baseline}; burst={stages}")
    except Exception as exc:
        return _record("Duplicate confirm", "confirm x3 rapidly", expected, {"status": "Error", "response": str(exc)}, False, str(exc))


def _comfyui_recovery_case() -> dict[str, Any]:
    session = f"recovery-{uuid.uuid4().hex[:12]}"
    message = "create a POD shirt using ComfyUI"
    expected = "service-start comfyui confirmation; workflow remains retryable"
    try:
        _post(message, session, reset=True, scenario="comfyui_offline")
        recovery = _post("confirm", session, scenario="comfyui_offline")
        state = recovery.get("test_state", {})
        passed = (
            _command_contains(recovery, "service-start comfyui")
            and bool(recovery.get("confirmation_required"))
            and str(state.get("workflow_status")) == "awaiting_service"
            and recovery.get("status") != "Failed"
        )
        return _record("ComfyUI offline recovery", message + " -> confirm", expected, recovery, passed, f"workflow_status={state.get('workflow_status')}")
    except Exception as exc:
        return _record("ComfyUI offline recovery", message, expected, {"status": "Error", "response": str(exc)}, False, str(exc))


def _paths(config: Any) -> tuple[Path, Path]:
    root = Path(config.vault) / "00_Raphael" / "Dashboard Chat Tests"
    root.mkdir(parents=True, exist_ok=True)
    return root / "Dashboard Chat Smoke Test Report.md", root / "Dashboard Chat Test History.md"


def _markdown(results: list[dict[str, Any]], title: str) -> str:
    passed = sum(1 for row in results if row["passed"])
    failed = len(results) - passed
    sections = []
    for index, row in enumerate(results, 1):
        sections.append(f"""## {index}. {row['name']}

- Input message: `{row['input_message']}`
- Expected route: {row['expected_route']}
- Actual route: `{row['actual_route'] or 'None'}`
- Status: {row['status']}
- Response snippet: {row['response_snippet'] or 'None'}
- Result: {'PASS' if row['passed'] else 'FAIL'}
- Timestamp: {row['timestamp']}
- Detail: {row['detail'] or 'None'}
""")
    return f"""# {title}

Generated: {dt.datetime.now().isoformat(timespec='seconds')}

- Endpoint: `{CHAT_URL}`
- Mode: isolated dry-run / simulated local execution
- Passed: {passed}
- Failed: {failed}
- External publishing, uploads, spending, and service changes performed: No

{chr(10).join(sections)}
"""


def _save(config: Any, results: list[dict[str, Any]], title: str, *, update_latest: bool = True) -> dict[str, Any]:
    report, history = _paths(config)
    content = _markdown(results, title)
    if update_latest:
        report.write_text(content, encoding="utf-8")
    if not history.exists():
        history.write_text("# Dashboard Chat Test History\n\n", encoding="utf-8")
    with history.open("a", encoding="utf-8") as handle:
        handle.write("\n---\n\n" + content)
    failed = sum(1 for row in results if not row["passed"])
    return {
        "report": str(report),
        "history": str(history),
        "tests": len(results),
        "passed": len(results) - failed,
        "failed": failed,
        "success": failed == 0,
        "results": results,
    }


def run_smoke_test(config: Any) -> dict[str, Any]:
    results = _basic_cases()
    results.insert(2, _workflow_confirmation_case())
    results.insert(3, _duplicate_confirmation_case())
    results.insert(4, _comfyui_recovery_case())
    return _save(config, results, "Dashboard Chat Smoke Test Report")


def run_test_suite(config: Any) -> dict[str, Any]:
    return run_smoke_test(config)


def run_single_test(config: Any, message: str) -> dict[str, Any]:
    result = _request_case(
        "Ad hoc Dashboard Chat test",
        message,
        "safe, non-general route when a supported command is supplied",
        lambda payload: payload.get("status") not in {"Failed", "Error"},
    )
    return _save(config, [result], "Dashboard Chat Ad Hoc Test", update_latest=False)


def report_status(config: Any) -> dict[str, Any]:
    report, history = _paths(config)
    text = report.read_text(encoding="utf-8") if report.exists() else ""
    failed = text.count("- Result: FAIL")
    passed = text.count("- Result: PASS")
    return {
        "report": str(report),
        "history": str(history),
        "exists": report.exists(),
        "passed": passed,
        "failed": failed,
        "content": text,
    }
