"""Phase 65 Daily Operating Loop.

This module generates advisory daily notes from existing Raphael OS records.
It never executes work, creates tasks, spends money, publishes, or performs
external actions.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Any

from . import legacy


ACTIVE_TASK_STATUSES = {"open", "in progress", "ready for review", "waiting", "blocked"}
DONE_TASK_STATUSES = {"done", "completed"}
PRIORITY_ORDER = {"critical": 0, "high": 1, "urgent": 1, "medium": 2, "normal": 3, "low": 4}


def daily_root(config: legacy.RaphaelConfig) -> Path:
    return config.vault / "00_Raphael" / "Daily Operating Loop"


def _dated_path(config: legacy.RaphaelConfig, label: str) -> Path:
    return daily_root(config) / f"{legacy.today()} {label}.md"


def _task_sort_key(task: dict[str, str]) -> tuple[int, int, str]:
    status = task.get("status", "").lower()
    status_rank = 0 if status == "in progress" else 1 if status == "open" else 2
    return (
        PRIORITY_ORDER.get(task.get("priority", "normal").lower(), 3),
        status_rank,
        task.get("id", ""),
    )


def _context(config: legacy.RaphaelConfig) -> dict[str, Any]:
    tasks = legacy.all_agent_tasks(config)
    open_tasks = sorted(
        [task for task in tasks if task.get("status", "").lower() in ACTIVE_TASK_STATUSES],
        key=_task_sort_key,
    )
    blocked_tasks = [
        task for task in open_tasks if task.get("status", "").lower() in {"blocked", "waiting"}
    ]
    done_tasks = [task for task in tasks if task.get("status", "").lower() in DONE_TASK_STATUSES]
    notifications = [
        row
        for row in legacy.read_notifications(config)
        if row.get("Status", "").lower() not in {"dismissed", "resolved", "done"}
    ]
    warnings = [
        row for row in notifications if row.get("Severity", "").lower() in {"critical", "high"}
    ]
    kpi_warnings = [
        row for row in legacy.read_kpis(config) if row.get("status", "").lower() in {"behind", "at risk"}
    ]
    goals = [
        row for row in legacy.parse_goals(config) if row.get("status", "").lower() in {"active", "open", "in progress"}
    ]
    portfolio = legacy.portfolio_context(config)
    resource = legacy.resource_profile(config)
    return {
        "tasks": tasks,
        "open_tasks": open_tasks,
        "blocked_tasks": blocked_tasks,
        "done_tasks": done_tasks,
        "notifications": notifications,
        "warnings": warnings,
        "kpi_warnings": kpi_warnings,
        "goals": goals,
        "portfolio": portfolio,
        "resource": resource,
        "execution_plan_count": len(legacy.execution_plan_files(config)),
        "deliberation_count": len(legacy.deliberation_files(config)),
    }


def _top_priority(ctx: dict[str, Any]) -> str:
    tasks: list[dict[str, str]] = ctx["open_tasks"]
    if tasks:
        task = tasks[0]
        return f"{task.get('task', task.get('name', 'Top task'))} ({task.get('id', 'untracked')})"
    goals: list[dict[str, str]] = ctx["goals"]
    if goals:
        return f"{goals[0].get('title', 'Active goal')} ({goals[0].get('id', 'goal')})"
    portfolio: list[dict[str, object]] = ctx["portfolio"]
    if portfolio:
        return str(portfolio[0].get("Recommended Action", portfolio[0].get("Business Name", "Review portfolio")))
    return "Review current commitments and choose one concrete next action."


def _task_lines(tasks: list[dict[str, str]], limit: int = 3) -> str:
    if not tasks:
        return "- No open tracked tasks. Review goals before creating new work."
    return "\n".join(
        f"- [{task.get('status', 'Open')}] {task.get('task', task.get('name', 'Task'))} "
        f"— {task.get('id', 'untracked')} · {task.get('agent', 'Unassigned')}"
        for task in tasks[:limit]
    )


def _warning_lines(ctx: dict[str, Any]) -> str:
    lines: list[str] = []
    for row in ctx["warnings"][:5]:
        lines.append(
            f"- {row.get('Severity', 'High')}: {row.get('Title', row.get('Notification ID', 'Notification'))}"
        )
    for task in ctx["blocked_tasks"][:5]:
        lines.append(f"- {task.get('status', 'Blocked')}: {task.get('task', task.get('name', 'Task'))}")
    for row in ctx["kpi_warnings"][:5]:
        lines.append(f"- KPI {row.get('name', row.get('id', 'Unknown'))}: {row.get('status', 'At Risk')}")
    return "\n".join(lines) if lines else "- No critical warnings detected in current Raphael records."


def _boundary() -> str:
    return (
        "This daily note is advisory. Raphael did not execute actions, create tasks, spend money, "
        "publish, deploy, or contact external systems."
    )


def _write(config: legacy.RaphaelConfig, path: Path, content: str) -> Path:
    legacy.write_generated_note(path, content.rstrip() + "\n", config)
    return path


def daily_start(config: legacy.RaphaelConfig) -> Path:
    morning = legacy.morning_brief(config)
    ctx = _context(config)
    priority = _top_priority(ctx)
    top_portfolio = ctx["portfolio"][0] if ctx["portfolio"] else {}
    content = f"""# Daily Start

Generated: {dt.datetime.now().isoformat(timespec="seconds")}

## Morning Brief

- Existing Executive Brief: `{morning}`
- Active goals: {len(ctx["goals"])}
- Open tasks: {len(ctx["open_tasks"])}
- Active execution plans: {ctx["execution_plan_count"]}
- Deliberations tracked: {ctx["deliberation_count"]}

## Top Priority

{priority}

## Top 3 Tasks

{_task_lines(ctx["open_tasks"])}

## Warnings

{_warning_lines(ctx)}

## Recommended First Action

- Open the top task and define the smallest finishable step before starting new work.
- Portfolio signal: {top_portfolio.get("Recommended Action", "Review the highest-priority active goal.")}

## Resource Snapshot

- Weekly hours available: {ctx["resource"].get("weekly_hours", 0):g}
- Focus slots available: {ctx["resource"].get("focus_slots", 0):g}
- Weekly budget available: ${ctx["resource"].get("weekly_budget", 0):g} (informational only)

## Suggested Next Command

`python raphael.py daily-plan`

## Safety Boundary

{_boundary()}
"""
    return _write(config, _dated_path(config, "Daily Start"), content)


def daily_focus(config: legacy.RaphaelConfig) -> Path:
    ctx = _context(config)
    content = f"""# Daily Focus

Generated: {dt.datetime.now().isoformat(timespec="seconds")}

## Today's Focus

{_top_priority(ctx)}

## Top 3 Tasks

{_task_lines(ctx["open_tasks"])}

## Protect Attention From

{_warning_lines(ctx)}

## Recommendation

- Complete one meaningful step on the top priority before switching contexts.

## Safety Boundary

{_boundary()}
"""
    return _write(config, _dated_path(config, "Daily Focus"), content)


def daily_plan(config: legacy.RaphaelConfig) -> Path:
    ctx = _context(config)
    tasks: list[dict[str, str]] = ctx["open_tasks"]
    first = tasks[0].get("task", "Advance the top priority") if tasks else _top_priority(ctx)
    second = tasks[1].get("task", "Continue the top priority or review an active goal") if len(tasks) > 1 else "Continue the top priority or review an active goal"
    portfolio_action = (
        str(ctx["portfolio"][0].get("Recommended Action", "Review a creative or business opportunity"))
        if ctx["portfolio"]
        else "Optional: review a creative or business opportunity"
    )
    content = f"""# Daily Plan

Generated: {dt.datetime.now().isoformat(timespec="seconds")}

## Focus Block 1

- {first}
- Keep the block narrow and produce one reviewable result.

## Focus Block 2

- {second}
- Reassess after block 1; do not expand scope automatically.

## Admin Block

- Review notifications, update existing task notes if needed, and clear small administrative items.
- Do not create new tracked tasks without confirmation.

## Optional Creative / Business Block

- {portfolio_action}
- Skip this block if the primary work is unfinished or warnings require attention.

## Check-in Prompt

`python raphael.py daily-checkin "What changed, what moved, and what is blocked?"`

## Safety Boundary

{_boundary()}
"""
    return _write(config, _dated_path(config, "Daily Plan"), content)


def daily_checkin(config: legacy.RaphaelConfig, update: str = "") -> Path:
    path = _dated_path(config, "Check-ins")
    if path.exists():
        existing = legacy.read_text_if_exists(path, config)
    else:
        existing = f"""# Daily Check-ins

Date: {legacy.today()}

## Prompt

What changed? What moved? What is blocked? What should change in the rest of today's plan?

## Check-ins
"""
    boundary_heading = "\n\n## Safety Boundary\n"
    if boundary_heading in existing:
        existing = existing.split(boundary_heading, 1)[0].rstrip()
    existing = existing.replace(
        "\n\n_No update recorded yet. Run the command again with your update in quotes._",
        "",
    )
    clean = update.strip()
    if clean:
        existing = existing.rstrip() + f"\n\n### {dt.datetime.now().isoformat(timespec='seconds')}\n\n{clean}\n"
    elif "No update recorded" not in existing:
        existing = existing.rstrip() + "\n\n_No update recorded yet. Run the command again with your update in quotes._\n"
    existing = existing.rstrip() + f"\n\n## Safety Boundary\n\n{_boundary()}\n"
    return _write(config, path, existing)


def _today_activity(config: legacy.RaphaelConfig) -> list[str]:
    path = config.vault / "00_Raphael" / "Activity Stream" / "Activity Sources.md"
    text = legacy.read_text_if_exists(path, config, 300000) if path.exists() else ""
    today_text = legacy.today()
    lines: list[str] = []
    for block in text.split("### EVENT-")[1:]:
        if today_text not in block:
            continue
        title = legacy.section_value(block, "Title")
        if not title:
            for line in block.splitlines():
                if line.startswith("- Title:"):
                    title = line.split(":", 1)[1].strip()
                    break
        if title:
            lines.append(title)
    return lines[:10]


def daily_end(config: legacy.RaphaelConfig) -> Path:
    evening = legacy.evening_review(config)
    ctx = _context(config)
    activity = _today_activity(config)
    checkins = _dated_path(config, "Check-ins")
    checkin_text = legacy.read_text_if_exists(checkins, config, 12000) if checkins.exists() else ""
    done = "\n".join(f"- {item}" for item in activity) or _task_lines(ctx["done_tasks"], 8)
    moved = (
        f"- Daily check-ins were recorded in `{checkins}`.\n- {len(ctx['open_tasks'])} tasks remain active."
        if checkin_text
        else f"- No check-in note was recorded.\n- {len(ctx['open_tasks'])} tasks remain active."
    )
    content = f"""# Daily End

Generated: {dt.datetime.now().isoformat(timespec="seconds")}

## What Got Done

{done}

## What Moved

{moved}

## Blockers

{_warning_lines(ctx)}

## Tomorrow Recommendation

{_top_priority(ctx)}

## Existing Evening Review

`{evening}`

## Suggested Next Command

`python raphael.py daily-review`

## Safety Boundary

{_boundary()}
"""
    return _write(config, _dated_path(config, "Daily End"), content)


def daily_review(config: legacy.RaphaelConfig) -> Path:
    ctx = _context(config)
    root = daily_root(config)
    today_files = sorted(root.glob(f"{legacy.today()} *.md")) if root.exists() else []
    file_lines = "\n".join(f"- `{path}`" for path in today_files) or "- No daily notes generated yet."
    content = f"""# Daily Operating Loop Review

Generated: {dt.datetime.now().isoformat(timespec="seconds")}

## Today's Notes

{file_lines}

## Current Focus

{_top_priority(ctx)}

## Current Task Snapshot

- Open / active: {len(ctx["open_tasks"])}
- Blocked / waiting: {len(ctx["blocked_tasks"])}
- Done records: {len(ctx["done_tasks"])}

## Warnings

{_warning_lines(ctx)}

## Recommended Next Step

- If the day is starting, run `python raphael.py daily-start`.
- If work is underway, run `python raphael.py daily-checkin "your update"`.
- If the day is ending, run `python raphael.py daily-end`.

## Safety Boundary

{_boundary()}
"""
    return _write(config, root / "Daily Review.md", content)
