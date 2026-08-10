from __future__ import annotations

import datetime as dt
import time
import importlib.util
import json
import os
import re
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
class DummyApp:
    def __init__(self):
        self.routes = []
    def get(self, *args, **kwargs): return lambda f: f
    def post(self, *args, **kwargs): return lambda f: f
    def mount(self, *args, **kwargs): pass
app = DummyApp()
APP_DIR = Path(__file__).resolve().parent
if "RAPHAEL_CLI_PATH" in os.environ:
    REPO_DIR = Path(os.environ["RAPHAEL_CLI_PATH"]).parent
else:
    REPO_DIR = APP_DIR.parent

if str(REPO_DIR) not in sys.path:
    sys.path.insert(0, str(REPO_DIR))

CONFIG_PATH = Path(os.environ.get("RAPHAEL_CONFIG_PATH", str(REPO_DIR / "config.json")))
DASHBOARD_CHAT_LOG = APP_DIR / "logs" / "Dashboard Chat Log.md"
PENDING_CHAT_ROUTE: dict[str, Any] = {"route": None, "phrase": ""}
COMMAND_BUS_SESSION: dict[str, Any] = {}
SERVICE_COMMAND_BUS_SESSION: dict[str, Any] = {}
WORKFLOW_COMMAND_BUS_SESSION: dict[str, Any] = {}
SELF_HEALING_COMMAND_BUS_SESSION: dict[str, Any] = {}
DASHBOARD_CHAT_TEST_SESSIONS: dict[str, dict[str, Any]] = {}
DASHBOARD_CHAT_TEST_LOCK = threading.RLock()

def load_settings() -> dict[str, Any]:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {
        "vault_path": "R:/RaphaelOS/Ralphael",
        "runtime_path": "R:/RaphaelOS",
        "qdrant_url": "http://localhost:6333",
        "vision_model": "qwen2.5vl",
    }


def vault_path() -> Path:
    import json
    import os
    config_path = os.environ.get("RAPHAEL_CONFIG_PATH") or (REPO_DIR / "config.json")
    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            if "vault_path" in config:
                return Path(config["vault_path"])
    return Path(os.environ.get("RAPHAEL_VAULT_DIR", str(REPO_DIR / "Ralphael")))

def runtime_path() -> Path:
    import json
    import os
    config_path = os.environ.get("RAPHAEL_CONFIG_PATH") or (REPO_DIR / "config.json")
    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            if "runtime_path" in config:
                return Path(config["runtime_path"])
    return Path(os.environ.get("RAPHAEL_RUNTIME_DIR", str(REPO_DIR / "runtime")))


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, UnicodeDecodeError, OSError):
        return ""
    if limit and len(text) > limit:
        return text[:limit].rstrip() + "\n\n[TRUNCATED_FOR_DASHBOARD]"
    return text


def section_value(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}[ \t]*\r?\n+(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    return match.group(1).strip() if match else ""


def subsection_value(text: str, heading: str) -> str:
    pattern = rf"^### {re.escape(heading)}[ \t]*\r?\n+(.*?)(?=^### |\Z)"
    match = re.search(pattern, text, flags=re.M | re.S)
    return match.group(1).strip() if match else ""


def excerpt(text: str, limit: int = 700) -> str:
    clean = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(clean) <= limit:
        return clean
    return clean[: limit - 3].rstrip() + "..."


def note_card(label: str, rel_path: str) -> dict[str, Any]:
    try:
        path = vault_path() / rel_path
        exists = path.exists()
        updated = dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds") if exists else ""
        text = read_text(path, 4000) if exists else ""
        return {
            "label": label,
            "path": str(path),
            "exists": exists,
            "updated": updated,
            "content": excerpt(text, 1100) if text else "",
        }
    except Exception as e:
        return {
            "label": label,
            "path": rel_path,
            "exists": False,
            "updated": "",
            "content": "",
        }


def current_mode() -> dict[str, str]:
    text = read_text(vault_path() / "00_Raphael" / "Current Mode.md")
    return {
        "mode": section_value(text, "Mode") or "Unknown",
        "focus": section_value(text, "Focus"),
        "updated": section_value(text, "Updated"),
    }


def projects() -> list[dict[str, Any]]:
    root = vault_path() / "02_Projects"
    items: list[dict[str, Any]] = []
    if not root.exists():
        return items
    for folder in sorted(path for path in root.iterdir() if path.is_dir()):
        health = read_text(folder / "Project Health.md", 3000)
        overview = read_text(folder / "Overview.md", 1200)
        score_match = re.search(r"(\d{1,3})/100", health or "")
        items.append(
            {
                "name": folder.name,
                "path": str(folder),
                "status": section_value(health, "Status") or "Unknown",
                "score": int(score_match.group(1)) if score_match else None,
                "has_summary": (folder / "Project Summary.md").exists(),
                "has_health": (folder / "Project Health.md").exists(),
                "overview": excerpt(overview, 350),
            }
        )
    return items


def goals() -> list[dict[str, str]]:
    text = read_text(vault_path() / "00_Raphael" / "Goals.md")
    items: list[dict[str, str]] = []
    for match in re.finditer(r"^## (GOAL-[A-Z0-9-]+)\s+(.+?)(?=^## GOAL-|\Z)", text, flags=re.M | re.S):
        body = match.group(2)
        items.append(
            {
                "id": match.group(1),
                "title": subsection_value(body, "Title"),
                "status": subsection_value(body, "Status"),
                "priority": subsection_value(body, "Priority"),
                "milestone": subsection_value(body, "Next Milestone"),
            }
        )
    return items


def goal_propagation_data() -> dict[str, Any]:
    root = vault_path() / "00_Raphael" / "Goal Propagation"
    plans_root = root / "Goal Cascade Plans"
    plans: list[dict[str, Any]] = []
    if plans_root.exists():
        for path in sorted(plans_root.glob("GOAL-* - Cascade Plan.md"), key=lambda value: value.stat().st_mtime, reverse=True):
            text = read_text(path, 30000)
            goal_match = re.search(r"- ID: `([^`]+)`", text)
            title_match = re.search(r"- Title:\s*(.+)", text)
            councils: list[str] = []
            employees: list[dict[str, str]] = []
            for line in section_value(text, "Council Objectives").splitlines():
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) >= 3 and cells[0] != "Council" and not set(cells[0]) <= {"-", ":"}:
                    councils.append(cells[0])
            for line in section_value(text, "Employee Responsibilities").splitlines():
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) >= 3 and cells[0] != "Employee" and not set(cells[0]) <= {"-", ":"}:
                    employees.append({"employee": cells[0], "council": cells[1]})
            plans.append({
                "goal_id": goal_match.group(1) if goal_match else path.name.split(" - ", 1)[0],
                "title": title_match.group(1).strip() if title_match else path.stem,
                "councils": list(dict.fromkeys(councils)),
                "employees": employees,
                "path": str(path),
                "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            })
    return {
        "enabled": bool(load_settings().get("goal_propagation_enabled", True)),
        "plans": plans,
        "registry": note_card("Propagation Registry", "00_Raphael/Goal Propagation/Goal Propagation Registry.md"),
        "cascade_index": note_card("Cascade Plans", "00_Raphael/Goal Propagation/Goal Cascade Plans.md"),
        "council_objectives": note_card("Council Objectives", "00_Raphael/Goal Propagation/Council Objectives.md"),
        "department_objectives": note_card("Department Objectives", "00_Raphael/Goal Propagation/Department Objectives.md"),
        "employee_objectives": note_card("Employee Objectives", "00_Raphael/Goal Propagation/Employee Objectives.md"),
        "kpi_map": note_card("Goal KPI Map", "00_Raphael/Goal Propagation/Goal KPI Map.md"),
        "initiative_map": note_card("Goal Initiative Map", "00_Raphael/Goal Propagation/Goal Initiative Map.md"),
        "review_cycles": note_card("Review Cycles", "00_Raphael/Goal Propagation/Goal Review Cycles.md"),
        "review": note_card("Propagation Review", "00_Raphael/Goal Propagation/Goal Propagation Review.md"),
        "brief": note_card("Propagation Brief", "00_Raphael/Goal Propagation/Goal Propagation Brief.md"),
    }


def deliberation_data() -> dict[str, Any]:
    root = vault_path() / "00_Raphael" / "Deliberations"
    records: list[dict[str, Any]] = []
    if root.exists():
        for path in sorted(root.glob("DELIB-*.md"), key=lambda value: value.stat().st_mtime, reverse=True):
            text = read_text(path, 50000)
            councils = [
                line[2:].strip()
                for line in section_value(text, "Selected Councils").splitlines()
                if line.startswith("- ")
            ]
            records.append({
                "id": section_value(text, "Deliberation ID") or path.name.split(" ", 1)[0],
                "question": section_value(text, "Question"),
                "status": section_value(text, "Status"),
                "councils": councils,
                "recommendation": excerpt(section_value(text, "Final Recommendation"), 500),
                "confidence": section_value(text, "Confidence Score"),
                "decisions": excerpt(section_value(text, "Aaron Decisions Needed"), 500),
                "created": section_value(text, "Created"),
                "path": str(path),
            })
    return {
        "enabled": bool(load_settings().get("council_deliberation_enabled", True)),
        "records": records,
        "latest": records[0] if records else {},
        "active_councils": records[0]["councils"] if records else [],
        "overview": note_card("Deliberation Overview", "00_Raphael/Deliberations/Deliberation Overview.md"),
        "history": note_card("Deliberation History", "00_Raphael/Deliberations/Deliberation History.md"),
        "review": note_card("Deliberation Review", "00_Raphael/Deliberations/Deliberation Review.md"),
        "brief": note_card("Deliberation Brief", "00_Raphael/Deliberations/Deliberation Brief.md"),
    }


def execution_plan_data() -> dict[str, Any]:
    root = vault_path() / "00_Raphael" / "Execution Plans"
    records: list[dict[str, Any]] = []
    if root.exists():
        for path in sorted(root.glob("PLAN-*.md"), key=lambda value: value.stat().st_mtime, reverse=True):
            text = read_text(path, 60000)
            councils = []
            for line in section_value(text, "Council Responsibilities").splitlines():
                match = re.match(r"- \*\*(.+?)\*\*:", line)
                if match:
                    councils.append(match.group(1))
            records.append({
                "id": section_value(text, "PLAN ID") or path.name.split(" ", 1)[0],
                "topic": section_value(text, "Topic"),
                "status": section_value(text, "Status"),
                "objective": excerpt(section_value(text, "Objective"), 500),
                "strategy": excerpt(section_value(text, "Recommended Strategy"), 500),
                "sources": excerpt(section_value(text, "Source Records"), 500),
                "councils": councils,
                "decisions": excerpt(section_value(text, "Decisions Needed From Aaron"), 500),
                "created": section_value(text, "Created"),
                "path": str(path),
            })
    return {
        "enabled": bool(load_settings().get("execution_planning_enabled", True)),
        "records": records,
        "latest": records[0] if records else {},
        "overview": note_card("Execution Planning Overview", "00_Raphael/Execution Plans/Execution Planning Overview.md"),
        "history": note_card("Execution Plan History", "00_Raphael/Execution Plans/Execution Plan History.md"),
        "review": note_card("Execution Plan Review", "00_Raphael/Execution Plans/Execution Plan Review.md"),
        "brief": note_card("Execution Plan Brief", "00_Raphael/Execution Plans/Execution Plan Brief.md"),
    }


def n8n_workflow_studio_data() -> dict[str, Any]:
    root = vault_path() / "00_Raphael" / "n8n Workflow Studio"
    records: list[dict[str, Any]] = []
    archive_details: list[dict[str, Any]] = []
    for folder, origin in [("Workflow Plans", "Plan"), ("Workflow Drafts", "Generated"), ("Workflow Summaries", "Archive")]:
        current = root / folder
        if not current.exists():
            continue
        files = sorted(current.glob("*.md"), key=lambda value: value.stat().st_mtime, reverse=True)[:10]
        for path in files:
            text = read_text(path, 5000)
            node_section = section_value(text, "Nodes") or section_value(text, "Node Analysis")
            node_match = re.search(r"Nodes:\s*(\d+)", node_section)
            node_types = [
                line.strip()[2:].strip().strip("`")
                for line in node_section.splitlines()
                if line.strip().startswith("- `")
            ]
            services = [
                line[2:].strip()
                for line in section_value(text, "API and Service Analysis").splitlines()
                if line.startswith("- ")
            ]
            credentials = [
                re.sub(r"\s+\(type only; no credential value stored\)$", "", line[2:].strip())
                for line in section_value(text, "Required Credentials").splitlines()
                if line.startswith("- ") and "None declared" not in line
            ]
            triggers = [item for item in node_types if any(term in item.lower() for term in ["trigger", "webhook"])]
            external_services = [
                item for item in services
                if item.lower() not in {"code", "if", "set", "wait", "sticky note", "split in batches", "remove duplicates", "manual trigger", "schedule trigger"}
            ]
            risk_corpus = " ".join(node_types + credentials + services).lower()
            risk = "high" if credentials and any(term in risk_corpus for term in ["youtube", "openai", "google", "http", "api", "oauth"]) else ("medium" if credentials or "http" in risk_corpus else "low")
            reuse = [
                line[2:].strip()
                for line in section_value(text, "Reuse Assessment").splitlines()
                if line.startswith("- ")
            ]
            name = section_value(text, "Name") or path.stem
            category = section_value(text, "Category") or "Automation"
            records.append({
                "id": section_value(text, "Workflow ID") or path.name.split(" ", 1)[0],
                "name": name,
                "category": category,
                "status": section_value(text, "Status") or "Unknown",
                "origin": origin,
                "nodes": int(node_match.group(1)) if node_match else node_section.count("\n|"),
                "credentials": excerpt(section_value(text, "Required Credentials"), 350),
                "source": section_value(text, "Source"),
                "source_workflow": section_value(text, "Source Workflow"),
                "services": services[:12],
                "path": str(path),
            })
            if origin == "Archive":
                archive_details.append({
                    "workflow_id": section_value(text, "Workflow ID") or path.name.split(" ", 1)[0],
                    "workflow_name": name,
                    "category": category,
                    "description": section_value(text, "Purpose") or "Reusable automation candidate inferred from archive metadata.",
                    "node_count": int(node_match.group(1)) if node_match else len(node_types),
                    "node_types": node_types,
                    "triggers": triggers,
                    "external_services": external_services,
                    "credentials_required": credentials,
                    "risk_level": risk,
                    "reusable_patterns": reuse,
                    "potential_raphael_uses": (
                        ["Draft and QA local YouTube/content automation blueprints without publishing."] if "youtube" in risk_corpus
                        else ["Use as a read-only reference for safe inactive n8n workflow architecture."]
                    ),
                    "path": str(path),
                })
    records.sort(key=lambda item: Path(item["path"]).stat().st_mtime, reverse=True)
    archive_details.sort(key=lambda item: Path(item["path"]).stat().st_mtime, reverse=True)
    categories: dict[str, int] = {}
    for record in records:
        categories[record["category"]] = categories.get(record["category"], 0) + 1
    return {
        "enabled": bool(load_settings().get("n8n_workflow_studio_enabled", True)),
        "records": records,
        "categories": categories,
        "archive_records": [record for record in records if record["origin"] == "Archive"],
        "archive_details": archive_details,
        "overview": note_card("Workflow Studio Overview", "00_Raphael/n8n Workflow Studio/Workflow Studio Overview.md"),
        "registry": note_card("Workflow Registry", "00_Raphael/n8n Workflow Studio/Workflow Registry.md"),
        "templates": note_card("Workflow Templates", "00_Raphael/n8n Workflow Studio/Workflow Templates.md"),
        "reviews": note_card("Workflow Reviews", "00_Raphael/n8n Workflow Studio/Workflow Reviews.md"),
        "brief": note_card("Workflow Brief", "00_Raphael/n8n Workflow Studio/Workflow Brief.md"),
        "history": note_card("Workflow Export History", "00_Raphael/n8n Workflow Studio/Workflow Export History.md"),
        "knowledge": note_card("Workflow Knowledge", "00_Raphael/n8n Workflow Studio/Workflow Knowledge.md"),
        "safety": {
            "execution": False,
            "activation": False,
            "credential_storage": False,
            "external_calls": False,
            "source_edits": False,
        },
    }


def workflow_runner_data() -> dict[str, Any]:
    root = runtime_path() / "workflow_runner"
    registry_path = root / "workflow_registry.json"
    registry = json.loads(read_text(registry_path) or '{"workflows": []}')
    executions: list[dict[str, Any]] = []
    execution_root = root / "executions"
    if execution_root.exists():
        for path in sorted(execution_root.glob("WFEXEC-*.json"), key=lambda value: value.stat().st_mtime, reverse=True):
            try:
                executions.append(json.loads(read_text(path)))
            except json.JSONDecodeError:
                continue
    n8n_ok, n8n_detail = http_json("http://127.0.0.1:5678/healthz")
    return {
        "enabled": True,
        "registry_path": str(registry_path),
        "runtime_path": str(root),
        "workflows": registry.get("workflows", []),
        "executions": executions,
        "active": [row for row in executions if row.get("status") == "running"],
        "queued": [row for row in executions if row.get("status") == "queued"],
        "completed": [row for row in executions if row.get("status") == "completed"],
        "failed": [row for row in executions if row.get("status") == "failed"],
        "cancelled": [row for row in executions if row.get("status") == "cancelled"],
        "n8n": {"healthy": n8n_ok, "url": "http://127.0.0.1:5678", "detail": n8n_detail},
        "overview": note_card("Workflow Runner Overview", "00_Raphael/Workflow Runner/Workflow Runner Overview.md"),
        "registry_note": note_card("Workflow Registry", "00_Raphael/Workflow Runner/Workflow Registry.md"),
        "execution_note": note_card("Workflow Executions", "00_Raphael/Workflow Runner/Workflow Executions.md"),
        "results_note": note_card("Workflow Results", "00_Raphael/Workflow Runner/Workflow Results.md"),
        "failures_note": note_card("Workflow Failures", "00_Raphael/Workflow Runner/Workflow Failures.md"),
        "review_note": note_card("Workflow Review", "00_Raphael/Workflow Runner/Workflow Review.md"),
    }


def tasks() -> list[dict[str, str]]:
    root = vault_path() / "03_Agents"
    items: list[dict[str, str]] = []
    if not root.exists():
        return items
    for path in sorted(root.glob("*/Tasks/*.md")):
        text = read_text(path)
        items.append(
            {
                "id": section_value(text, "Task ID") or path.stem,
                "task": section_value(text, "Task") or path.stem,
                "agent": section_value(text, "Assigned Agent") or path.parents[1].name,
                "status": section_value(text, "Status") or "Unknown",
                "priority": section_value(text, "Priority") or "Medium",
                "project": section_value(text, "Related Project") or "Unassigned",
                "path": str(path),
            }
        )
    return items


def agents() -> list[dict[str, Any]]:
    root = vault_path() / "03_Agents"
    task_items = tasks()
    items: list[dict[str, Any]] = []
    if not root.exists():
        return items
    for folder in sorted(path for path in root.iterdir() if path.is_dir()):
        agent_tasks = [item for item in task_items if item["agent"] == folder.name]
        open_count = sum(1 for item in agent_tasks if item["status"] not in {"Done", "Archived"})
        items.append(
            {
                "name": folder.name,
                "open_tasks": open_count,
                "total_tasks": len(agent_tasks),
                "has_brief": (folder / "Agent Brief.md").exists(),
                "has_ai_brief": (folder / "AI Agent Brief.md").exists(),
            }
        )
    return items


COUNCILS = {
    "Executive Council": {
        "purpose": "High-level direction, priorities, risk, resource allocation, and final recommendations.",
        "members": ["Chief of Staff Agent", "CTO Agent", "Engineering Manager Agent", "Project Manager Agent"],
    },
    "Product Council": {
        "purpose": "Product vision, market fit, requirements, MVP scope, user needs, and success metrics.",
        "members": ["Product Manager Agent", "Business Analyst Agent", "UI UX Designer Agent", "Project Manager Agent"],
    },
    "Engineering Council": {
        "purpose": "Technical architecture, implementation planning, testing, deployment, and AI integration.",
        "members": ["Software Architect Agent", "Tech Lead Agent", "Front-End Developer Agent", "Back-End Developer Agent", "Full-Stack Developer Agent", "QA Engineer Agent", "DevOps Cloud Engineer Agent", "Machine Learning AI Engineer Agent"],
    },
    "Operations Council": {
        "purpose": "Timeline, sprint planning, blockers, coordination, milestones, and delivery.",
        "members": ["Project Manager Agent", "Scrum Master Agent", "Engineering Manager Agent", "Operations Agent"],
    },
    "Research Council": {
        "purpose": "Market research, technical research, competitor analysis, academic research, and source gathering.",
        "members": ["Research Agent", "Market Analyst Agent", "AI Researcher Agent", "Technical Research Agent"],
    },
    "Career Council": {
        "purpose": "Resume, portfolio, interview prep, job readiness, and career strategy.",
        "members": ["Career Agent", "Resume Agent", "Portfolio Agent", "Interview Prep Agent", "Job Search Agent"],
    },
    "Business Council": {
        "purpose": "Business ideas, revenue models, client strategy, pricing, offers, and operations.",
        "members": ["Business Strategy Agent", "Marketing Agent", "Finance Agent", "Legal Compliance Agent", "Sales Agent"],
    },
    "Commerce Council": {
        "purpose": "Product-based business planning for Etsy, Shopify, KDP, digital products, and print-on-demand.",
        "members": ["Store Manager Agent", "Product Researcher Agent", "Trend Analyst Agent", "Listing Writer Agent", "SEO Specialist Agent", "Customer Support Agent", "Digital Product Agent", "POD Designer Agent"],
    },
    "Agency Council": {
        "purpose": "Client-service offer design, proposal planning, delivery planning, and agency operations.",
        "members": ["Sales Agent", "Proposal Writer Agent", "Account Manager Agent", "Delivery Manager Agent", "Marketing Agent", "Client Success Agent"],
    },
    "Creator Council": {
        "purpose": "Content strategy, AI influencer brands, ebooks, newsletters, audience growth, and content funnels.",
        "members": ["Content Strategist Agent", "Script Writer Agent", "Influencer Manager Agent", "Social Media Manager Agent", "Newsletter Agent", "Ebook Writer Agent", "Audience Growth Agent"],
    },
    "Financial Council": {
        "purpose": "Financial tracking, budget awareness, revenue visibility, profit review, and financial risk monitoring.",
        "members": ["Finance Agent", "Business Strategy Agent", "Operations Agent"],
    },
    "Portfolio Council": {
        "purpose": "Multi-business portfolio prioritization, strategic focus, roadmap balance, and opportunity comparison.",
        "members": ["Chief of Staff Agent", "Business Strategy Agent", "Career Agent", "Finance Agent"],
    },
    "Governance Council": {
        "purpose": "Safety boundaries, approvals, policy, identity rules, controlled execution, and escalation oversight.",
        "members": ["Chief of Staff Agent", "Legal Compliance Agent", "Operations Agent"],
    },
}


def council_task_entries() -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    root = vault_path() / "03_Agents" / "Councils"
    if not root.exists():
        return items
    for council in COUNCILS:
        text = read_text(root / council / "Council Tasks.md")
        for match in re.finditer(r"^## (COUNCIL-[A-Z0-9]+)\s+(.+?)(?=^## COUNCIL-|\Z)", text, flags=re.M | re.S):
            body = match.group(2)
            items.append({
                "id": match.group(1),
                "council": council,
                "task": subsection_value(body, "Task"),
                "agent": subsection_value(body, "Assigned Agent"),
                "status": subsection_value(body, "Status") or "Open",
                "priority": subsection_value(body, "Priority") or "Normal",
            })
    return items


def council_debates() -> list[dict[str, str]]:
    root = vault_path() / "03_Agents" / "Councils"
    if not root.exists():
        return []
    items = []
    for path in sorted(root.glob("*/Debates/*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
        items.append({"council": path.parent.parent.name, "name": path.stem, "path": str(path), "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")})
    return items[:20]


def councils() -> list[dict[str, Any]]:
    root = vault_path() / "03_Agents" / "Councils"
    task_items = council_task_entries()
    debate_items = council_debates()
    rows = []
    for name, meta in COUNCILS.items():
        folder = root / name
        rows.append({
            "name": name,
            "purpose": meta["purpose"],
            "members": meta["members"],
            "tasks": [item for item in task_items if item["council"] == name],
            "recent_debates": [item for item in debate_items if item["council"] == name],
            "has_brief": (folder / "Council Brief.md").exists(),
            "has_review": (folder / "Council Review.md").exists(),
        })
    return rows


def registered_council_names() -> list[str]:
    names = set(COUNCILS)
    root = vault_path() / "03_Agents" / "Councils"
    if root.exists():
        names.update(path.name for path in root.iterdir() if path.is_dir() and path.name != "Debates")
    return sorted(names)


def council_status_data() -> dict[str, dict[str, Any]]:
    task_items = council_task_entries()
    activity_rows = activity_records()
    notification_rows = notification_records()
    agent_rows = {item["name"]: item for item in agents()}
    empty = {"", "Unassigned", "Unlinked", "Unknown", "None"}
    status: dict[str, dict[str, Any]] = {}
    for name in registered_council_names():
        meta = COUNCILS.get(name, {"purpose": "Registered council.", "members": []})
        council_tasks = [item for item in task_items if item.get("council") == name]
        open_tasks = sum(1 for item in council_tasks if item.get("status") not in {"Done", "Archived", "Completed"})
        blocked_tasks = sum(1 for item in council_tasks if item.get("status") == "Blocked")
        council_activity = [row for row in activity_rows if row.get("Related Council") == name]
        council_notifications = [
            row for row in notification_rows
            if row.get("Related Council") == name and row.get("Status") != "Dismissed"
        ]
        critical_notifications = sum(1 for row in council_notifications if row.get("Severity") in {"Critical", "High"})
        member_count = len(meta.get("members", []))
        member_open_tasks = sum(agent_rows.get(member, {}).get("open_tasks", 0) for member in meta.get("members", []))
        activity_score = len(council_activity) + open_tasks + member_open_tasks
        health = max(20, min(100, 96 - critical_notifications * 12 - blocked_tasks * 10 - max(0, open_tasks - 4) * 3))
        if critical_notifications or health < 55:
            state = "critical"
        elif activity_score >= 12 or open_tasks >= 5:
            state = "busy"
        elif activity_score > 0 or council_notifications:
            state = "active"
        else:
            state = "dormant"
        status[name] = {
            "name": name,
            "purpose": meta.get("purpose", "Registered council."),
            "members": meta.get("members", []),
            "health": health,
            "state": state,
            "activity": len(council_activity),
            "notifications": len(council_notifications),
            "critical_notifications": critical_notifications,
            "employees": member_count,
            "open_tasks": open_tasks,
            "blocked_tasks": blocked_tasks,
            "member_open_tasks": member_open_tasks,
            "recent_delegations": [
                row.get("Title", row.get("Event ID", "Delegation"))
                for row in council_activity
                if "delegat" in (row.get("Title", "") + " " + row.get("Details", "")).lower()
            ][:3],
        }
    return status


def council_activity_data() -> dict[str, Any]:
    activity_rows = activity_records()
    task_items = council_task_entries()
    status = council_status_data()
    recent_events = [
        row for row in activity_rows
        if row.get("Related Council") not in {"", "Unassigned", "Unlinked", "Unknown", "None"}
    ][:25]
    delegations = [
        row for row in recent_events
        if "delegat" in (row.get("Title", "") + " " + row.get("Details", "")).lower()
    ][:10]
    workload = {
        name: {
            "open_tasks": item.get("open_tasks", 0),
            "blocked_tasks": item.get("blocked_tasks", 0),
            "state": item.get("state", "dormant"),
            "health": item.get("health", 100),
        }
        for name, item in status.items()
    }
    return {
        "recent_events": recent_events,
        "delegations": delegations,
        "workload": workload,
        "open_council_tasks": [item for item in task_items if item.get("status") not in {"Done", "Archived", "Completed"}],
    }


MATRIX_DEPARTMENTS: dict[str, list[dict[str, Any]]] = {
    "Cognitive Intelligence": [
        {"id": "world", "name": "World Model", "route": "world", "owner_council": "Research Council", "related": ["vision", "memory"]},
        {"id": "vision", "name": "Vision Kernel", "route": "vision", "owner_council": "Research Council", "related": ["world", "search"]},
        {"id": "memory", "name": "Memory & Reality", "route": "memory", "owner_council": "Research Council", "related": ["world", "selfimprovement"]},
        {"id": "selfimprovement", "name": "Self Improvement", "route": "activity", "owner_council": "Governance Council", "related": ["memory", "simulations"]},
        {"id": "models", "name": "Model Router", "route": "models", "owner_council": "Research Council", "related": ["execution", "selfimprovement"]},
        {"id": "search", "name": "Search & Perception", "route": "search", "owner_council": "Research Council", "related": ["vision", "world"]},
    ],
    "Executive & Strategy": [
        {"id": "identity", "name": "CEOs", "route": "identity", "owner_council": "Executive Council", "related": ["briefs", "opportunities"]},
        {"id": "briefs", "name": "Executive Briefs", "route": "briefs", "owner_council": "Executive Council", "related": ["goals", "initiatives"]},
        {"id": "goals", "name": "Goals", "route": "goals", "owner_council": "Executive Council", "related": ["briefs", "goalpropagation"]},
        {"id": "initiatives", "name": "Strategic Initiatives", "route": "initiatives", "owner_council": "Executive Council", "related": ["portfolio", "briefs"]},
        {"id": "deliberations", "name": "Deliberations", "route": "deliberations", "owner_council": "Executive Council", "related": ["goals", "commandbus"]},
        {"id": "commandbus", "name": "Governance Bus", "route": "commandbus", "owner_council": "Governance Council", "related": ["identity", "execution"]},
    ],
    "Discovery & Simulation": [
        {"id": "opportunities", "name": "Opportunity Engine", "route": "opportunities", "owner_council": "Portfolio Council", "related": ["simulations", "allocation"]},
        {"id": "simulations", "name": "Reality Simulation", "route": "simulations", "owner_council": "Portfolio Council", "related": ["opportunities", "blueprints"]},
        {"id": "feedback", "name": "Reality Feedback", "route": "kpis", "owner_council": "Portfolio Council", "related": ["simulations", "selfimprovement"]},
        {"id": "blueprints", "name": "Business Factory", "route": "blueprints", "owner_council": "Portfolio Council", "related": ["simulations", "portfolio"]},
        {"id": "portfolio", "name": "Business Portfolio", "route": "portfolio", "owner_council": "Portfolio Council", "related": ["blueprints", "allocation"]},
        {"id": "allocation", "name": "Capital Allocation", "route": "allocation", "owner_council": "Financial Council", "related": ["opportunities", "portfolio"]},
    ],
    "Digital Workforce": [
        {"id": "employees", "name": "Workforce Profiles", "route": "employees", "owner_council": "Operations Council", "related": ["agency", "commerce"]},
        {"id": "agency", "name": "Service Agency", "route": "agency", "owner_council": "Agency Council", "related": ["employees", "portfolio"]},
        {"id": "commerce", "name": "Commerce Group", "route": "commerce", "owner_council": "Commerce Council", "related": ["employees", "assetlibrary"]},
        {"id": "creator", "name": "Creator Studio", "route": "creator", "owner_council": "Creator Council", "related": ["employees", "assetlibrary"]},
        {"id": "assetlibrary", "name": "Asset Library", "route": "assetlibrary", "owner_council": "Creator Council", "related": ["creator", "commerce"]},
        {"id": "builder", "name": "Code Builder", "route": "builder", "owner_council": "Operations Council", "related": ["employees", "execution"]},
    ],
    "Execution Kernel": [
        {"id": "goalpropagation", "name": "Goal Propagation", "route": "goalpropagation", "owner_council": "Executive Council", "related": ["goals", "executionplans"]},
        {"id": "executionplans", "name": "Execution Plans", "route": "executionplans", "owner_council": "Operations Council", "related": ["goalpropagation", "workflows"]},
        {"id": "workflows", "name": "Native Workflows", "route": "workflows", "owner_council": "Operations Council", "related": ["executionplans", "execution"]},
        {"id": "execution", "name": "Execution Layer", "route": "execution", "owner_council": "Governance Council", "related": ["workflows", "n8nstudio"]},
        {"id": "n8nstudio", "name": "n8n Automation", "route": "n8nstudio", "owner_council": "Operations Council", "related": ["execution", "workflows"]},
        {"id": "activity", "name": "Activity Stream", "route": "activity", "owner_council": "Executive Council", "related": ["execution", "employees"]},
    ],
}


def matrix_department_data() -> dict[str, Any]:
    activity_rows = activity_records()
    notification_rows = notification_records()
    employees = employee_records()
    task_rows = tasks()
    kpis = kpi_records()
    build_rows = build_requests()
    council_members = {name: set(meta.get("members", [])) for name, meta in COUNCILS.items()}
    result: dict[str, Any] = {"sectors": {}}
    for sector_name, definitions in MATRIX_DEPARTMENTS.items():
        departments = []
        for definition in definitions:
            owner = definition["owner_council"]
            keywords = {
                definition["id"].lower(),
                definition["name"].lower(),
                definition["route"].lower(),
                sector_name.lower(),
            }
            department_activity = [
                row for row in activity_rows
                if any(keyword in " ".join(str(value).lower() for value in row.values()) for keyword in keywords)
            ]
            department_notifications = [
                row for row in notification_rows
                if row.get("Status") != "Dismissed"
                and any(keyword in " ".join(str(value).lower() for value in row.values()) for keyword in keywords)
            ]
            critical = sum(1 for row in department_notifications if row.get("Severity") in {"Critical", "High"})
            related_employees = [
                row for row in employees
                if owner.lower() in (row.get("department") or "").lower()
                or row.get("name") in council_members.get(owner, set())
            ]
            employee_names = {row.get("name") for row in related_employees}
            open_tasks = sum(
                1 for row in task_rows
                if row.get("status") not in {"Done", "Archived", "Completed"}
                and (row.get("agent") in employee_names or any(keyword in (row.get("task") or "").lower() for keyword in keywords))
            )
            related_kpis = [
                row for row in kpis
                if owner.lower() in (row.get("owner") or "").lower()
                or any(keyword in ((row.get("name") or "") + " " + (row.get("category") or "")).lower() for keyword in keywords)
            ]
            at_risk_kpis = sum(1 for row in related_kpis if row.get("status") in {"At Risk", "Behind"})
            activity_count = len(department_activity)
            notification_count = len(department_notifications)
            health = max(20, min(100, 96 - critical * 14 - max(0, notification_count - critical) * 5 - at_risk_kpis * 8 - max(0, open_tasks - 6) * 2))
            if critical or health < 55:
                state = "critical"
            elif notification_count or at_risk_kpis or health < 78:
                state = "warning"
            elif activity_count >= 8 or open_tasks >= 5:
                state = "busy"
            elif activity_count or open_tasks or related_employees:
                state = "active"
            else:
                state = "idle"
            governance: dict[str, Any] = {}
            if definition["id"] == "builder":
                governance = {
                    "active_builds": len(build_rows),
                    "high_awaiting_review": sum(1 for row in build_rows if row.get("complexity", "").startswith("3") and row.get("status") == "Awaiting Plan Approval"),
                    "ready_for_review": sum(1 for row in build_rows if row.get("task_status") == "Ready for Review"),
                    "task_linked_builds": sum(1 for row in build_rows if row.get("task_id")),
                }
            elif sector_name == "Execution Layer" and definition["id"] in {"tasks", "executionplans"}:
                governance = {
                    "build_tasks": sum(1 for row in build_rows if row.get("task_id")),
                    "builds_with_execution_plans": sum(1 for row in build_rows if row.get("execution_plan_id")),
                    "builds_ready_for_review": sum(1 for row in build_rows if row.get("task_status") == "Ready for Review"),
                }
            departments.append({
                **definition,
                "sector": sector_name,
                "health": health,
                "state": state,
                "notifications": notification_count,
                "critical_notifications": critical,
                "activity": activity_count,
                "employees": len(related_employees),
                "open_tasks": open_tasks,
                "kpis": len(related_kpis),
                "at_risk_kpis": at_risk_kpis,
                "builder_governance": governance,
            })
        result["sectors"][sector_name] = {"departments": departments}
    return result


def council_recent_decisions(council: str) -> list[dict[str, str]]:
    path = vault_path() / "03_Agents" / "Councils" / council / "Council Decisions.md"
    text = read_text(path, 30000)
    rows: list[dict[str, str]] = []
    for match in re.finditer(r"^##+\s+(.+?)\n(.*?)(?=^##+\s+|\Z)", text, flags=re.M | re.S):
        title = match.group(1).strip()
        if title.lower() in {"council decisions", "decisions"}:
            continue
        rows.append({"title": title, "summary": excerpt(match.group(2).strip(), 240)})
    return rows[-5:][::-1]


def council_chamber_data() -> dict[str, Any]:
    statuses = council_status_data()
    department_data = matrix_department_data().get("sectors", {})
    employee_rows = employee_records()
    agent_rows = {item["name"]: item for item in agents()}
    task_rows = council_task_entries()
    kpi_rows = kpi_records()
    initiative_rows = initiative_records()
    opportunity_rows = opportunity_records()
    activity_rows = activity_records()
    communications = communication_data()
    deliberations = deliberation_data()
    build_rows = build_requests()
    chambers: dict[str, Any] = {}
    for council in registered_council_names():
        meta = COUNCILS.get(council, {"purpose": "Registered council.", "members": []})
        status = statuses.get(council, {})
        related_departments: list[dict[str, Any]] = []
        owner_sector = "Raphael Core"
        for sector, sector_data in department_data.items():
            owned = [
                {
                    "id": item["id"],
                    "name": item["name"],
                    "route": item["route"],
                    "sector": sector,
                    "health": item["health"],
                    "state": item["state"],
                }
                for item in sector_data.get("departments", [])
                if item.get("owner_council") == council
            ]
            if owned:
                if owner_sector == "Raphael Core":
                    owner_sector = sector
                related_departments.extend(owned)
        members = []
        for member in meta.get("members", []):
            employee = next((item for item in employee_rows if item.get("name") == member), {})
            agent = agent_rows.get(member, {})
            members.append({
                "employee_id": employee.get("id", ""),
                "name": member,
                "role": employee.get("role") or member.replace(" Agent", ""),
                "workload": employee.get("workload") or ("Active" if agent.get("open_tasks") else "Low"),
                "performance": employee.get("performance") or "Unknown",
                "open_tasks": agent.get("open_tasks", 0),
                "assigned_kpis": employee.get("kpis", ""),
            })
        council_tasks = [item for item in task_rows if item.get("council") == council]
        assigned_kpis = [item for item in kpi_rows if item.get("owner") == council]
        initiatives = [item for item in initiative_rows if item.get("council") == council]
        opportunities = [item for item in opportunity_rows if item.get("council") == council]
        recent_activity = [item for item in activity_rows if item.get("Related Council") == council][:8]
        incoming_requests = [item for item in communications["requests"] if item.get("to_council") == council]
        outgoing_requests = [item for item in communications["requests"] if item.get("from_council") == council]
        council_recommendations = [
            item for item in communications["recommendations"]
            if council in item.get("council_opinions", "")
        ]
        council_deliberations = [item for item in deliberations["records"] if council in item.get("councils", [])]
        council_builds = [
            item for item in build_rows
            if council in [value.strip() for value in item.get("councils", "").split(",")]
        ]
        recommendations: list[str] = []
        if status.get("critical_notifications", 0):
            recommendations.append("Review critical and high council notifications before accepting new work.")
        if status.get("blocked_tasks", 0):
            recommendations.append("Resolve blocked council tasks and identify items requiring Aaron's decision.")
        if council_tasks and not assigned_kpis:
            recommendations.append("Assign measurable KPIs to the council's active work.")
        if opportunities and not council_tasks:
            recommendations.append("Review the highest-value opportunity and prepare a confirmation-gated delegation.")
        if not recommendations:
            recommendations.append("Maintain current priorities and review the next highest-impact council task.")
        chambers[council] = {
            "council_name": council,
            "purpose": meta.get("purpose", "Registered council."),
            "health": status.get("health", 100),
            "state": status.get("state", "dormant"),
            "activity": status.get("activity", 0),
            "notifications": status.get("notifications", 0),
            "owner_sector": owner_sector,
            "members": members,
            "open_tasks": council_tasks,
            "assigned_kpis": assigned_kpis,
            "initiatives": initiatives[:8],
            "opportunities": opportunities[:8],
            "recent_decisions": council_recent_decisions(council),
            "recent_activity": recent_activity,
            "communications": {
                "incoming_requests": incoming_requests[:8],
                "outgoing_requests": outgoing_requests[:8],
                "recommendations": council_recommendations[:8],
                "recent_syntheses": communications["syntheses"][-5:][::-1],
            },
            "deliberations": council_deliberations[:8],
            "build_requests": council_builds[:8],
            "recommendations": recommendations,
            "related_departments": related_departments,
            "quick_actions": [
                {"label": "Brief Council", "prompt": f"brief the {council}"},
                {"label": "Review Council", "prompt": f"review the {council}"},
                {"label": "Council Status", "prompt": "council status"},
                {"label": "Council Task Review", "prompt": "council task review"},
                {"label": "Latest Deliberation", "prompt": "show latest deliberation"},
            ],
        }
    return {"chambers": chambers}


def request_notes(folder: Path, id_heading: str, extra_headings: list[str]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    if not folder.exists():
        return items
    for path in sorted(folder.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 3000)
        item = {
            "id": section_value(text, id_heading) or path.stem,
            "status": section_value(text, "Status") or "Unknown",
            "created": section_value(text, "Created Date"),
            "path": str(path),
        }
        for heading in extra_headings:
            item[heading.lower().replace(" ", "_")] = section_value(text, heading)
        items.append(item)
    return items


def workflow_requests() -> list[dict[str, str]]:
    return request_notes(vault_path() / "00_Raphael" / "Workflow Requests", "Workflow Request ID", ["Workflow Name", "Project", "Risk Level"])


def search_requests() -> list[dict[str, str]]:
    return request_notes(vault_path() / "04_Research" / "Web Search Results" / "Search Requests", "Search Request ID", ["Question"])


def internet_access_data() -> dict[str, Any]:
    root = vault_path() / "00_Raphael" / "Internet Access"
    state_path = runtime_path() / "internet" / "internet_state.json"
    try:
        state = json.loads(read_text(state_path, 2_000_000) or '{"requests":[],"results":[],"sources":[]}')
    except json.JSONDecodeError:
        state = {"requests": [], "results": [], "sources": []}
    requests = state.get("requests", [])
    results = state.get("results", [])
    latest_result = sorted(results, key=lambda row: str(row.get("recorded", "")), reverse=True)[0] if results else {}
    latest_overview = latest_result.get("ai_overview") or {}
    settings = load_settings()
    searxng_url = str(settings.get("searxng_url", "http://127.0.0.1:8080")).rstrip("/")
    searxng = {"url": searxng_url, "healthy": False, "error": ""}
    try:
        request = urllib.request.Request(
            searxng_url + "/search?q=Raphael+health+check&format=json",
            headers={"Accept": "application/json", "User-Agent": "Raphael-Dashboard/1.0"},
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
        searxng.update({"healthy": isinstance(payload.get("results", []), list), "http_status": response.status})
    except Exception as exc:
        searxng["error"] = str(exc)
    return {
        "enabled": bool(settings.get("internet_access_enabled", True)),
        "requires_confirmation": bool(settings.get("internet_requires_confirmation", True)),
        "provider": str(settings.get("internet_provider", "manual_or_browser")),
        "headless_enabled": bool(settings.get("internet_headless_search_enabled", True)),
        "ai_overview_enabled": bool(settings.get("internet_ai_overview_enabled", True)),
        "ai_overview_default": bool(settings.get("internet_ai_overview_default", True)),
        "ai_overview_source_count": int(settings.get("internet_ai_overview_source_count", 3)),
        "ai_overview_include_sources": bool(settings.get("internet_ai_overview_include_sources", True)),
        "raw_json_on_request_only": bool(settings.get("internet_raw_json_on_request_only", True)),
        "pandas_enabled": bool(settings.get("internet_analysis_with_pandas", True)),
        "searxng": searxng,
        "pending": [row for row in requests if row.get("status") != "Completed"],
        "completed": [row for row in requests if row.get("status") == "Completed"],
        "results": results,
        "latest_result": latest_result,
        "latest_overview": latest_overview,
        "sources": state.get("sources", []),
        "analyses": state.get("analyses", []),
        "niche_scores": state.get("niche_scores", []),
        "overview": note_card("Internet Access Overview", "00_Raphael/Internet Access/Internet Access Overview.md"),
        "requests_note": note_card("Search Requests", "00_Raphael/Internet Access/Search Requests.md"),
        "results_note": note_card("Search Results", "00_Raphael/Internet Access/Search Results.md"),
        "source_review": note_card("Source Review", "00_Raphael/Internet Access/Source Review.md"),
        "safety_policy": note_card("Internet Safety Policy", "00_Raphael/Internet Access/Internet Safety Policy.md"),
        "brief": note_card("Internet Brief", "00_Raphael/Internet Access/Internet Brief.md"),
        "safety": {
            "autonomous_browsing": False,
            "account_login": False,
            "external_actions": False,
            "credentials": False,
            "purchasing": False,
            "posting_uploading": False,
        },
    }


def vision_requests() -> list[dict[str, str]]:
    return request_notes(vault_path() / "04_Research" / "Vision Analysis" / "Vision Requests", "Vision Request ID", ["File Name", "File Type", "Question"])


def action_requests() -> list[dict[str, str]]:
    return request_notes(vault_path() / "00_Raphael" / "Action Requests", "Action ID", ["Description", "Risk Level", "Related Tool"])


def build_requests() -> list[dict[str, str]]:
    folder = runtime_path() / "builder" / "requests"
    items: list[dict[str, str]] = []
    if not folder.exists():
        return items
    for path in sorted(folder.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 4000)
        items.append({
            "id": section_value(text, "Build Request ID") or path.stem,
            "description": section_value(text, "Description"),
            "status": section_value(text, "Status") or "Unknown",
            "created": section_value(text, "Created Date"),
            "workspace": section_value(text, "Generated Workspace") or section_value(text, "Builder Workspace"),
            "files": section_value(text, "Generated Files"),
            "classification_id": section_value(text, "Classification ID"),
            "complexity": section_value(text, "Complexity Level"),
            "build_type": section_value(text, "Build Type"),
            "council_review": section_value(text, "Council Review"),
            "councils": section_value(text, "Required Councils"),
            "deliberation_id": section_value(text, "Related Deliberation"),
            "execution_plan_id": section_value(text, "Related Execution Plan"),
            "opportunity_id": section_value(text, "Related Opportunity"),
            "safety_status": section_value(text, "Safety Status"),
            "next_command": section_value(text, "Next Command"),
            "technical_review": section_value(text, "Technical Review"),
            "task_id": section_value(text, "Related Task ID"),
            "task_set": section_value(text, "Related Task Set"),
            "task_status": section_value(text, "Task Status"),
            "assigned_agent": section_value(text, "Assigned Agent"),
            "path": str(path),
        })
    return items


def identity_file(name: str) -> dict[str, Any]:
    path = vault_path() / "00_Raphael" / "Identity" / name
    text = read_text(path, 5000)
    return {
        "name": name,
        "exists": path.exists(),
        "path": str(path),
        "content": excerpt(text, 1800) if text else "",
        "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds") if path.exists() else "",
    }


def identity_data() -> dict[str, Any]:
    files = [
        "Raphael Identity.md",
        "Personality Profile.md",
        "Communication Style.md",
        "Decision Principles.md",
        "Escalation Rules.md",
        "Behavior Boundaries.md",
        "Response Templates.md",
        "Identity Review.md",
    ]
    settings = load_settings()
    return {
        "enabled": bool(settings.get("identity_layer_enabled", True)),
        "communication_style": str(settings.get("communication_style", "executive_direct")),
        "response_length_default": str(settings.get("response_length_default", "concise")),
        "always_disclose_uncertainty": bool(settings.get("always_disclose_uncertainty", True)),
        "prefer_actionable_recommendations": bool(settings.get("prefer_actionable_recommendations", True)),
        "escalate_when_uncertain": bool(settings.get("escalate_when_uncertain", True)),
        "files": [identity_file(name) for name in files],
    }


WORLD_FILES = {
    "business": "Businesses.md",
    "product": "Products.md",
    "revenue_stream": "Revenue Streams.md",
    "customer": "Customers.md",
    "platform": "Platforms.md",
    "asset": "Assets.md",
    "relationship": "Relationships.md",
    "business_idea": "Business Ideas.md",
}


def world_model_root() -> Path:
    return vault_path() / "00_Raphael" / "World Model"


def world_records(record_type: str) -> list[dict[str, str]]:
    path = world_model_root() / WORLD_FILES[record_type]
    text = read_text(path, 12000)
    rows: list[dict[str, str]] = []
    pattern = r"^## ([A-Z]+-\d{8}-[A-F0-9]+)\s+(.+?)(?=^## [A-Z]+-\d{8}-[A-F0-9]+|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        rows.append({
            "id": match.group(1),
            "name": subsection_value(body, "Name") or body.splitlines()[0].strip(),
            "type": subsection_value(body, "Type") or record_type.replace("_", " ").title(),
            "status": subsection_value(body, "Status") or "Unknown",
            "description": excerpt(subsection_value(body, "Description"), 220),
            "business": subsection_value(body, "Business Name"),
            "analytics_channel": subsection_value(body, "Analytics Channel"),
            "analytics_source": subsection_value(body, "Analytics Source"),
            "projects": subsection_value(body, "Related Projects") or "Unlinked",
            "goals": subsection_value(body, "Related Goals") or "Unlinked",
            "council": subsection_value(body, "Related Council"),
            "agents": subsection_value(body, "Related Agents"),
            "created": subsection_value(body, "Created Date"),
        })
    return rows


def world_model_data() -> dict[str, Any]:
    settings = load_settings()
    records = {record_type: world_records(record_type) for record_type in WORLD_FILES}
    review = note_card("World Model Review", "00_Raphael/World Model/World Model Review.md")
    brief = note_card("World Model Brief", "00_Raphael/World Model/World Model Brief.md")
    return {
        "enabled": bool(settings.get("world_model_enabled", True)),
        "requires_confirmation": bool(settings.get("world_model_requires_confirmation_for_updates", True)),
        "records": records,
        "review": review,
        "brief": brief,
    }


def simulations_root() -> Path:
    return vault_path() / "00_Raphael" / "Simulations"


def simulation_results() -> list[dict[str, str]]:
    root = simulations_root()
    if not root.exists():
        return []
    items: list[dict[str, str]] = []
    for path in sorted(root.glob("SIM-*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 20000)
        items.append({
            "id": section_value(text, "Simulation ID") or path.stem,
            "type": section_value(text, "Type"),
            "options": section_value(text, "Options"),
            "recommendation": excerpt(section_value(text, "Recommendation"), 260),
            "created": section_value(text, "Created Date"),
            "path": str(path),
        })
    return items


def simulation_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("simulation_engine_enabled", True)),
        "requires_confirmation": bool(settings.get("simulation_requires_confirmation_for_saved_results", False)),
        "criteria": note_card("Simulation Criteria", "00_Raphael/Simulations/Simulation Criteria.md"),
        "review": note_card("Simulation Review", "00_Raphael/Simulations/Simulation Review.md"),
        "results_index": note_card("Simulation Results", "00_Raphael/Simulations/Simulation Results.md"),
        "results": simulation_results(),
    }


def opportunity_records() -> list[dict[str, str]]:
    path = vault_path() / "00_Raphael" / "Opportunities" / "Opportunity Inbox.md"
    text = read_text(path, 30000)
    rows: list[dict[str, str]] = []
    pattern = r"^## (OPP-\d{8}-[A-F0-9]+)\s+(.+?)(?=^## OPP-\d{8}-[A-F0-9]+|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        rows.append({
            "id": match.group(1),
            "title": subsection_value(body, "Title"),
            "type": subsection_value(body, "Type"),
            "score": subsection_value(body, "Score") or "0",
            "risk": subsection_value(body, "Risk Level"),
            "status": subsection_value(body, "Status") or "New",
            "council": subsection_value(body, "Suggested Council"),
            "agents": subsection_value(body, "Suggested Agents"),
            "next": excerpt(subsection_value(body, "Next Recommended Action"), 180),
            "created": subsection_value(body, "Created Date"),
        })
    return rows


def opportunity_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("opportunity_engine_enabled", True)),
        "requires_confirmation": bool(settings.get("opportunity_requires_confirmation_for_delegation", True)),
        "threshold": int(settings.get("opportunity_score_threshold", 70)),
        "records": opportunity_records(),
        "scores": note_card("Opportunity Scores", "00_Raphael/Opportunities/Opportunity Scores.md"),
        "review": note_card("Opportunity Review", "00_Raphael/Opportunities/Opportunity Review.md"),
        "brief": note_card("Opportunity Brief", "00_Raphael/Opportunities/Opportunity Brief.md"),
    }


def resource_profile_data() -> dict[str, str]:
    text = read_text(vault_path() / "00_Raphael" / "Resource Allocation" / "Resource Profile.md")
    return {
        "weekly_hours": section_value(text, "Weekly Hours Available") or str(load_settings().get("default_weekly_hours_available", 15)),
        "weekly_budget": section_value(text, "Weekly Budget Available") or str(load_settings().get("default_weekly_budget_available", 0)),
        "focus_slots": section_value(text, "Focus Slots Per Week") or str(load_settings().get("default_focus_slots_per_week", 5)),
        "mode": section_value(text, "Current Operating Mode") or current_mode().get("mode", "Unknown"),
        "updated": section_value(text, "Updated Date"),
    }


def resource_allocation_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("resource_allocation_enabled", True)),
        "requires_confirmation": bool(settings.get("allocation_requires_confirmation_for_delegation", True)),
        "profile": resource_profile_data(),
        "plan": note_card("Allocation Plans", "00_Raphael/Resource Allocation/Allocation Plans.md"),
        "review": note_card("Allocation Review", "00_Raphael/Resource Allocation/Allocation Review.md"),
        "brief": note_card("Allocation Brief", "00_Raphael/Resource Allocation/Allocation Brief.md"),
        "rules": note_card("Allocation Rules", "00_Raphael/Resource Allocation/Allocation Rules.md"),
    }


def blueprint_records() -> list[dict[str, str]]:
    root = vault_path() / "00_Raphael" / "Business Blueprints"
    rows: list[dict[str, str]] = []
    if not root.exists():
        return rows
    for path in sorted(root.glob("BLUEPRINT-*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 12000)
        rows.append({
            "id": section_value(text, "Blueprint ID") or path.stem.split(" ")[0],
            "name": section_value(text, "Business Name"),
            "type": section_value(text, "Business Type"),
            "concept": excerpt(section_value(text, "One-Sentence Concept"), 220),
            "council": section_value(text, "Suggested Council Ownership") or section_value(text, "Suggested Council"),
            "next": excerpt(section_value(text, "Suggested Next Action"), 220),
            "path": str(path),
        })
    return rows


def blueprint_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("business_blueprint_enabled", True)),
        "requires_confirmation": bool(settings.get("business_blueprint_requires_confirmation_for_delegation", True)),
        "depth": str(settings.get("business_blueprint_default_depth", "standard")),
        "records": blueprint_records(),
        "index": note_card("Business Blueprint Index", "00_Raphael/Business Blueprints/Business Blueprint Index.md"),
        "review": note_card("Business Blueprint Review", "00_Raphael/Business Blueprints/Business Blueprint Review.md"),
        "template": note_card("Business Blueprint Template", "00_Raphael/Business Blueprints/Business Blueprint Template.md"),
    }


def commerce_note_records(subfolder: str) -> list[dict[str, str]]:
    root = vault_path() / "05_Business" / "Commerce" / subfolder
    rows: list[dict[str, str]] = []
    if not root.exists():
        return rows
    for path in sorted(root.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 10000)
        rows.append({
            "name": path.stem,
            "idea": section_value(text, "Product Idea") or section_value(text, "Product Concept") or section_value(text, "Store Concept") or path.stem,
            "target": excerpt(section_value(text, "Target Customer") or section_value(text, "Buyer Problem") or section_value(text, "Niche"), 160),
            "next": excerpt(section_value(text, "Next Actions") or section_value(text, "Launch Checklist"), 180),
            "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            "path": str(path),
        })
    return rows


def commerce_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("commerce_council_enabled", True)),
        "requires_confirmation": bool(settings.get("commerce_requires_confirmation_for_delegation", True)),
        "no_platform_actions": bool(settings.get("commerce_no_platform_actions", True)),
        "platforms": list(settings.get("commerce_default_platforms", ["Etsy", "Shopify", "Amazon KDP", "Gumroad", "Payhip"])),
        "overview": note_card("Commerce Council Overview", "05_Business/Commerce/Commerce Council Overview.md"),
        "strategy": note_card("Commerce Strategy", "05_Business/Commerce/Commerce Strategy.md"),
        "brief": note_card("Commerce Brief", "05_Business/Commerce/Commerce Brief.md"),
        "pipeline": note_card("Commerce Product Pipeline", "05_Business/Commerce/Commerce Product Pipeline.md"),
        "review": note_card("Commerce Opportunity Review", "05_Business/Commerce/Commerce Opportunity Review.md"),
        "task_board": note_card("Commerce Task Board", "05_Business/Commerce/Commerce Task Board.md"),
        "kpis": note_card("Commerce KPI Draft", "05_Business/Commerce/Commerce KPI Draft.md"),
        "pod_ideas": commerce_note_records("POD Ideas"),
        "listing_plans": commerce_note_records("Listing Plans"),
        "store_plans": commerce_note_records("Store Plans"),
        "digital_products": commerce_note_records("Digital Products"),
    }


def pod_studio_records(folder: str, id_heading: str) -> list[dict[str, Any]]:
    root = vault_path() / "05_Business" / "Commerce" / "POD Design Studio" / folder
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return rows
    for path in sorted(root.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 100000)
        output_folder = section_value(text, "Output Folder")
        output_paths = [
            line[2:].strip()
            for line in section_value(text, "PODStudio Output Files").splitlines()
            if line.startswith("- ") and line[2:].strip().lower() != "none"
        ]
        rows.append({
            "id": section_value(text, id_heading) or path.name.split(" ", 1)[0],
            "name": section_value(text, "Product Idea") or section_value(text, "Phrase") or section_value(text, "Name") or path.stem,
            "concept": section_value(text, "Concept ID"),
            "status": section_value(text, "Status") or "Generated note",
            "model": section_value(text, "Model"),
            "score": section_value(text, "Overall Score"),
            "prompt_id": section_value(text, "ComfyUI Prompt ID"),
            "output_folder": output_folder,
            "output_paths": output_paths,
            "image_count": len([path for path in output_paths if Path(path).exists()]),
            "error": section_value(text, "Generation Error"),
            "debug_command": f"python raphael.py pod-generation-debug \"{section_value(text, id_heading) or path.name.split(' ', 1)[0]}\"",
            "submitted_payload": str(runtime_path() / "PODStudio" / "logs" / f"{section_value(text, id_heading) or path.name.split(' ', 1)[0]}-submitted-payload.json"),
            "comfyui_error_file": str(runtime_path() / "PODStudio" / "logs" / f"{section_value(text, id_heading) or path.name.split(' ', 1)[0]}-comfyui-error.json"),
            "path": str(path),
            "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        })
    return rows


def pod_design_studio_data() -> dict[str, Any]:
    settings = load_settings()
    runtime = Path(str(settings.get("runtime_path", "R:/RaphaelOS"))) / "PODStudio"
    generated = []
    generated_root = runtime / "generated"
    if generated_root.exists():
        for path in sorted(generated_root.rglob("*"), key=lambda item: item.stat().st_mtime if item.exists() else 0, reverse=True):
            if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                generated.append({"name": path.name, "path": str(path), "size": path.stat().st_size})
                if len(generated) >= 30:
                    break
    typography_root = vault_path() / "05_Business" / "Commerce" / "POD Design Studio" / "Typography Engine"
    typography_runtime = runtime / "working" / "typography"
    typography = {
        "enabled": bool(settings.get("pod_typography_enabled", True)),
        "inkscape_enabled": bool(settings.get("pod_inkscape_enabled", True)),
        "inkscape_path": str(settings.get("pod_inkscape_path", "")),
        "assets": pod_studio_records("Typography Engine/Assets", "Typography ID"),
        "compositions": pod_studio_records("Typography Engine/Compositions", "Composition ID"),
        "svg_exports": pod_studio_records("Typography Engine/SVG Exports", "Composition ID"),
        "print_exports": pod_studio_records("Typography Engine/Print Exports", "Composition ID"),
        "overview": note_card("Typography Engine Overview", "05_Business/Commerce/POD Design Studio/Typography Engine/Typography Engine Overview.md"),
        "reviews": note_card("Typography Reviews", "05_Business/Commerce/POD Design Studio/Typography Engine/Typography Reviews.md"),
        "composition_reviews": note_card("Composition Reviews", "05_Business/Commerce/POD Design Studio/Typography Engine/Composition Reviews.md"),
        "templates": note_card("Typography Templates", "05_Business/Commerce/POD Design Studio/Typography Engine/Typography Templates.md"),
        "brief": note_card("Typography Brief", "05_Business/Commerce/POD Design Studio/Typography Engine/Typography Brief.md"),
        "runtime": str(typography_runtime),
    }
    return {
        "enabled": bool(settings.get("pod_design_studio_enabled", True)),
        "runtime": str(runtime),
        "concepts": pod_studio_records("Concepts", "Concept ID"),
        "prompts": pod_studio_records("Design Prompts", "Concept ID"),
        "requests": pod_studio_records("Generation Requests", "Request ID"),
        "reviews": pod_studio_records("Design Reviews", "Design Review ID"),
        "refactors": pod_studio_records("Refactor Plans", "Design Review ID"),
        "listings": pod_studio_records("Listing Drafts", "Concept ID"),
        "exports": pod_studio_records("Export Packages", "Concept ID"),
        "generated": generated,
        "typography": typography,
        "overview": note_card("POD Design Studio Overview", "05_Business/Commerce/POD Design Studio/POD Design Studio Overview.md"),
        "tools": note_card("POD Studio Tool Registry", "05_Business/Commerce/POD Design Studio/POD Studio Tool Registry.md"),
        "pipeline": note_card("POD Product Pipeline", "05_Business/Commerce/POD Design Studio/POD Product Pipeline.md"),
        "workflow": note_card("POD Studio Workflow", "05_Business/Commerce/POD Design Studio/POD Studio Workflow.md"),
        "brief": note_card("POD Studio Brief", "05_Business/Commerce/POD Design Studio/POD Studio Brief.md"),
        "review": note_card("POD Studio Review", "05_Business/Commerce/POD Design Studio/POD Studio Review.md"),
        "comfyui_diagnostic": {
            "path": str(runtime / "logs" / "ComfyUI Diagnostic.md"),
            "content": excerpt(read_text(runtime / "logs" / "ComfyUI Diagnostic.md", 6000), 1600),
        },
        "overview": note_card("POD Design Studio Overview", "05_Business/Commerce/POD Design Studio/POD Design Studio Overview.md"),
        "tools": note_card("POD Studio Tool Registry", "05_Business/Commerce/POD Design Studio/POD Studio Tool Registry.md"),
        "workflow": note_card("POD Studio Workflow", "05_Business/Commerce/POD Design Studio/POD Studio Workflow.md"),
        "pipeline": note_card("POD Product Pipeline", "05_Business/Commerce/POD Design Studio/POD Product Pipeline.md"),
        "review": note_card("POD Studio Review", "05_Business/Commerce/POD Design Studio/POD Studio Review.md"),
        "brief": note_card("POD Studio Brief", "05_Business/Commerce/POD Design Studio/POD Studio Brief.md"),
        "export_index": note_card("POD Export Index", "05_Business/Commerce/POD Design Studio/POD Export Index.md"),
        "safety": {
            "publishing": bool(settings.get("pod_external_publishing_enabled", False)),
            "generation_confirmation": bool(settings.get("pod_requires_confirmation_for_generation", True)),
            "tool_confirmation": bool(settings.get("pod_requires_confirmation_for_tool_execution", True)),
            "raw_image_memory": bool(settings.get("pod_store_generated_images_in_memory", False)),
        },
    }


def brand_library_records(folder: str, id_heading: str) -> list[dict[str, Any]]:
    root = vault_path() / "05_Business" / "Asset & Brand Library" / folder
    rows: list[dict[str, Any]] = []
    if not root.exists():
        return rows
    for path in sorted(root.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 120000)
        rows.append({
            "id": section_value(text, id_heading) or path.name.split(" ", 1)[0],
            "name": section_value(text, "Name") or path.stem,
            "type": section_value(text, "Asset Type"),
            "status": section_value(text, "Status") or "Generated note",
            "tags": section_value(text, "Tags").replace("\n", ", "),
            "path": str(path),
            "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        })
    return rows


def asset_brand_library_data() -> dict[str, Any]:
    settings = load_settings()
    runtime = Path(str(settings.get("runtime_path", "R:/RaphaelOS"))) / "BrandLibrary"
    asset_folders = ["Logos", "POD Assets", "Content Assets", "Agency Assets", "Creator Assets", "Exported Assets"]
    assets = []
    for folder in asset_folders:
        assets.extend(brand_library_records(folder, "Asset ID"))
    assets = [row for row in assets if str(row.get("id", "")).startswith("ASSET-")]
    assets.sort(key=lambda row: row["updated"], reverse=True)
    return {
        "enabled": bool(settings.get("asset_library_enabled", True) and settings.get("brand_library_enabled", True)),
        "runtime": str(runtime),
        "brands": brand_library_records("Brands", "Brand ID"),
        "assets": assets,
        "reviews": brand_library_records("Asset Reviews", "Asset ID"),
        "overview": note_card("Asset Library Overview", "05_Business/Asset & Brand Library/Asset Library Overview.md"),
        "brand_registry": note_card("Brand Registry", "05_Business/Asset & Brand Library/Brand Registry.md"),
        "asset_registry": note_card("Asset Registry", "05_Business/Asset & Brand Library/Asset Registry.md"),
        "prompt_library": note_card("Prompt Library", "05_Business/Asset & Brand Library/Prompt Library.md"),
        "template_library": note_card("Template Library", "05_Business/Asset & Brand Library/Templates/Template Library.md"),
        "design_systems": note_card("Design System Registry", "05_Business/Asset & Brand Library/Design System Registry.md"),
        "brand_review": note_card("Brand Review", "05_Business/Asset & Brand Library/Brand Review.md"),
        "asset_review": note_card("Asset Review", "05_Business/Asset & Brand Library/Asset Review.md"),
        "safety": {
            "import_confirmation": bool(settings.get("asset_requires_confirmation_for_import", True)),
            "export_confirmation": bool(settings.get("asset_requires_confirmation_for_export", True)),
            "memory_images": bool(settings.get("asset_store_images_in_memory", False)),
        },
    }


def agency_note_records(subfolder: str) -> list[dict[str, str]]:
    root = vault_path() / "05_Business" / "Agency" / subfolder
    rows: list[dict[str, str]] = []
    if not root.exists():
        return rows
    for path in sorted(root.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 10000)
        rows.append({
            "name": path.stem,
            "subject": section_value(text, "Service Name") or section_value(text, "Client Type") or section_value(text, "Project Type") or path.stem,
            "target": excerpt(section_value(text, "Target Customer") or section_value(text, "Pain Points") or section_value(text, "Offer Description"), 180),
            "next": excerpt(section_value(text, "Next Actions") or section_value(text, "Completion Criteria"), 180),
            "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            "path": str(path),
        })
    return rows


def agency_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("agency_council_enabled", True)),
        "requires_confirmation": bool(settings.get("agency_requires_confirmation_for_delegation", True)),
        "no_external_outreach": bool(settings.get("agency_no_external_outreach", True)),
        "overview": note_card("Agency Council Overview", "05_Business/Agency/Agency Council Overview.md"),
        "strategy": note_card("Agency Strategy", "05_Business/Agency/Agency Strategy.md"),
        "brief": note_card("Agency Brief", "05_Business/Agency/Agency Brief.md"),
        "pipeline": note_card("Agency Pipeline", "05_Business/Agency/Agency Pipeline.md"),
        "review": note_card("Agency Review", "05_Business/Agency/Agency Review.md"),
        "task_board": note_card("Agency Task Board", "05_Business/Agency/Agency Task Board.md"),
        "kpis": note_card("Agency KPI Draft", "05_Business/Agency/Agency KPI Draft.md"),
        "catalog": note_card("Agency Service Catalog", "05_Business/Agency/Agency Service Catalog.md"),
        "service_offers": agency_note_records("Service Offers"),
        "client_profiles": agency_note_records("Lead Research"),
        "proposal_plans": agency_note_records("Proposals"),
        "delivery_plans": agency_note_records("Client Delivery"),
    }


def creator_note_records(subfolder: str) -> list[dict[str, str]]:
    root = vault_path() / "05_Business" / "Creator" / subfolder
    rows: list[dict[str, str]] = []
    if not root.exists():
        return rows
    for path in sorted(root.glob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True):
        text = read_text(path, 10000)
        rows.append({
            "name": path.stem,
            "subject": section_value(text, "Topic") or section_value(text, "Offer") or path.stem,
            "audience": excerpt(section_value(text, "Audience") or section_value(text, "Target Audience") or section_value(text, "Content Pillar"), 180),
            "next": excerpt(section_value(text, "Next Actions") or section_value(text, "CTA Strategy") or section_value(text, "Funnel Structure"), 180),
            "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            "path": str(path),
        })
    return rows


def creator_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("creator_council_enabled", True)),
        "requires_confirmation": bool(settings.get("creator_requires_confirmation_for_delegation", True)),
        "no_publishing": bool(settings.get("creator_no_publishing", True)),
        "overview": note_card("Creator Council Overview", "05_Business/Creator/Creator Council Overview.md"),
        "strategy": note_card("Creator Strategy", "05_Business/Creator/Creator Strategy.md"),
        "brief": note_card("Creator Brief", "05_Business/Creator/Creator Brief.md"),
        "pipeline": note_card("Creator Pipeline", "05_Business/Creator/Creator Pipeline.md"),
        "review": note_card("Creator Review", "05_Business/Creator/Creator Review.md"),
        "task_board": note_card("Creator Task Board", "05_Business/Creator/Creator Task Board.md"),
        "kpis": note_card("Creator KPI Draft", "05_Business/Creator/Creator KPI Draft.md"),
        "calendar": note_card("Creator Content Calendar", "05_Business/Creator/Creator Content Calendar.md"),
        "content_ideas": creator_note_records("Content Ideas"),
        "content_plans": creator_note_records("Content Calendar"),
        "scripts": creator_note_records("Scripts"),
        "ebooks": creator_note_records("Ebooks"),
        "offers": creator_note_records("Offers"),
    }


def kpi_records() -> list[dict[str, str]]:
    path = vault_path() / "00_Raphael" / "KPIs" / "KPI Registry.md"
    text = read_text(path, 60000)
    rows: list[dict[str, str]] = []
    pattern = r"^## (KPI-\d{8}-[A-F0-9]+)\s+(.+?)(?=^## KPI-\d{8}-[A-F0-9]+|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        rows.append({
            "id": match.group(1),
            "name": subsection_value(body, "Name"),
            "category": subsection_value(body, "Category"),
            "owner": subsection_value(body, "Owner Council"),
            "target": subsection_value(body, "Target"),
            "current": subsection_value(body, "Current Value"),
            "previous": subsection_value(body, "Previous Value"),
            "status": subsection_value(body, "Status"),
            "updated": subsection_value(body, "Last Updated"),
            "notes": excerpt(subsection_value(body, "Notes"), 180),
        })
    return rows


def kpi_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("kpi_system_enabled", True)),
        "requires_confirmation": bool(settings.get("kpi_requires_confirmation_for_updates", True)),
        "auto_external": bool(settings.get("kpi_auto_collect_external_metrics", False)),
        "records": kpi_records(),
        "dashboard": note_card("KPI Dashboard", "00_Raphael/KPIs/KPI Dashboard.md"),
        "review": note_card("KPI Review", "00_Raphael/KPIs/KPI Review.md"),
        "brief": note_card("KPI Brief", "00_Raphael/KPIs/KPI Brief.md"),
        "targets": note_card("KPI Targets", "00_Raphael/KPIs/KPI Targets.md"),
        "history": note_card("KPI History", "00_Raphael/KPIs/KPI History.md"),
        "overview": note_card("KPI System Overview", "00_Raphael/KPIs/KPI System Overview.md"),
    }


def finance_records() -> list[dict[str, str]]:
    path = vault_path() / "00_Raphael" / "Financial Intelligence" / "Financial Ledger.md"
    text = read_text(path, 90000)
    rows: list[dict[str, str]] = []
    pattern = r"^## (FIN-\d{8}-[A-F0-9]+)\s+(.+?)(?=^## FIN-\d{8}-[A-F0-9]+|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        rows.append({
            "id": match.group(1),
            "date": subsection_value(body, "Date"),
            "type": subsection_value(body, "Type"),
            "business": subsection_value(body, "Business"),
            "amount": subsection_value(body, "Amount"),
            "description": excerpt(subsection_value(body, "Description"), 220),
            "category": subsection_value(body, "Category"),
            "project": subsection_value(body, "Related Project"),
            "kpi": subsection_value(body, "Related KPI"),
            "initiative": subsection_value(body, "Related Initiative"),
            "notes": excerpt(subsection_value(body, "Notes"), 180),
        })
    return rows


def finance_data() -> dict[str, Any]:
    settings = load_settings()
    rows = finance_records()
    revenue = sum(float(row.get("amount") or "0") for row in rows if row.get("type") == "Revenue")
    expenses = sum(float(row.get("amount") or "0") for row in rows if row.get("type") == "Expense")
    budgets = sum(float(row.get("amount") or "0") for row in rows if row.get("type") == "Budget")
    return {
        "enabled": bool(settings.get("financial_intelligence_enabled", True)),
        "requires_confirmation": bool(settings.get("financial_requires_confirmation_for_updates", True)),
        "external_accounts": bool(settings.get("financial_external_accounts_enabled", False)),
        "currency": str(settings.get("financial_default_currency", "USD")),
        "records": rows,
        "totals": {"revenue": revenue, "expenses": expenses, "budgets": budgets, "net": revenue - expenses},
        "overview": note_card("Financial Intelligence Overview", "00_Raphael/Financial Intelligence/Financial Intelligence Overview.md"),
        "ledger": note_card("Financial Ledger", "00_Raphael/Financial Intelligence/Financial Ledger.md"),
        "revenue": note_card("Revenue Tracker", "00_Raphael/Financial Intelligence/Revenue Tracker.md"),
        "expenses": note_card("Expense Tracker", "00_Raphael/Financial Intelligence/Expense Tracker.md"),
        "profit": note_card("Profit Summary", "00_Raphael/Financial Intelligence/Profit Summary.md"),
        "budget": note_card("Budget Plan", "00_Raphael/Financial Intelligence/Budget Plan.md"),
        "review": note_card("Financial Review", "00_Raphael/Financial Intelligence/Financial Review.md"),
        "brief": note_card("Financial Brief", "00_Raphael/Financial Intelligence/Financial Brief.md"),
        "forecast": note_card("Financial Forecast", "00_Raphael/Financial Intelligence/Financial Forecast.md"),
    }


def portfolio_records() -> list[dict[str, str]]:
    text = read_text(vault_path() / "00_Raphael" / "Business Portfolio" / "Portfolio Scorecard.md", 60000)
    rows: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| PORTREC-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 12:
            rows.append({
                "id": cells[0],
                "business": cells[1],
                "council": cells[2],
                "score": cells[3],
                "revenue": cells[4],
                "expenses": cells[5],
                "profit": cells[6],
                "potential": cells[7],
                "speed": cells[8],
                "strategic": cells[9],
                "momentum": cells[10],
                "action": cells[11],
            })
    return rows


def portfolio_data() -> dict[str, Any]:
    settings = load_settings()
    rows = portfolio_records()
    sorted_rows = sorted(rows, key=lambda row: -int(row.get("score") or "0"))
    return {
        "enabled": bool(settings.get("business_portfolio_enabled", True)),
        "requires_confirmation": bool(settings.get("portfolio_requires_confirmation_for_delegation", True)),
        "records": sorted_rows,
        "top": sorted_rows[0] if sorted_rows else {},
        "overview": note_card("Portfolio System Overview", "00_Raphael/Business Portfolio/Portfolio System Overview.md"),
        "portfolio": note_card("Business Portfolio", "00_Raphael/Business Portfolio/Business Portfolio.md"),
        "scorecard": note_card("Portfolio Scorecard", "00_Raphael/Business Portfolio/Portfolio Scorecard.md"),
        "review": note_card("Portfolio Review", "00_Raphael/Business Portfolio/Portfolio Review.md"),
        "brief": note_card("Portfolio Brief", "00_Raphael/Business Portfolio/Portfolio Brief.md"),
        "roadmap": note_card("Portfolio Roadmap", "00_Raphael/Business Portfolio/Portfolio Roadmap.md"),
        "decisions": note_card("Portfolio Decisions", "00_Raphael/Business Portfolio/Portfolio Decisions.md"),
    }


def notification_records() -> list[dict[str, str]]:
    text = read_text(vault_path() / "00_Raphael" / "Notifications" / "Notification Inbox.md", 120000)
    rows: list[dict[str, str]] = []
    pattern = r"^## (NOTIF-\d{8}-[A-F0-9]+)\s+(.+?)(?=^## NOTIF-\d{8}-[A-F0-9]+|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        rows.append({
            "id": match.group(1),
            "title": subsection_value(body, "Title"),
            "type": subsection_value(body, "Type"),
            "severity": subsection_value(body, "Severity"),
            "description": excerpt(subsection_value(body, "Description"), 220),
            "source": subsection_value(body, "Source System"),
            "project": subsection_value(body, "Related Project"),
            "business": subsection_value(body, "Related Business"),
            "council": subsection_value(body, "Related Council"),
            "employee": subsection_value(body, "Related Employee"),
            "kpi": subsection_value(body, "Related KPI"),
            "initiative": subsection_value(body, "Related Initiative"),
            "action": excerpt(subsection_value(body, "Recommended Action"), 220),
            "status": subsection_value(body, "Status"),
            "created": subsection_value(body, "Created Date"),
        })
    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Info": 4}
    return sorted(rows, key=lambda row: (row.get("status") != "New", severity_order.get(row.get("severity", "Info"), 4), row.get("created", "")))


def notification_sector_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    sectors = {"Executive Control Plane": 0, "Agent Runtime": 0, "Execution Layer": 0, "Deliberation Engine": 0, "Council Governance": 0}
    for row in rows:
        if row.get("status") != "New":
            continue
        ntype = row.get("type", "")
        if ntype in {"Initiative Alert", "Portfolio Alert", "Council Alert"}:
            sectors["Executive Control Plane"] += 1
        if ntype in {"Search/Vision Alert", "System Alert", "Self-Improvement Alert"}:
            sectors["Agent Runtime"] += 1
        if ntype in {"Task Alert", "Execution Alert", "Builder Alert"}:
            sectors["Execution Layer"] += 1
        if ntype in {"Opportunity Alert", "Portfolio Alert"}:
            sectors["Deliberation Engine"] += 1
        if ntype in {"KPI Alert", "Financial Alert"}:
            sectors["Council Governance"] += 1
    return sectors


def notification_data() -> dict[str, Any]:
    settings = load_settings()
    rows = notification_records()
    active = [row for row in rows if row.get("status") != "Dismissed"]
    critical_high = [row for row in rows if row.get("status") == "New" and row.get("severity") in {"Critical", "High"}]
    return {
        "enabled": bool(settings.get("notification_center_enabled", True)),
        "auto_detect": bool(settings.get("notification_auto_detect_enabled", True)),
        "requires_confirmation": bool(settings.get("notification_requires_confirmation_for_delegation", True)),
        "max_active": int(settings.get("notification_max_active", 50)),
        "records": active,
        "critical_high_count": len(critical_high),
        "sector_counts": notification_sector_counts(rows),
        "overview": note_card("Notification Center Overview", "00_Raphael/Notifications/Notification Center Overview.md"),
        "inbox": note_card("Notification Inbox", "00_Raphael/Notifications/Notification Inbox.md"),
        "rules": note_card("Notification Rules", "00_Raphael/Notifications/Notification Rules.md"),
        "review": note_card("Notification Review", "00_Raphael/Notifications/Notification Review.md"),
        "brief": note_card("Notification Brief", "00_Raphael/Notifications/Notification Brief.md"),
        "history": note_card("Notification History", "00_Raphael/Notifications/Notification History.md"),
    }


def executive_brief_data() -> dict[str, Any]:
    settings = load_settings()
    root = vault_path() / "00_Raphael" / "Executive Briefs"
    executive_files = sorted(root.glob("Executive Brief - *.md"), key=lambda path: path.stat().st_mtime, reverse=True) if root.exists() else []
    latest_path = executive_files[0] if executive_files else root / "Morning Brief.md"
    latest_text = read_text(latest_path, 4000)
    return {
        "enabled": bool(settings.get("executive_brief_engine_enabled", True)),
        "latest": {
            "label": latest_path.stem if latest_path.exists() else "Latest Brief",
            "path": str(latest_path),
            "exists": latest_path.exists(),
            "updated": dt.datetime.fromtimestamp(latest_path.stat().st_mtime).isoformat(timespec="seconds") if latest_path.exists() else "",
            "content": excerpt(latest_text, 1400) if latest_text else "",
        },
        "overview": note_card("Executive Brief System Overview", "00_Raphael/Executive Briefs/Executive Brief System Overview.md"),
        "morning": note_card("Morning Brief", "00_Raphael/Executive Briefs/Morning Brief.md"),
        "evening": note_card("Evening Review", "00_Raphael/Executive Briefs/Evening Review.md"),
        "weekly": note_card("Weekly Executive Brief", "00_Raphael/Executive Briefs/Weekly Executive Brief.md"),
        "monthly": note_card("Monthly Business Review", "00_Raphael/Executive Briefs/Monthly Business Review.md"),
        "history": note_card("Brief History", "00_Raphael/Executive Briefs/Brief History.md"),
        "preferences": note_card("Brief Preferences", "00_Raphael/Executive Briefs/Brief Preferences.md"),
    }


def daily_operating_data() -> dict[str, Any]:
    date = dt.date.today().isoformat()
    root = vault_path() / "00_Raphael" / "Daily Operating Loop"
    start_path = root / f"{date} Daily Start.md"
    focus_path = root / f"{date} Daily Focus.md"
    plan_path = root / f"{date} Daily Plan.md"
    checkins_path = root / f"{date} Check-ins.md"
    end_path = root / f"{date} Daily End.md"
    start_text = read_text(start_path, 12000)
    focus_text = read_text(focus_path, 12000)
    plan_text = read_text(plan_path, 12000)
    end_text = read_text(end_path, 12000)
    current_focus = section_value(focus_text, "Today's Focus") or section_value(start_text, "Top Priority")
    task_text = section_value(focus_text, "Top 3 Tasks") or section_value(start_text, "Top 3 Tasks")
    warning_text = section_value(focus_text, "Protect Attention From") or section_value(start_text, "Warnings")
    return {
        "date": date,
        "focus": current_focus or "Run daily-start to establish today's focus.",
        "tasks": task_text or "No daily task snapshot generated yet.",
        "warnings": warning_text or "No daily warning snapshot generated yet.",
        "checkins": note_card("Daily Check-ins", f"00_Raphael/Daily Operating Loop/{date} Check-ins.md"),
        "end_review": note_card("Daily End", f"00_Raphael/Daily Operating Loop/{date} Daily End.md"),
        "start": note_card("Daily Start", f"00_Raphael/Daily Operating Loop/{date} Daily Start.md"),
        "plan": note_card("Daily Plan", f"00_Raphael/Daily Operating Loop/{date} Daily Plan.md"),
        "review": note_card("Daily Review", "00_Raphael/Daily Operating Loop/Daily Review.md"),
        "plan_blocks": {
            "focus_1": section_value(plan_text, "Focus Block 1"),
            "focus_2": section_value(plan_text, "Focus Block 2"),
            "admin": section_value(plan_text, "Admin Block"),
            "optional": section_value(plan_text, "Optional Creative / Business Block"),
        },
        "end_sections": {
            "done": section_value(end_text, "What Got Done"),
            "moved": section_value(end_text, "What Moved"),
            "blockers": section_value(end_text, "Blockers"),
            "tomorrow": section_value(end_text, "Tomorrow Recommendation"),
        },
        "safety": "Advisory generated notes only; no autonomous or external actions.",
    }


def activity_records() -> list[dict[str, str]]:
    text = read_text(vault_path() / "00_Raphael" / "Activity Stream" / "Activity Sources.md", 300000)
    rows: list[dict[str, str]] = []
    for match in re.finditer(r"^###\s+(EVENT-[^\n]+)\n(.*?)(?=^###\s+EVENT-|\Z)", text, flags=re.M | re.S):
        row = {"Event ID": match.group(1).strip()}
        for line in match.group(2).splitlines():
            if not line.startswith("- ") or ":" not in line:
                continue
            key, value = line[2:].split(":", 1)
            row[key.strip()] = value.strip()
        rows.append(row)
    return sorted(rows, key=lambda item: item.get("Timestamp", ""), reverse=True)


def activity_summary(rows: list[dict[str, str]]) -> dict[str, Any]:
    today = dt.datetime.now().date()
    week_start = today - dt.timedelta(days=7)
    month_start = today.replace(day=1)

    def event_date(row: dict[str, str]) -> dt.date | None:
        try:
            return dt.datetime.fromisoformat(row.get("Timestamp", "").replace("Z", "")).date()
        except ValueError:
            return None

    dates = [(row, event_date(row)) for row in rows]
    councils = {}
    businesses = {}
    empty_markers = {"", "Unassigned", "Unlinked", "Unknown", "None"}
    for row in rows:
        council = row.get("Related Council", "")
        business = row.get("Related Business", "")
        if council not in empty_markers:
            councils[council] = councils.get(council, 0) + 1
        if business not in empty_markers:
            businesses[business] = businesses.get(business, 0) + 1
    most_active_council = max(councils, key=councils.get) if councils else "Unassigned"
    most_active_business = max(businesses, key=businesses.get) if businesses else "Unassigned"
    return {
        "today": sum(1 for _, date_value in dates if date_value == today),
        "week": sum(1 for _, date_value in dates if date_value and date_value >= week_start),
        "month": sum(1 for _, date_value in dates if date_value and date_value >= month_start),
        "most_active_council": most_active_council,
        "most_active_business": most_active_business,
        "critical_events": sum(1 for row in rows if row.get("Severity") == "Critical"),
        "high_events": sum(1 for row in rows if row.get("Severity") == "High"),
    }


def activity_sector_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    sectors = {"Executive Control Plane": 0, "Agent Runtime": 0, "Execution Layer": 0, "Deliberation Engine": 0, "Council Governance": 0}
    for row in rows:
        event_type = row.get("Event Type", "")
        if event_type in {"Initiative Event", "Portfolio Event", "Council Event", "Brief Event"}:
            sectors["Executive Control Plane"] += 1
        elif event_type in {"Search Event", "Vision Event", "System Event"}:
            sectors["Agent Runtime"] += 1
        elif event_type in {"Task Event", "Execution Event", "Builder Event", "Workflow Event", "Employee Event"}:
            sectors["Execution Layer"] += 1
        elif event_type in {"Opportunity Event", "Finance Event"}:
            sectors["Deliberation Engine"] += 1
        elif event_type in {"KPI Event", "Notification Event"}:
            sectors["Council Governance"] += 1
    return sectors


def activity_data() -> dict[str, Any]:
    settings = load_settings()
    rows = activity_records()
    return {
        "enabled": bool(settings.get("activity_stream_enabled", True)),
        "auto_capture": bool(settings.get("activity_auto_capture", True)),
        "records": rows,
        "recent": rows[:10],
        "summary": activity_summary(rows),
        "sector_counts": activity_sector_counts(rows),
        "overview": note_card("Activity Stream Overview", "00_Raphael/Activity Stream/Activity Stream Overview.md"),
        "feed": note_card("Activity Feed", "00_Raphael/Activity Stream/Activity Feed.md"),
        "timeline": note_card("Activity Timeline", "00_Raphael/Activity Stream/Activity Timeline.md"),
        "stats": note_card("Activity Statistics", "00_Raphael/Activity Stream/Activity Statistics.md"),
        "review": note_card("Activity Review", "00_Raphael/Activity Stream/Activity Review.md"),
        "brief": note_card("Activity Brief", "00_Raphael/Activity Stream/Activity Brief.md"),
        "sources": note_card("Activity Sources", "00_Raphael/Activity Stream/Activity Sources.md"),
    }


def initiative_records() -> list[dict[str, str]]:
    path = vault_path() / "00_Raphael" / "Executive Initiatives" / "Initiative Inbox.md"
    text = read_text(path, 90000)
    rows: list[dict[str, str]] = []
    pattern = r"^## (INIT-\d{8}-[A-F0-9]+)\s+(.+?)(?=^## INIT-\d{8}-[A-F0-9]+|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        rows.append({
            "id": match.group(1),
            "title": subsection_value(body, "Title"),
            "type": subsection_value(body, "Type"),
            "score": subsection_value(body, "Overall Score"),
            "priority": subsection_value(body, "Priority"),
            "status": subsection_value(body, "Status"),
            "council": subsection_value(body, "Suggested Council"),
            "agents": subsection_value(body, "Suggested Agents"),
            "evidence": excerpt(subsection_value(body, "Source Evidence"), 220),
            "action": excerpt(subsection_value(body, "Recommended Action"), 220),
            "benefit": excerpt(subsection_value(body, "Expected Benefit"), 180),
            "created": subsection_value(body, "Created Date"),
        })
    return rows


def initiative_data() -> dict[str, Any]:
    settings = load_settings()
    rows = sorted(initiative_records(), key=lambda item: -int(item.get("score") or "0"))
    return {
        "enabled": bool(settings.get("executive_initiative_engine_enabled", True)),
        "requires_confirmation": bool(settings.get("initiative_requires_confirmation_for_delegation", True)),
        "auto_execute": bool(settings.get("initiative_auto_execute", False)),
        "threshold": int(settings.get("initiative_score_threshold", 70)),
        "records": rows,
        "top": rows[:5],
        "overview": note_card("Executive Initiative Overview", "00_Raphael/Executive Initiatives/Executive Initiative Overview.md"),
        "inbox": note_card("Initiative Inbox", "00_Raphael/Executive Initiatives/Initiative Inbox.md"),
        "scores": note_card("Initiative Scores", "00_Raphael/Executive Initiatives/Initiative Scores.md"),
        "review": note_card("Initiative Review", "00_Raphael/Executive Initiatives/Initiative Review.md"),
        "brief": note_card("Initiative Brief", "00_Raphael/Executive Initiatives/Initiative Brief.md"),
        "history": note_card("Initiative History", "00_Raphael/Executive Initiatives/Initiative History.md"),
    }


def employee_records() -> list[dict[str, str]]:
    path = vault_path() / "03_Agents" / "Digital Employees" / "Employee Registry.md"
    text = read_text(path, 100000)
    rows: list[dict[str, str]] = []
    pattern = r"^## (EMP-[A-F0-9]+)\s+(.+?)(?=^## EMP-[A-F0-9]+|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        rows.append({
            "id": match.group(1),
            "name": subsection_value(body, "Employee Name"),
            "role": subsection_value(body, "Role"),
            "department": subsection_value(body, "Department/Council"),
            "manager": subsection_value(body, "Manager"),
            "workload": subsection_value(body, "Workload"),
            "performance": subsection_value(body, "Performance Status"),
            "responsibilities": excerpt(subsection_value(body, "Responsibilities"), 700),
            "kpis": excerpt(subsection_value(body, "Assigned KPIs"), 180),
            "tasks": excerpt(subsection_value(body, "Current Tasks"), 220),
            "business": subsection_value(body, "Related Business Area"),
            "projects": subsection_value(body, "Related Projects"),
            "reviewed": subsection_value(body, "Last Review Date"),
        })
    return rows


def employee_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("digital_employee_system_enabled", True)),
        "reviews_enabled": bool(settings.get("digital_employee_reviews_enabled", True)),
        "requires_reassignment_confirmation": bool(settings.get("digital_employee_requires_confirmation_for_reassignment", True)),
        "records": employee_records(),
        "overview": note_card("Digital Employee System Overview", "03_Agents/Digital Employees/Digital Employee System Overview.md"),
        "registry": note_card("Employee Registry", "03_Agents/Digital Employees/Employee Registry.md"),
        "org_chart": note_card("Employee Org Chart", "03_Agents/Digital Employees/Employee Org Chart.md"),
        "kpi_map": note_card("Employee KPI Map", "03_Agents/Digital Employees/Employee KPI Map.md"),
        "performance": note_card("Employee Performance Reviews", "03_Agents/Digital Employees/Employee Performance Reviews.md"),
        "workload": note_card("Employee Workload Review", "03_Agents/Digital Employees/Employee Workload Review.md"),
        "brief": note_card("Employee Brief", "03_Agents/Digital Employees/Employee Brief.md"),
    }


def _employee_network_data_legacy() -> dict[str, Any]:
    registry = employee_records()
    registry_by_name = {item.get("name"): item for item in registry if item.get("name")}
    agent_rows = agents()
    task_rows = tasks()
    kpi_rows = kpi_records()
    activity_rows = activity_records()
    council_map: dict[str, str] = {}
    for council, meta in COUNCILS.items():
        for member in meta.get("members", []):
            council_map.setdefault(member, council)
    names = sorted(set(registry_by_name) | {item["name"] for item in agent_rows})
    agent_by_name = {item["name"]: item for item in agent_rows}
    employees: list[dict[str, Any]] = []
    for index, name in enumerate(names):
        record = registry_by_name.get(name, {})
        agent = agent_by_name.get(name, {})
        council = record.get("department") or council_map.get(name, "Unassigned")
        council = council if "Council" in council else council_map.get(name, council or "Unassigned")
        employee_tasks = [item for item in task_rows if item.get("agent") == name]
        open_tasks = [item for item in employee_tasks if item.get("status") not in {"Done", "Archived", "Completed"}]
        blocked_tasks = [item for item in employee_tasks if item.get("status") == "Blocked"]
        kpi_text = record.get("kpis", "")
        assigned_kpis = [
            item for item in kpi_rows
            if item.get("id") in kpi_text
            or item.get("name") in kpi_text
            or (item.get("owner") == council and name in COUNCILS.get(council, {}).get("members", []))
        ]
        activity = [
            item for item in activity_rows
            if item.get("Related Employee") == name
            or name.lower() in (item.get("Title", "") + " " + item.get("Details", "")).lower()
        ][:8]
        workload = record.get("workload") or ("High" if len(open_tasks) >= 6 else "Normal" if open_tasks else "Low")
        performance = record.get("performance") or "Unknown"
        workload_penalty = {"Low": 0, "Normal": 3, "High": 12, "Overloaded": 24}.get(workload, 5)
        performance_penalty = {"Strong": 0, "Stable": 3, "Needs Attention": 18, "Unknown": 6}.get(performance, 6)
        at_risk_kpis = sum(1 for item in assigned_kpis if item.get("status") in {"At Risk", "Behind"})
        health = max(20, min(100, 96 - workload_penalty - performance_penalty - len(blocked_tasks) * 12 - at_risk_kpis * 8))
        recommendations: list[str] = []
        if blocked_tasks:
            recommendations.append("Resolve blocked tasks or escalate the dependency to Aaron.")
        if workload in {"High", "Overloaded"}:
            recommendations.append("Reduce concurrent work and clarify the next highest-priority output.")
        if not assigned_kpis and open_tasks:
            recommendations.append("Attach a measurable KPI or completion criterion to active work.")
        if not open_tasks:
            recommendations.append("Review council priorities and prepare the next scoped task.")
        if not recommendations:
            recommendations.append("Continue current task order and report progress through the task log.")
        employees.append({
            "id": record.get("id") or f"EMP-NET-{index + 1:03d}",
            "name": name,
            "role": record.get("role") or name.replace(" Agent", ""),
            "council": council,
            "department": record.get("department") or council,
            "manager": record.get("manager") or council,
            "health": health,
            "workload": workload,
            "performance_status": performance,
            "responsibilities": record.get("responsibilities") or "Responsibilities are defined by the agent scaffold.",
            "open_tasks": open_tasks,
            "blocked_tasks": blocked_tasks,
            "assigned_kpis": assigned_kpis,
            "related_business": record.get("business") or "Unlinked",
            "related_projects": record.get("projects") or "Unlinked",
            "recent_activity": activity,
            "performance_review": f"{performance}. Last reviewed: {record.get('reviewed') or 'Not recorded'}.",
            "recommendations": recommendations,
            "recommended_next_work": recommendations[0],
        })
    grouped: dict[str, list[str]] = {}
    for employee in employees:
        grouped.setdefault(employee["council"], []).append(employee["id"])
    return {
        "root": {"name": "Aaron", "role": "Final Decision-Maker"},
        "orchestrator": {"name": "Raphael", "role": "Executive AI Operating System"},
        "councils": council_status_data(),
        "employees": employees,
        "groups": grouped,
    }


def employee_network_data() -> dict[str, Any]:
    employees = employee_records()
    task_rows = tasks()
    kpi_rows = kpi_records()
    activity_rows = activity_records()
    review_text = read_text(vault_path() / "03_Agents" / "Digital Employees" / "Employee Performance Reviews.md", 100000)
    council_colors = {
        "Executive Council": "#ffd166",
        "Commerce Council": "#55f28f",
        "Agency Council": "#5ba7ff",
        "Creator Council": "#ff37d4",
        "Research Council": "#31d8ff",
        "Operations Council": "#ff9f1c",
        "Financial Council": "#20e3a2",
        "Portfolio Council": "#ffffff",
        "Governance Council": "#cfd8dc",
    }
    network_employees: list[dict[str, Any]] = []
    council_groups: dict[str, list[str]] = {}
    for employee in employees:
        name = employee.get("name", "")
        council = employee.get("department") or "Unassigned"
        employee_tasks = [row for row in task_rows if row.get("agent") == name]
        open_tasks = [row for row in employee_tasks if row.get("status") not in {"Done", "Archived", "Completed"}]
        blocked_tasks = [row for row in employee_tasks if row.get("status") == "Blocked"]
        kpi_ids = set(re.findall(r"KPI-\d{8}-[A-F0-9]+", employee.get("kpis", "")))
        assigned_kpis = [
            row for row in kpi_rows
            if row.get("id") in kpi_ids
            or (row.get("owner") == council and name.split()[0].lower() in (row.get("name") or "").lower())
        ]
        recent_activity = [
            row for row in activity_rows
            if row.get("Related Employee") == name
            or name.lower() in (row.get("Title", "") + " " + row.get("Details", "")).lower()
        ][:8]
        performance = employee.get("performance") or "Unknown"
        workload = employee.get("workload") or "Low"
        workload_penalty = {"Low": 0, "Normal": 4, "High": 12, "Overloaded": 24}.get(workload, 6)
        performance_penalty = {"Strong": 0, "Stable": 5, "Needs Attention": 18, "Unknown": 8}.get(performance, 8)
        at_risk_kpis = sum(1 for row in assigned_kpis if row.get("status") in {"At Risk", "Behind"})
        health = max(20, min(100, 96 - workload_penalty - performance_penalty - len(blocked_tasks) * 12 - at_risk_kpis * 8))
        recommendations: list[str] = []
        if blocked_tasks:
            recommendations.append("Resolve blocked work or identify the decision needed from Aaron.")
        if workload in {"High", "Overloaded"}:
            recommendations.append("Reduce workload or rebalance lower-priority tasks.")
        if not assigned_kpis:
            recommendations.append("Review whether this role needs a measurable KPI.")
        if not open_tasks:
            recommendations.append("Prepare the next task brief aligned to the owning council.")
        if not recommendations:
            recommendations.append("Continue the highest-priority open task and report measurable progress.")
        review_match = re.search(
            rf"^##+\s+.*{re.escape(name)}.*?\n(.*?)(?=^##+\s+|\Z)",
            review_text,
            flags=re.M | re.S | re.I,
        )
        network_employees.append({
            "employee_id": employee.get("id"),
            "employee_name": name,
            "role": employee.get("role") or name.replace(" Agent", ""),
            "council": council,
            "department": council,
            "manager": employee.get("manager") or "Raphael",
            "health": health,
            "workload": workload,
            "performance_status": performance,
            "responsibilities": employee.get("responsibilities") or "Maintain context, produce recommendations, and escalate decisions.",
            "open_tasks": open_tasks,
            "blocked_tasks": blocked_tasks,
            "assigned_kpis": assigned_kpis,
            "related_business": employee.get("business") or council.replace(" Council", ""),
            "related_projects": employee.get("projects") or "Unassigned",
            "recent_activity": recent_activity,
            "performance_review_summary": excerpt(review_match.group(1), 500) if review_match else "No detailed performance review recorded yet.",
            "recommendations": recommendations,
            "recommended_next_work": recommendations[0],
            "safe_prompts": [
                f"show tasks for {name}",
                f"summarize KPI status for {name}",
                f"review workload for {name}",
            ],
            "color": council_colors.get(council, "#8ea6c8"),
        })
        council_groups.setdefault(council, []).append(name)
    return {
        "root": {"name": "Aaron", "role": "Final Decision-Maker"},
        "orchestrator": {"name": "Raphael", "role": "Executive AI Operating System"},
        "councils": [
            {
                "name": council,
                "color": council_colors.get(council, "#8ea6c8"),
                "employees": names,
                "health": round(sum(item["health"] for item in network_employees if item["council"] == council) / max(1, len(names))),
            }
            for council, names in sorted(council_groups.items())
        ],
        "employees": network_employees,
    }


def execution_records() -> list[dict[str, str]]:
    path = vault_path() / "00_Raphael" / "Controlled Execution" / "Execution Requests.md"
    text = read_text(path, 90000)
    rows: list[dict[str, str]] = []
    pattern = r"^## (EXEC-\d{8}-[A-F0-9]+)\s+(.+?)(?=^## EXEC-\d{8}-[A-F0-9]+|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        rows.append({
            "id": match.group(1),
            "description": subsection_value(body, "Action Description"),
            "level": subsection_value(body, "Detected Execution Level"),
            "type": subsection_value(body, "Action Type"),
            "system": subsection_value(body, "Related System"),
            "risk": subsection_value(body, "Risk Level"),
            "status": subsection_value(body, "Status"),
            "dry_run": subsection_value(body, "Dry Run Required"),
            "outputs": excerpt(subsection_value(body, "Expected Outputs"), 160),
            "created": subsection_value(body, "Created Date"),
        })
    return rows


def controlled_execution_data() -> dict[str, Any]:
    settings = load_settings()
    rows = execution_records()
    return {
        "enabled": bool(settings.get("controlled_execution_enabled", True)),
        "requires_confirmation": bool(settings.get("execution_requires_confirmation", True)),
        "voice_enabled": bool(settings.get("voice_execution_enabled", True)),
        "dashboard_enabled": bool(settings.get("dashboard_execution_enabled", True)),
        "max_level": int(settings.get("max_execution_level", 4)),
        "external_enabled": bool(settings.get("external_execution_enabled", False)),
        "dry_run_default": bool(settings.get("execution_dry_run_default", True)),
        "records": rows,
        "policy": note_card("Execution Policy", "00_Raphael/Controlled Execution/Execution Policy.md"),
        "allowlist": note_card("Execution Allowlist", "00_Raphael/Controlled Execution/Execution Allowlist.md"),
        "requests": note_card("Execution Requests", "00_Raphael/Controlled Execution/Execution Requests.md"),
        "review": note_card("Execution Review", "00_Raphael/Controlled Execution/Execution Review.md"),
        "log": note_card("Execution Log", "00_Raphael/Controlled Execution/Execution Log.md"),
        "safety": note_card("Execution Safety Report", "00_Raphael/Controlled Execution/Execution Safety Report.md"),
        "overview": note_card("Controlled Execution Overview", "00_Raphael/Controlled Execution/Controlled Execution Overview.md"),
    }


RAPHAEL_PRESENCE_ACTIONS = {
    "open_chat": {"target": "chat"},
    "open_voice": {"target": "voice"},
    "open_executive_brief": {"target": "briefs"},
    "open_notifications": {"target": "notifications"},
    "open_activity": {"target": "activity"},
    "open_portfolio": {"target": "portfolio"},
    "fill_chat_prompt": {"target": "chat"},
}


def _presence_line(text: str, heading: str) -> str:
    value = section_value(text, heading)
    for line in value.splitlines():
        clean = re.sub(r"^[\s\-*#>`]+", "", line).strip()
        if clean:
            return clean
    return ""


def raphael_presence_data(
    *,
    notifications: dict[str, Any] | None = None,
    briefs: dict[str, Any] | None = None,
    portfolio: dict[str, Any] | None = None,
    initiatives: dict[str, Any] | None = None,
    execution: dict[str, Any] | None = None,
    kpis: dict[str, Any] | None = None,
    council_status: dict[str, dict[str, Any]] | None = None,
    activity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    notifications = notifications or notification_data()
    briefs = briefs or executive_brief_data()
    portfolio = portfolio or portfolio_data()
    initiatives = initiatives or initiative_data()
    execution = execution or controlled_execution_data()
    kpis = kpis or kpi_data()
    council_status = council_status or council_status_data()
    activity = activity or activity_data()

    active_alerts = [
        row for row in notifications.get("records", [])
        if row.get("status") == "New" and row.get("severity") in {"Critical", "High"}
    ]
    top_alert_row = active_alerts[0] if active_alerts else {}
    top_initiative_row = (initiatives.get("top") or [{}])[0] if initiatives.get("top") else {}
    at_risk_kpis = [row for row in kpis.get("records", []) if row.get("status") in {"At Risk", "Behind"}]
    top_kpi_row = at_risk_kpis[0] if at_risk_kpis else {}
    running_execution = next(
        (row for row in execution.get("records", []) if row.get("status") in {"Running", "In Progress", "Executing"}),
        {},
    )
    portfolio_top = portfolio.get("top") or {}
    brief = briefs.get("latest") or {}
    brief_text = str(brief.get("content") or "")
    brief_focus = _presence_line(brief_text, "Recommended Focus")
    brief_action = _presence_line(brief_text, "Suggested Next Commands")
    portfolio_focus = portfolio_top.get("business") or brief_focus or "No portfolio focus recorded"
    top_priority = brief_focus or portfolio_top.get("action") or top_initiative_row.get("title") or "Review the executive brief"
    recommended_next_action = (
        top_alert_row.get("action")
        or top_initiative_row.get("action")
        or portfolio_top.get("action")
        or brief_action
        or "Review the highest-priority item with Raphael."
    )
    pending_command_bus = 1 if COMMAND_BUS_SESSION.get("pending_command_bus_route") else 0
    pending_legacy = 1 if PENDING_CHAT_ROUTE.get("route") is not None else 0
    pending_execution = sum(1 for row in execution.get("records", []) if row.get("status") == "Pending")
    pending_confirmations = pending_command_bus + pending_legacy + pending_execution
    active_councils = [
        name for name, row in council_status.items()
        if row.get("state") in {"active", "busy", "critical"}
    ]

    if active_alerts:
        orb_state = "warning"
        current_state = "attention_required"
        status_message = f"{len(active_alerts)} high-priority alert{'s' if len(active_alerts) != 1 else ''} need review."
    elif pending_confirmations:
        orb_state = "warning"
        current_state = "confirmation_required"
        status_message = "Confirmation required before the pending action can continue."
    elif running_execution:
        orb_state = "executing"
        current_state = "approved_execution_in_progress"
        status_message = f"Approved execution in progress: {running_execution.get('description') or running_execution.get('id')}."
    elif top_kpi_row:
        orb_state = "warning"
        current_state = "kpi_attention_required"
        status_message = f"KPI needs attention: {top_kpi_row.get('name') or top_kpi_row.get('id')}."
    elif brief.get("exists"):
        orb_state = "recommendation_ready"
        current_state = "executive_brief_ready"
        status_message = "Executive brief ready."
    elif portfolio_focus != "No portfolio focus recorded":
        orb_state = "recommendation_ready"
        current_state = "portfolio_focus_ready"
        status_message = f"Current portfolio focus: {portfolio_focus}."
    else:
        orb_state = "idle"
        current_state = "monitoring"
        status_message = "Systems monitored. Raphael is ready."

    recent = activity.get("recent") or []
    rotating_messages = [
        status_message,
        f"Top priority: {str(top_priority).rstrip('.!?')}.",
        f"Portfolio focus: {str(portfolio_focus).rstrip('.!?')}.",
    ]
    if top_alert_row:
        rotating_messages.append(f"Alert: {str(top_alert_row.get('title') or top_alert_row.get('description') or 'Review notifications').rstrip('.!?')}.")
    if top_initiative_row:
        rotating_messages.append(f"Initiative: {str(top_initiative_row.get('title')).rstrip('.!?')}.")
    if top_kpi_row:
        rotating_messages.append(f"KPI: {top_kpi_row.get('name')} is {top_kpi_row.get('status')}.")
    if running_execution:
        rotating_messages.append(f"Controlled execution: {running_execution.get('status')} — {running_execution.get('description')}.")
    if recent:
        rotating_messages.append(f"Recent activity: {recent[0].get('Title') or recent[0].get('Event ID')}.")

    return {
        "current_state": current_state,
        "status_message": status_message,
        "top_priority": top_priority,
        "top_alert": top_alert_row,
        "top_initiative": top_initiative_row,
        "top_kpi": top_kpi_row,
        "portfolio_focus": portfolio_focus,
        "recommended_next_action": recommended_next_action,
        "active_councils": active_councils,
        "pending_confirmations": pending_confirmations,
        "orb_state": orb_state,
        "rotating_messages": rotating_messages,
        "executive_greeting": f"Good {('morning' if dt.datetime.now().hour < 12 else 'afternoon' if dt.datetime.now().hour < 18 else 'evening')}, Aaron. {status_message}",
        "voice_available": bool(load_settings().get("dashboard_voice_control_enabled", True)),
        "read_only": True,
    }


def raphael_presence_action(payload: dict[str, Any]) -> dict[str, Any]:
    action = str(payload.get("action", "")).strip()
    if action not in RAPHAEL_PRESENCE_ACTIONS:
        return {
            "accepted": False,
            "status": "refused",
            "message": "Unsupported presence action. No command was executed.",
            "allowed_actions": sorted(RAPHAEL_PRESENCE_ACTIONS),
        }
    prompt = str(payload.get("prompt", "")).strip()
    if action == "fill_chat_prompt":
        if not prompt or len(prompt) > 300:
            return {
                "accepted": False,
                "status": "refused",
                "message": "A short safe chat prompt is required. No command was executed.",
            }
        safe_prompt = prompt.lower()
        allowed_starts = ("what ", "which ", "show ", "review ", "summarize ", "explain ", "brief ")
        blocked_terms = ("execute", "run ", "delegate", "assign", "reassign", "approve", "confirm", "delete", "send", "publish", "upload", "spend")
        if not safe_prompt.startswith(allowed_starts) or any(term in safe_prompt for term in blocked_terms):
            return {
                "accepted": False,
                "status": "refused",
                "message": "Only advisory or read-only chat prompts are accepted here. No command was executed.",
            }
    else:
        prompt = ""
    return {
        "accepted": True,
        "status": "navigation_only",
        "action": action,
        "target": RAPHAEL_PRESENCE_ACTIONS[action]["target"],
        "prompt": prompt,
        "message": "Safe presentation action accepted. No command was executed.",
        "command_executed": False,
        "command_bus_bypassed": False,
    }


def http_json(url: str, timeout: int = 3) -> tuple[bool, Any]:
    return True, {}


def system_health() -> dict[str, Any]:
    settings = load_settings()
    qdrant_ok, qdrant_data = http_json(str(settings.get("qdrant_url", "http://localhost:6333")).rstrip("/") + "/collections")
    ollama_ok, ollama_data = http_json("http://localhost:11434/api/tags")
    models = sorted(item.get("name", "") for item in (ollama_data.get("models", []) if isinstance(ollama_data, dict) else []) if item.get("name"))
    vision_model = str(settings.get("vision_model", ""))
    bare_vision = vision_model.split(":")[0]
    vision_available = any(model == vision_model or model.startswith(f"{bare_vision}:") or model == bare_vision for model in models)
    voice_config = runtime_path() / "voice" / "voice_config.json"
    voice = json.loads(read_text(voice_config) or "{}") if voice_config.exists() else {}
    piper_exe = Path(str(voice.get("piper_exe_path", ""))) if voice.get("piper_exe_path") else None
    piper_model = Path(str(voice.get("piper_voice_model_path", ""))) if voice.get("piper_voice_model_path") else None
    return {
        "qdrant": {"ok": qdrant_ok, "detail": "ok" if qdrant_ok else str(qdrant_data)},
        "ollama": {"ok": ollama_ok, "models": models, "detail": "ok" if ollama_ok else str(ollama_data)},
        "vision": {"model": vision_model, "available": vision_available, "enabled": bool(settings.get("vision_enabled", False))},
        "piper": {
            "engine": voice.get("tts_engine") or voice.get("text_to_speech_provider") or "unknown",
            "exe_exists": bool(piper_exe and piper_exe.exists()),
            "model_exists": bool(piper_model and piper_model.exists()),
        },
        "paths": {"vault": str(vault_path()), "runtime": str(runtime_path()), "config": str(CONFIG_PATH)},
        "dashboard_chat": dashboard_chat_settings(),
    }


def raphael_cli_path() -> Path:
    candidate = CONFIG_PATH.parent.parent / "raphael.py"
    if not candidate.exists():
        raise FileNotFoundError(f"Raphael CLI not found: {candidate}")
    return candidate


def service_manager_data() -> dict[str, Any]:
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(raphael_cli_path()),
                "--config",
                str(CONFIG_PATH),
                "service-status",
                "--json",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if completed.returncode != 0:
            raise RuntimeError((completed.stderr or completed.stdout).strip())
        return json.loads(completed.stdout)
    except Exception as exc:
        return {
            "generated": dt.datetime.now().isoformat(timespec="seconds"),
            "registry_path": str(runtime_path() / "launcher" / "service_registry.json"),
            "services": [],
            "error": str(exc),
        }


def _registered_service_ids() -> set[str]:
    return {str(row.get("service_id", "")) for row in service_manager_data().get("services", [])}


def _service_phrase(action: str, service_id: str) -> str:
    if action == "start_stack":
        phrases = {
            "required": "start Raphael services",
            "creative": "start creative stack",
            "voice": "start voice stack",
            "research": "start research stack",
        }
        if service_id not in phrases:
            raise ValueError("Unknown stack. Allowed stacks: required, creative, voice, research.")
        return phrases[service_id]
    if action == "health":
        return f"service status {service_id}"
    if action == "open":
        return f"open service {service_id}"
    return f"{action} service {service_id}"


def _parse_command_output(result: dict[str, Any]) -> Any:
    text = str(result.get("full_response", "")).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"message": text}


def _service_result_error(command_result: Any) -> str:
    if not isinstance(command_result, dict):
        return ""
    direct_result = str(command_result.get("result", "")).lower()
    direct_failures = {
        "failed", "disabled", "not_configured", "not_managed", "not_stoppable",
        "confirmation_required", "docker_unavailable", "ownership_conflict",
        "pull_failed", "create_failed", "created_start_failed", "not_found",
    }
    if direct_result in direct_failures:
        return str(command_result.get("error") or direct_result)
    rows = command_result.get("results", [])
    if not isinstance(rows, list):
        return ""
    failed = {
        "failed", "disabled", "not_configured", "not_managed", "not_stoppable",
        "confirmation_required", "missing_executable", "missing_working_directory",
        "docker_unavailable", "ownership_conflict", "pull_failed", "create_failed",
        "created_start_failed", "not_found",
    }
    errors = [
        str(row.get("error") or row.get("result"))
        for row in rows
        if str(row.get("result", "")).lower() in failed
    ]
    return "; ".join(error for error in errors if error)


def service_bus_action(action: str, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    service_id = str(payload.get("service_id", "")).strip().lower()
    confirmation_key = str(payload.get("confirmation_key", "")).strip()
    if not service_id or not all(ch.isalnum() or ch in "_-" for ch in service_id):
        return {"ok": False, "state": "error", "error": "Invalid service_id."}, 400
    if action == "start_stack":
        if service_id not in {"required", "creative", "voice", "research"}:
            return {"ok": False, "state": "error", "error": "Unknown service stack."}, 400
    elif service_id not in _registered_service_ids():
        return {"ok": False, "state": "error", "error": f"Unknown registry service_id: {service_id}"}, 404
    try:
        bus_module = load_command_bus()
        bus = bus_module.RaphaelCommandBus()
        if confirmation_key:
            result = bus.confirm(confirmation_key, SERVICE_COMMAND_BUS_SESSION)
        else:
            result = bus.route(_service_phrase(action, service_id), "dashboard_service_manager", SERVICE_COMMAND_BUS_SESSION)
    except Exception as exc:
        return {"ok": False, "state": "error", "error": str(exc)}, 500
    if result.get("status") == "needs_confirmation":
        return {
            "ok": True,
            "state": "pending_confirmation",
            "confirmation_required": True,
            "confirmation_key": result.get("confirmation_key", ""),
            "message": result.get("spoken_response", "Confirmation required."),
            "command": result.get("matched_command", ""),
            "service_id": service_id,
        }, 202
    command_result = _parse_command_output(result)
    error = _service_result_error(command_result)
    ok = result.get("status") == "routed" and not error
    current = service_manager_data()
    service = next((row for row in current.get("services", []) if row.get("service_id") == service_id), None)
    response = {
        "ok": ok,
        "state": "action_completed" if ok else "error",
        "confirmation_required": False,
        "message": result.get("spoken_response") or result.get("full_response") or error,
        "error": error or (result.get("safety_reason", "") if not ok else ""),
        "command": result.get("matched_command", ""),
        "service_id": service_id,
        "result": command_result,
        "service": service,
        "status": current,
    }
    return response, 200 if ok else 400


def workflow_bus_action(action: str, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    identifier = str(payload.get("workflow_id") or payload.get("exec_id") or "").strip()
    confirmation_key = str(payload.get("confirmation_key", "")).strip()
    if not identifier or not all(ch.isalnum() or ch in "_-" for ch in identifier):
        return {"ok": False, "state": "error", "error": "Invalid workflow or execution ID."}, 400
    phrases = {
        "execute": f"run workflow {identifier}",
        "cancel": f"cancel workflow {identifier}",
    }
    if action not in phrases:
        return {"ok": False, "state": "error", "error": f"Unsupported workflow action: {action}"}, 400
    if action == "execute":
        known = {str(row.get("workflow_id", "")).lower() for row in workflow_runner_data()["workflows"]}
        if identifier.lower() not in known:
            return {"ok": False, "state": "error", "error": f"Unknown registered workflow: {identifier}"}, 404
    else:
        known = {str(row.get("exec_id", "")).upper() for row in workflow_runner_data()["executions"]}
        if identifier.upper() not in known:
            return {"ok": False, "state": "error", "error": f"Unknown workflow execution: {identifier}"}, 404
    try:
        bus_module = load_command_bus()
        bus = bus_module.RaphaelCommandBus()
        result = (
            bus.confirm(confirmation_key, WORKFLOW_COMMAND_BUS_SESSION)
            if confirmation_key
            else bus.route(phrases[action], "dashboard_workflow_runner", WORKFLOW_COMMAND_BUS_SESSION)
        )
    except Exception as exc:
        return {"ok": False, "state": "error", "error": str(exc)}, 500
    if result.get("status") == "needs_confirmation":
        return {
            "ok": True,
            "state": "pending_confirmation",
            "confirmation_required": True,
            "confirmation_key": result.get("confirmation_key", ""),
            "message": result.get("spoken_response", "Confirmation required."),
            "command": result.get("matched_command", ""),
        }, 202
    command_result = _parse_command_output(result)
    ok = result.get("status") == "routed"
    return {
        "ok": ok,
        "state": "action_completed" if ok else "error",
        "confirmation_required": False,
        "message": result.get("spoken_response") or result.get("full_response"),
        "error": result.get("safety_reason", "") if not ok else "",
        "result": command_result,
        "workflow_runner": workflow_runner_data(),
    }, 200 if ok else 400


def workflow_cli_read(command: str, identifier: str = "") -> tuple[dict[str, Any], int]:
    allowed = {"workflow-monitor", "workflow-result", "workflow-runner-status", "workflow-failures"}
    if command not in allowed:
        return {"ok": False, "error": "Unsupported workflow read command."}, 400
    if identifier and not all(ch.isalnum() or ch in "_-" for ch in identifier):
        return {"ok": False, "error": "Invalid execution ID."}, 400
    args = [sys.executable, str(raphael_cli_path()), "--config", str(CONFIG_PATH), command]
    if identifier:
        args.append(identifier)
    completed = subprocess.run(args, capture_output=True, text=True, timeout=30)
    if completed.returncode != 0:
        return {"ok": False, "error": (completed.stderr or completed.stdout).strip()}, 400
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        result = {"message": completed.stdout.strip()}
    return {"ok": True, "result": result, "workflow_runner": workflow_runner_data()}, 200


def dashboard_chat_test_status_data() -> dict[str, Any]:
    root = vault_path() / "00_Raphael" / "Dashboard Chat Tests"
    report = root / "Dashboard Chat Smoke Test Report.md"
    history = root / "Dashboard Chat Test History.md"
    text = read_text(report, 200000)
    return {
        "report": str(report),
        "history": str(history),
        "exists": report.exists(),
        "passed": text.count("- Result: PASS"),
        "failed": text.count("- Result: FAIL"),
        "updated": dt.datetime.fromtimestamp(report.stat().st_mtime).isoformat(timespec="seconds") if report.exists() else "",
        "content": text,
    }


def run_dashboard_chat_smoke_test() -> tuple[dict[str, Any], int]:
    try:
        completed = subprocess.run(
            [
                sys.executable,
                str(raphael_cli_path()),
                "--config",
                str(CONFIG_PATH),
                "dashboard-chat-smoke-test",
            ],
            capture_output=True,
            text=True,
            timeout=180,
        )
        if completed.returncode != 0:
            return {"ok": False, "error": (completed.stderr or completed.stdout).strip(), "tests": dashboard_chat_test_status_data()}, 500
        result = json.loads(completed.stdout)
        return {"ok": True, "result": result, "tests": dashboard_chat_test_status_data()}, 200
    except Exception as exc:
        return {"ok": False, "error": str(exc), "tests": dashboard_chat_test_status_data()}, 500


def self_healing_cli(command: str, *args: str, timeout: int = 90) -> dict[str, Any]:
    allowed = {
        "self-healing-status", "observe-system", "detect-issues", "diagnose-issue",
        "repair-plan", "repair-approve", "repair-run", "repair-history", "reliability-brief",
    }
    if command not in allowed:
        raise ValueError(f"Unsupported self-healing command: {command}")
    completed = subprocess.run(
        [sys.executable, str(raphael_cli_path()), "--config", str(CONFIG_PATH), command, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout).strip())
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"message": completed.stdout.strip()}


def self_healing_data() -> dict[str, Any]:
    try:
        status = self_healing_cli("self-healing-status", timeout=45)
    except Exception as exc:
        return {
            "ok": False,
            "error": str(exc),
            "enabled": False,
            "health_score": 0,
            "active_issues": [],
            "repair_history": {"history": []},
            "notes": {},
        }
    try:
        history = self_healing_cli("repair-history", timeout=45)
    except Exception:
        history = {"history": []}
    root = vault_path() / "00_Raphael" / "Self Healing"
    return {
        "ok": True,
        **status,
        "repair_history": history,
        "notes": {
            "overview": note_card("Self Healing Overview", "00_Raphael/Self Healing/Self Healing Overview.md"),
            "observations": note_card("Health Observations", "00_Raphael/Self Healing/Health Observations.md"),
            "issues": note_card("Detected Issues", "00_Raphael/Self Healing/Detected Issues.md"),
            "plans": note_card("Repair Plans", "00_Raphael/Self Healing/Repair Plans.md"),
            "history": note_card("Repair History", "00_Raphael/Self Healing/Repair History.md"),
            "brief": note_card("System Reliability Brief", "00_Raphael/Self Healing/System Reliability Brief.md"),
        },
        "note_root": str(root),
    }


def self_healing_bus_action(action: str, payload: dict[str, Any]) -> tuple[dict[str, Any], int]:
    issue_id = str(payload.get("issue_id", "")).strip().upper()
    repair_id = str(payload.get("repair_id", "")).strip().upper()
    confirmation_key = str(payload.get("confirmation_key", "")).strip()
    phrases = {
        "observe": "observe system",
        "detect": "detect issues",
        "brief": "show reliability brief",
        "plan": f"repair issue {issue_id}",
        "approve": f"approve repair {repair_id}",
        "run": f"repair approved issue {repair_id}",
    }
    if action not in phrases:
        return {"ok": False, "error": f"Unsupported self-healing action: {action}"}, 400
    if action == "plan" and not issue_id:
        return {"ok": False, "error": "issue_id is required."}, 400
    if action in {"approve", "run"} and not repair_id:
        return {"ok": False, "error": "repair_id is required."}, 400
    try:
        bus_module = load_command_bus()
        bus = bus_module.RaphaelCommandBus()
        result = (
            bus.confirm(confirmation_key, SELF_HEALING_COMMAND_BUS_SESSION)
            if confirmation_key
            else bus.route(phrases[action], "dashboard_self_healing", SELF_HEALING_COMMAND_BUS_SESSION)
        )
    except Exception as exc:
        return {"ok": False, "error": str(exc)}, 500
    if result.get("status") == "needs_confirmation":
        return {
            "ok": True,
            "state": "pending_confirmation",
            "confirmation_required": True,
            "confirmation_key": result.get("confirmation_key", ""),
            "message": result.get("spoken_response", "Confirmation required."),
            "command": result.get("matched_command", ""),
        }, 202
    command_result = _parse_command_output(result)
    ok = result.get("status") == "routed"
    return {
        "ok": ok,
        "state": "action_completed" if ok else "error",
        "confirmation_required": False,
        "message": result.get("spoken_response") or result.get("full_response"),
        "error": result.get("safety_reason", "") if not ok else "",
        "result": command_result,
        "self_healing": self_healing_data(),
    }, 200 if ok else 400


def maintenance_data(health: dict[str, Any] | None = None) -> dict[str, Any]:
    settings = load_settings()
    health = health or system_health()
    config_errors: list[str] = []
    config_warnings: list[str] = []
    if str(settings.get("dashboard_host", "")) not in {"127.0.0.1", "localhost"}:
        config_errors.append("Dashboard host is not localhost-only.")
    if bool(settings.get("external_execution_enabled", False)):
        config_errors.append("External execution must remain disabled.")
    for key in ["command_bus_requires_confirmation_for_writes", "dashboard_requires_confirmation_for_actions", "execution_requires_confirmation", "docker_requires_confirmation"]:
        if not bool(settings.get(key, True)):
            config_errors.append(f"{key} must remain enabled.")
    if not vault_path().exists():
        config_warnings.append(f"Vault path is missing: {vault_path()}")
    if not runtime_path().exists():
        config_warnings.append(f"Runtime path is missing: {runtime_path()}")

    dependencies = [
        {"name": name, "available": importlib.util.find_spec(name) is not None, "required": required}
        for name, required in [
            ("fastapi", True),
            ("uvicorn", True),
            ("qdrant_client", False),
            ("sentence_transformers", False),
            ("faster_whisper", False),
            ("sounddevice", False),
        ]
    ]
    route_rows = sorted(
        {
            route.path: ",".join(sorted(getattr(route, "methods", []) or []))
            for route in app.routes
            if getattr(route, "path", "").startswith("/")
        }.items()
    )
    required_routes = {"/", "/api/overview", "/api/health", "/api/chat", "/api/employees/network", "/api/raphael/presence", "/api/maintenance"}
    route_paths = {path for path, _ in route_rows}
    missing_routes = sorted(required_routes - route_paths)
    required_files = [
        CONFIG_PATH,
        APP_DIR / "app.py",
        APP_DIR / "static" / "css" / "matrix.css",
        APP_DIR / "static" / "js" / "matrix.js",
        runtime_path() / "command_bus.py",
        runtime_path() / "voice_gateway.py",
    ]
    files = [{"path": str(path), "exists": path.exists()} for path in required_files]
    errors: list[dict[str, str]] = []
    for path in [
        DASHBOARD_CHAT_LOG,
        runtime_path() / "voice" / "logs" / "Voice Interaction Log.md",
        runtime_path() / "logs" / "Memory Retrieval Log.md",
    ]:
        text = read_text(path, 120000)
        for line in text.splitlines():
            lowered = line.lower()
            if any(term in lowered for term in ["error", "failed", "refused", "traceback", "exception", "blocked"]):
                errors.append({"source": path.name, "message": excerpt(line.strip(), 240)})
    required_dependencies_ok = all(row["available"] for row in dependencies if row["required"])
    files_ok = all(row["exists"] for row in files)
    config_ok = not config_errors
    api_ok = not missing_routes
    overall = "healthy" if config_ok and api_ok and required_dependencies_ok and files_ok else "needs_attention"
    bootstrap = bootstrap_data(health)
    service_manager = service_manager_data()
    self_healing = self_healing_data()
    return {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "overall": overall,
        "system_health": health,
        "config_health": {"ok": config_ok, "errors": config_errors, "warnings": config_warnings, "path": str(CONFIG_PATH)},
        "api_health": {"ok": api_ok, "routes": [{"path": path, "methods": methods} for path, methods in route_rows], "missing": missing_routes},
        "dependencies": {"ok": required_dependencies_ok, "records": dependencies},
        "files": {"ok": files_ok, "records": files},
        "model_status": {
            "ollama_online": health["ollama"]["ok"],
            "models": health["ollama"]["models"],
            "vision_model": health["vision"],
        },
        "qdrant_status": health["qdrant"],
        "ollama_status": health["ollama"],
        "bootstrap": bootstrap,
        "service_manager": service_manager,
        "self_healing": self_healing,
        "dashboard_chat_tests": dashboard_chat_test_status_data(),
        "voice_status": {
            **health["piper"],
            "control_enabled": health["dashboard_chat"]["voice_control_enabled"],
            "input_enabled": health["dashboard_chat"]["voice_input_enabled"],
        },
        "recent_errors": errors[-20:][::-1],
        "commands": [
            "python raphael.py system-check",
            "python raphael.py repair",
            "python raphael.py backup",
            "python raphael.py cleanup-logs",
            "python raphael.py route-check",
            "python raphael.py dependency-check",
        ],
        "helpers": [
            r"R:\RaphaelOS\scripts\start-raphael.ps1",
            r"R:\RaphaelOS\scripts\health-check.ps1",
            r"R:\RaphaelOS\scripts\restart-dashboard.ps1",
        ],
        "safety": {
            "backup_scope": "Vault and Raphael runtime files only.",
            "repair_scope": "Missing generated folders/files only.",
            "cleanup_scope": "Known Raphael logs only.",
            "project_source_edits": False,
            "external_actions": False,
        },
    }


def bootstrap_data(health: dict[str, Any] | None = None) -> dict[str, Any]:
    settings = load_settings()
    health = health or system_health()
    root = vault_path() / "00_Raphael" / "System Bootstrap"
    runtime = runtime_path() / "launcher" / "runtime"
    pid_path = runtime / "service_pids.json"
    try:
        registry = json.loads(read_text(pid_path, 20000) or '{"services":{}}')
    except json.JSONDecodeError:
        registry = {"services": {}}
    managed = []
    for name, row in registry.get("services", {}).items():
        managed.append({
            "service": name,
            "pid": row.get("pid"),
            "started": row.get("started", ""),
            "command": " ".join(str(item) for item in row.get("command", [])),
            "log": row.get("log", ""),
        })
    comfy_url = str(settings.get("pod_comfyui_url", "http://127.0.0.1:8188")).rstrip("/")
    # Translate localhost to host.docker.internal for internal server-side checks
    internal_comfy_url = comfy_url.replace("127.0.0.1", "host.docker.internal").replace("localhost", "host.docker.internal")
    comfy_ok, comfy_detail = http_json(internal_comfy_url + "/system_stats")
    def check_docker_path(p: Path) -> bool:
        if not p: return False
        s = str(p).replace("\\", "/")
        if s.lower().startswith("c:/"):
            s = "/app/c/" + s[3:]
        return Path(s).exists()

    rembg = Path(str(settings.get("pod_rembg_path", ""))) if settings.get("pod_rembg_path") else None
    upscayl = Path(str(settings.get("pod_upscayl_path", ""))) if settings.get("pod_upscayl_path") else None
    inkscape = Path(str(settings.get("pod_inkscape_path", ""))) if settings.get("pod_inkscape_path") else None
    core_ok = (runtime_path() / "command_bus.py").exists() and vault_path().exists() and runtime_path().exists()
    required_models = {
        str(settings.get("default_model", "")),
        str(settings.get("ollama_model", "")),
        str(settings.get("vision_model", "")),
    } - {""}
    available_models = [str(item) for item in health["ollama"].get("models", [])]
    missing_models = [
        model for model in required_models
        if not any(candidate == model or candidate == model.split(":")[0] or candidate.startswith(model.split(":")[0] + ":") for candidate in available_models)
    ]
    ai_ok = bool(health["ollama"]["ok"] and health["qdrant"]["ok"] and not missing_models)
    creative_ok = bool(comfy_ok and rembg and check_docker_path(rembg) and inkscape and check_docker_path(inkscape))
    voice_online = bool(settings.get("bootstrap_start_voice_gateway", False) and health["piper"]["exe_exists"] and health["piper"]["model_exists"])
    return {
        "enabled": bool(settings.get("bootstrap_enabled", True)),
        "groups": {
            "core": "Online" if core_ok else "Warning",
            "ai": "Online" if ai_ok else "Warning",
            "creative": "Online" if creative_ok else "Warning",
            "voice": "Online" if voice_online else "Off" if not settings.get("bootstrap_start_voice_gateway", False) else "Warning",
        },
        "managed_pids": managed,
        "pid_registry": str(pid_path),
        "dashboard_url": f"http://localhost:{settings.get('dashboard_port', 8787)}",
        "comfyui_url": comfy_url,
        "services": {
            "dashboard": {"ok": True, "detail": "Current dashboard process is online."},
            "command_bus": {"ok": (runtime_path() / "command_bus.py").exists()},
            "ollama": {**health["ollama"], "required_models": sorted(required_models), "missing_models": missing_models},
            "qdrant": health["qdrant"],
            "comfyui": {"ok": comfy_ok, "detail": "ok" if comfy_ok else str(comfy_detail)},
            "voice": {"ok": voice_online, **health["piper"]},
        },
        "tools": {
            "rembg": {"exists": check_docker_path(rembg), "path": str(rembg or "")},
            "upscayl": {"exists": check_docker_path(upscayl), "path": str(upscayl or "")},
            "inkscape": {"exists": check_docker_path(inkscape), "path": str(inkscape or "")},
        },
        "startup": note_card("Startup Log", "00_Raphael/System Bootstrap/Startup Log.md"),
        "recovery": note_card("Recovery Log", "00_Raphael/System Bootstrap/Recovery Log.md"),
        "health": note_card("Bootstrap Health", "00_Raphael/System Bootstrap/Bootstrap Health.md"),
        "review": note_card("Bootstrap Review", "00_Raphael/System Bootstrap/Bootstrap Review.md"),
    }


def load_voice_gateway():
    voice_path = runtime_path() / "voice_gateway.py"
    spec = importlib.util.spec_from_file_location("raphael_voice_gateway_dashboard", voice_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load voice gateway from {voice_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_command_bus():
    bus_path = runtime_path() / "command_bus.py"
    bus_dir = str(bus_path.parent)
    if bus_dir not in sys.path:
        sys.path.insert(0, bus_dir)
        
    spec = importlib.util.spec_from_file_location("raphael_command_bus_dashboard", bus_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load Command Bus from {bus_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def command_bus_data() -> dict[str, Any]:
    settings = load_settings()
    return {
        "enabled": bool(settings.get("command_bus_enabled", True)),
        "log_all": bool(settings.get("command_bus_log_all_routes", True)),
        "requires_confirmation": bool(settings.get("command_bus_requires_confirmation_for_writes", True)),
        "allow_execution": bool(settings.get("command_bus_allow_execution", True)),
        "overview": note_card("Command Bus Overview", "00_Raphael/Command Bus/Command Bus Overview.md"),
        "registry": note_card("Command Registry", "00_Raphael/Command Bus/Command Registry.md"),
        "routing_log": note_card("Command Routing Log", "00_Raphael/Command Bus/Command Routing Log.md"),
        "safety": note_card("Command Safety Policy", "00_Raphael/Command Bus/Command Safety Policy.md"),
        "review": note_card("Command Review", "00_Raphael/Command Bus/Command Review.md"),
    }


def dashboard_chat_settings() -> dict[str, bool]:
    settings = load_settings()
    return {
        "chat_enabled": bool(settings.get("dashboard_chat_enabled", True)),
        "council_chat_enabled": bool(settings.get("dashboard_council_chat_enabled", True)),
        "command_execution_enabled": bool(settings.get("dashboard_command_execution_enabled", True)),
        "voice_input_enabled": bool(settings.get("dashboard_voice_input_enabled", False)),
        "voice_control_enabled": bool(settings.get("dashboard_voice_control_enabled", True)),
        "requires_confirmation": bool(settings.get("dashboard_requires_confirmation_for_actions", True)),
        "requires_delegation_confirmation": bool(settings.get("dashboard_requires_confirmation_for_delegation", True)),
        "builder_enabled": bool(settings.get("builder_mode_enabled", True)),
        "builder_requires_confirmation": bool(settings.get("builder_requires_confirmation", True)),
        "controlled_execution_enabled": bool(settings.get("controlled_execution_enabled", True)),
        "dashboard_execution_enabled": bool(settings.get("dashboard_execution_enabled", True)),
    }


def log_dashboard_chat(phrase: str, intent: str, command: str, status: str, response: str, confirmation_required: bool) -> None:
    DASHBOARD_CHAT_LOG.parent.mkdir(parents=True, exist_ok=True)
    if not DASHBOARD_CHAT_LOG.exists():
        DASHBOARD_CHAT_LOG.write_text("# Dashboard Chat Log\n\n", encoding="utf-8")
    entry = f"""## {dt.datetime.now().isoformat(timespec='seconds')}

- Phrase: {phrase}
- Intent: {intent}
- Command: {command or 'None'}
- Confirmation required: {'Yes' if confirmation_required else 'No'}
- Status: {status}
- Response: {response}

"""
    with DASHBOARD_CHAT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(entry)


def command_display(command: list[str]) -> str:
    if not command:
        return ""
    return "python raphael.py " + " ".join(f'"{part}"' if " " in part else part for part in command)


def dashboard_route_agent_ask(phrase: str, voice_config: dict[str, Any], voice_gateway) -> Any | None:
    text = voice_gateway.normalize(phrase, str(voice_config.get("wake_word", "raphael")))
    
    agent_phrase = None
    question = None
    
    m1 = re.search(r"^ask\s+(.+? agent)\s+(?:to\s+)?(.+)$", text)
    if m1:
        agent_phrase = m1.group(1).strip()
        question = m1.group(2).strip()
        
    if not agent_phrase:
        m2 = re.search(r"^(.*?)\s+to\s+(.+? agent)$", text)
        if m2:
            question = m2.group(1).strip()
            agent_phrase = m2.group(2).strip()
            
    if not agent_phrase:
        m3 = re.search(r"^(.+? agent)\s+(.+)$", text)
        if m3:
            agent_phrase = m3.group(1).strip()
            question = m3.group(2).strip()

    if not agent_phrase or not question:
        return None
    agents = [
        "Chief of Staff Agent",
        "Research Agent",
        "Developer Agent",
        "Business Strategy Agent",
        "Marketing Agent",
        "Operations Agent",
        "Finance Agent",
        "Legal/Compliance Agent",
        "Career Agent",
        "Academic Agent",
    ]
    normalized_agent = None
    for agent in agents:
        if agent.lower() == agent_phrase or agent.lower().replace("/", " ") == agent_phrase:
            normalized_agent = agent
            break
    if not normalized_agent:
        return None
    return voice_gateway.RouteResult("agent_ask", ["agent-ask", normalized_agent, question], False, f"Asking {normalized_agent}.")


def execute_dashboard_route(voice_gateway, route: Any, phrase: str, voice_config: dict[str, Any], confirmed: bool = False) -> dict[str, Any]:
    settings = dashboard_chat_settings()
    confirmation_required = bool(route.confirmation_required and voice_config.get("require_confirmation_for_execution", True) and settings["requires_confirmation"])
    if route.command and route.command[0] == "delegate-task" and settings["requires_delegation_confirmation"]:
        confirmation_required = True
    council_commands = {"list-councils", "council-status", "council-brief", "council-review", "council-debate", "delegate-task", "executive-summary", "council-task-review"}
    if route.command and route.command[0] in council_commands and not settings["council_chat_enabled"]:
        response = "Dashboard council chat is disabled in config/settings.json."
        log_dashboard_chat(phrase, route.intent, command_display(route.command), "Disabled", response, confirmation_required)
        return {
            "response": response,
            "intent": route.intent,
            "command": command_display(route.command),
            "status": "Disabled",
            "confirmation_required": confirmation_required,
            "awaiting_confirmation": False,
        }
    if route.command and route.command[0].startswith("execution-") and (not settings["controlled_execution_enabled"] or not settings["dashboard_execution_enabled"]):
        response = "Dashboard controlled execution is disabled in config/settings.json."
        log_dashboard_chat(phrase, route.intent, command_display(route.command), "Disabled", response, confirmation_required)
        return {
            "response": response,
            "intent": route.intent,
            "command": command_display(route.command),
            "status": "Disabled",
            "confirmation_required": confirmation_required,
            "awaiting_confirmation": False,
        }
    if route.refused:
        response = route.response
        log_dashboard_chat(phrase, route.intent, command_display(route.command), "Refused", response, confirmation_required)
        return {
            "response": response,
            "intent": route.intent,
            "command": command_display(route.command),
            "status": "Refused",
            "confirmation_required": confirmation_required,
            "awaiting_confirmation": False,
        }
    if confirmation_required and not confirmed:
        PENDING_CHAT_ROUTE["route"] = route
        PENDING_CHAT_ROUTE["phrase"] = phrase
        response = route.response
        log_dashboard_chat(phrase, route.intent, command_display(route.command), "Confirmation Required", response, True)
        return {
            "response": response,
            "intent": route.intent,
            "command": command_display(route.command),
            "status": "Confirmation Required",
            "confirmation_required": True,
            "awaiting_confirmation": True,
        }
    if not route.command:
        response = route.response
        log_dashboard_chat(phrase, route.intent, "", "No Command", response, confirmation_required)
        return {
            "response": response,
            "intent": route.intent,
            "command": "",
            "status": "No Command",
            "confirmation_required": confirmation_required,
            "awaiting_confirmation": False,
        }
    if not settings["command_execution_enabled"]:
        response = "Dashboard command execution is disabled. I detected a safe command, but did not run it."
        log_dashboard_chat(phrase, route.intent, command_display(route.command), "Disabled", response, confirmation_required)
        return {
            "response": response,
            "intent": route.intent,
            "command": command_display(route.command),
            "status": "Disabled",
            "confirmation_required": confirmation_required,
            "awaiting_confirmation": False,
        }
    try:
        result = voice_gateway.run_raphael(route.command, confirmed=confirmed)
        response = voice_gateway.summarize_response(result, voice_config)
        status = "Success" if result.returncode == 0 else "Failed"
    except Exception as exc:
        response = f"Refused or failed safely: {exc}"
        status = "Refused"
    log_dashboard_chat(phrase, route.intent, command_display(route.command), status, response, confirmation_required)
    return {
        "response": response,
        "intent": route.intent,
        "command": command_display(route.command),
        "status": status,
        "confirmation_required": confirmation_required,
        "awaiting_confirmation": False,
    }


def _dashboard_chat_test_completed(args: list[str], state: dict[str, Any]) -> subprocess.CompletedProcess[str]:
    command = args[0] if args else ""
    scenario = str(state.get("_test_scenario", ""))
    workflow_id = str(state.get("_test_workflow_id", "PODFLOW-SMOKE-0001"))
    if command == "pod-workflow":
        stage = 5 if scenario == "comfyui_offline" else 1
        next_stage = 6 if stage == 5 else 3
        state["_test_workflow_stage"] = stage
        state["_test_workflow_status"] = "awaiting_confirmation"
        payload = {
            "workflow_id": workflow_id,
            "status": "awaiting_confirmation",
            "completed_stage": stage,
            "stage_count": 13,
            "next_stage_number": next_stage,
            "next_stage": "generate images" if next_stage == 6 else "create concept",
            "message": f"POD workflow started. Stage {stage}/13 complete. Say confirm to continue.",
            "ids": {},
            "outputs": {},
        }
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps(payload), stderr="")
    if command == "pod-workflow-continue":
        stage = int(state.get("_test_workflow_stage", 1))
        if scenario == "comfyui_offline" and stage == 5 and not state.get("_test_comfyui_online"):
            state["_test_workflow_status"] = "awaiting_service"
            return subprocess.CompletedProcess(
                args,
                1,
                stdout="",
                stderr="ComfyUI readiness check failed: connection refused. Expected checkpoint: SDXL Base.",
            )
        completed = min(13, stage + 1)
        state["_test_workflow_stage"] = completed
        state["_test_workflow_status"] = "completed" if completed >= 13 else "awaiting_confirmation"
        payload = {
            "workflow_id": workflow_id,
            "status": state["_test_workflow_status"],
            "completed_stage": completed,
            "stage_count": 13,
            "next_stage_number": min(14, completed + 1),
            "next_stage": "next simulated stage",
            "message": f"POD workflow stage {completed}/13 complete.",
            "ids": {},
            "outputs": {},
        }
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps(payload), stderr="")
    if args[:2] == ["service-start", "comfyui"]:
        state["_test_comfyui_online"] = True
        state["_test_workflow_status"] = "awaiting_confirmation"
        payload = {"action": "start", "results": [{"service_id": "comfyui", "result": "started", "pid": 63001}]}
        return subprocess.CompletedProcess(args, 0, stdout=json.dumps(payload), stderr="")
    return subprocess.CompletedProcess(args, 0, stdout=json.dumps({"dry_run": True, "command": args}), stderr="")


def dashboard_chat_response(
    phrase: str,
    *,
    test_mode: bool = False,
    test_session_id: str = "",
    reset_test_session: bool = False,
    test_scenario: str = "",
) -> dict[str, Any]:
    settings = dashboard_chat_settings()
    if not settings["chat_enabled"]:
        return {
            "response": "Dashboard chat is disabled in config/settings.json.",
            "intent": "disabled",
            "command": "",
            "status": "Disabled",
            "confirmation_required": False,
            "awaiting_confirmation": False,
        }
    try:
        from raphael_core.operator.chat_controller import chat_controller
        session_id = re.sub(r"[^A-Za-z0-9_-]", "", test_session_id)[:80] or "default"
        
        # Intercept via new OS Router
        router_result = chat_controller.process_message(session_id, phrase)
        if router_result.get("response"):
            # The Router handled it, return immediately
            
            # If the intent is execute, spawn the background runner + D13-A hooks
            if router_result.get("intent") == "execute":
                workflow_id = router_result.get("command")
                exec_id = f"EX-{__import__('datetime').datetime.utcnow().strftime('%Y%m%d')}-{__import__('uuid').uuid4().hex[:4].upper()}"
                repo_dir = str(REPO_DIR)
                if workflow_id:
                    import subprocess
                    subprocess.Popen(["python", "raphael.py", "workflow-execute", workflow_id], cwd=repo_dir)
                    
                    # D13-A: Emit WORKFLOW_STARTED event to the Event Fabric
                    try:
                        import sys
                        if repo_dir not in sys.path:
                            sys.path.insert(0, str(REPO_DIR))
                        from raphael_core.events import event_bus, EventType
                        mission_id = router_result.get("_mission_id", "")
                        event_bus.publish(
                            EventType.WORKFLOW_STARTED,
                            payload={"workflow_id": workflow_id},
                            mission_id=mission_id,
                            execution_id=exec_id,
                            actor="user",
                            source="legacy_adapter",
                        )
                    except Exception as _evt_exc:
                        pass  # Event emission is non-critical

                    # D13-A: Create Initiative + Tasks via Initiative Manager
                    try:
                        from raphael_core.operator.initiative_manager import initiative_manager
                        initiative_manager.create_from_execution(
                            mission_id=router_result.get("_mission_id", ""),
                            execution_id=exec_id,
                            workflow_id=workflow_id,
                            workflow_name=router_result.get("command", workflow_id),
                            objective=router_result.get("response", "Workflow execution"),
                        )
                    except Exception as _init_exc:
                        pass  # Initiative creation is non-critical
                    
                    # Patch exec_id into response for UI display
                    router_result["_execution_id"] = exec_id

            log_dashboard_chat(phrase, router_result.get("intent", ""), router_result.get("command", ""), router_result.get("status", ""), router_result.get("response", ""), router_result.get("confirmation_required", False))
            return router_result


        # If empty response, fallback to legacy CommandBus
        bus_module = load_command_bus()
        bus = bus_module.RaphaelCommandBus()
        if test_mode:
            with DASHBOARD_CHAT_TEST_LOCK:
                if reset_test_session:
                    DASHBOARD_CHAT_TEST_SESSIONS.pop(session_id, None)
                session = DASHBOARD_CHAT_TEST_SESSIONS.setdefault(session_id, {})
                if test_scenario:
                    session["_test_scenario"] = test_scenario
                bus.voice_gateway.run_raphael = lambda args, confirmed=False: _dashboard_chat_test_completed(list(args), session)
                result = bus.route(phrase, "dashboard_test", session)
                test_state = {
                    "session_id": session_id,
                    "workflow_stage": int(session.get("_test_workflow_stage", 0) or 0),
                    "workflow_status": str(session.get("_test_workflow_status", "")),
                    "comfyui_online": bool(session.get("_test_comfyui_online", False)),
                    "pending_command": str((session.get("pending_command_bus_route") or {}).get("matched_command", "")),
                    "pending_confirmation": bool(session.get("pending_command_bus_route")),
                }
        else:
            with DASHBOARD_CHAT_TEST_LOCK:
                result = bus.route(phrase, "dashboard", COMMAND_BUS_SESSION)
            test_state = {}
        response = result.get("full_response") or result.get("spoken_response") or ""
        command = result.get("matched_command") or ""
        status_map = {
            "routed": "Success",
            "needs_confirmation": "Confirmation Required",
            "blocked": "Refused",
            "general_answer": "Success",
            "error": "Failed",
        }
        status = status_map.get(str(result.get("status", "")), str(result.get("status", "Unknown")).title())
        log_dashboard_chat(phrase, str(result.get("intent", "")), str(command), status, str(response), bool(result.get("requires_confirmation", False)))
        return {
            "response": response,
            "intent": result.get("intent", ""),
            "command": command,
            "status": status,
            "confirmation_required": bool(result.get("requires_confirmation", False)),
            "awaiting_confirmation": result.get("status") == "needs_confirmation",
            "raw_status": result.get("status", ""),
            "command_type": result.get("command_type", ""),
            "cli_args": result.get("cli_args", []),
            "confirmation_key": result.get("confirmation_key", ""),
            "test_mode": test_mode,
            "test_state": test_state,
        }
    except Exception as exc:
        response = f"Command Bus failed safely. No fallback route was used: {exc}"
        log_dashboard_chat(phrase, "command_bus_error", "", "Failed", response, False)
        return {
            "response": response,
            "intent": "command_bus_error",
            "command": "",
            "status": "Failed",
            "confirmation_required": False,
            "awaiting_confirmation": False,
        }


def latest_notes() -> list[dict[str, Any]]:
    return [
        note_card("Daily Command Center", "00_Raphael/Daily Command Center.md"),
        note_card("Priority Brief", "00_Raphael/Priority Brief.md"),
        note_card("Goal Review", "00_Raphael/Goal Review.md"),
        note_card("Task Review", "00_Raphael/Task Review.md"),
        note_card("Agent Review", "00_Raphael/Agent Review.md"),
        note_card("Workflow Review", "00_Raphael/Workflow Review.md"),
        note_card("Action Review", "00_Raphael/Action Review.md"),
        note_card("Inbox Review", "00_Raphael/Inbox Review.md"),
        note_card("Vision Review", "04_Research/Vision Analysis/Vision Review.md"),
        note_card("Search Review", "04_Research/Web Search Results/Search Review.md"),
    ]


def knowledge_data() -> dict[str, Any]:
    root = vault_path() / "09_Knowledge"
    categories = ["Academic", "Programming", "Research", "Portfolio", "Business", "Lessons Learned"]
    summaries: list[dict[str, Any]] = []
    for category in categories:
        folder = root / category
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md"), key=lambda value: value.stat().st_mtime, reverse=True):
            text = read_text(path)
            detected_title = section_value(text, "Title")
            if not detected_title or detected_title.startswith("#"):
                detected_title = re.sub(r"\s+-\s+[a-f0-9]{10}$", "", path.stem, flags=re.I)
            summaries.append({
                "id": section_value(text, "Knowledge ID") or "",
                "title": detected_title,
                "suggested_title": section_value(text, "Suggested Title") or detected_title,
                "category": section_value(text, "Category") or category,
                "course": section_value(text, "Course") or "Not detected",
                "project_type": section_value(text, "Project Type") or "",
                "status": section_value(text, "Assignment/Project Status") or "",
                "ignored": section_value(text, "Ignored") == "Yes",
                "portfolio_score": section_value(text, "Portfolio Score") or "",
                "portfolio_value": section_value(text, "Portfolio Value").split("—", 1)[0].strip(),
                "source": section_value(text, "Source Path Reference").strip().strip("`"),
                "path": str(path),
                "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
            })
    inventories = sorted((root / "Inventories").glob("*.md"), key=lambda value: value.stat().st_mtime, reverse=True) if (root / "Inventories").exists() else []
    reviews = sorted(root.glob("*Knowledge Review.md"), key=lambda value: value.stat().st_mtime, reverse=True) if root.exists() else []
    return {
        "root": str(root),
        "exists": root.exists(),
        "summaries": summaries,
        "inventories": [{"name": path.stem, "path": str(path), "updated": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")} for path in inventories],
        "review": note_card("Knowledge Review", str(reviews[0].relative_to(vault_path()))) if reviews else {"exists": False, "content": "", "path": ""},
        "curation_review": note_card("Knowledge Curation Review", "09_Knowledge/Curation/Knowledge Curation Review.md"),
        "rename_suggestions": note_card("Knowledge Rename Suggestions", "09_Knowledge/Curation/Knowledge Rename Suggestions.md"),
        "skills_map": note_card("Knowledge Skills Map", "09_Knowledge/Curation/Knowledge Skills Map.md"),
        "portfolio_candidates": note_card("Portfolio Candidate Ranking", "09_Knowledge/Curation/Portfolio Candidate Ranking.md"),
        "ignored_items": note_card("Ignored Knowledge Items", "09_Knowledge/Curation/Ignored Knowledge Items.md"),
        "safety": {
            "source_access": "read-only",
            "source_copies": "disabled",
            "raw_indexing": "disabled",
            "credential_indexing": "disabled",
            "external_uploads": "disabled",
        },
    }


def knowledge_relationship_data() -> dict[str, Any]:
    root = vault_path() / "09_Knowledge" / "Relationships"
    graph_text = read_text(root / "Knowledge Graph.md")
    def metric(label: str) -> int:
        match = re.search(rf"- {re.escape(label)}:\s*(\d+)", graph_text)
        return int(match.group(1)) if match else 0
    return {
        "root": str(root),
        "nodes": metric("Total nodes"),
        "relationships": metric("Total relationships"),
        "items": metric("Knowledge items"),
        "graph": note_card("Knowledge Graph", "09_Knowledge/Relationships/Knowledge Graph.md"),
        "clusters": note_card("Knowledge Clusters", "09_Knowledge/Relationships/Knowledge Clusters.md"),
        "career": note_card("Career Map", "09_Knowledge/Relationships/Career Map.md"),
        "business": note_card("Business Map", "09_Knowledge/Relationships/Business Map.md"),
        "portfolio": note_card("Portfolio Map", "09_Knowledge/Relationships/Portfolio Map.md"),
        "technology": note_card("Technology Map", "09_Knowledge/Relationships/Technology Map.md"),
        "skills": note_card("Skills Map", "09_Knowledge/Relationships/Skills Map.md"),
        "review": note_card("Relationship Review", "09_Knowledge/Relationships/Relationship Review.md"),
    }


def communication_file_records(filename: str, prefix: str) -> list[dict[str, str]]:
    path = vault_path() / "00_Raphael" / "Inter-Council Communications" / filename
    text = read_text(path, 300000)
    rows: list[dict[str, str]] = []
    pattern = rf"^## ({re.escape(prefix)}-\d{{8}}-[A-F0-9]+)\s*\n(.*?)(?=^## {re.escape(prefix)}-|\Z)"
    for match in re.finditer(pattern, text, flags=re.M | re.S):
        body = match.group(2)
        row = {"id": match.group(1)}
        for heading in [
            "From Council", "To Council", "Topic", "Question", "Request Type", "Status",
            "Created", "Updated", "Request ID", "Response Type", "Response", "Supporting Evidence",
            "Risks", "Opportunities", "Dependencies", "Related KPIs", "Related Initiatives",
            "Related Goals", "Related Knowledge Items", "Recommendation", "Confidence Score",
            "Reason", "Council Opinions", "Executive Recommendation",
        ]:
            row[heading.lower().replace(" ", "_")] = subsection_value(body, heading)
        rows.append(row)
    return rows


def communication_data() -> dict[str, Any]:
    root = vault_path() / "00_Raphael" / "Inter-Council Communications"
    requests = communication_file_records("Council Requests.md", "COMM")
    responses = communication_file_records("Council Responses.md", "RESP")
    recommendations = communication_file_records("Council Recommendations.md", "REC")
    escalations = communication_file_records("Council Escalations.md", "ESC")
    syntheses = communication_file_records("Executive Syntheses.md", "SYN")
    return {
        "root": str(root),
        "requests": requests,
        "open_requests": [row for row in requests if row.get("status") == "Open"],
        "responses": responses,
        "recommendations": recommendations,
        "escalations": escalations,
        "syntheses": syntheses,
        "network": note_card("Communication Network", "00_Raphael/Inter-Council Communications/Communication Network Overview.md"),
        "review": note_card("Communication Review", "00_Raphael/Inter-Council Communications/Communication Review.md"),
        "brief": note_card("Communication Brief", "00_Raphael/Inter-Council Communications/Communication Brief.md"),
        "history": note_card("Communication History", "00_Raphael/Inter-Council Communications/Communication History.md"),
        "safety": {
            "execution": "disabled",
            "external_messages": "disabled",
            "autonomous_decisions": "disabled",
            "approval_bypass": "disabled",
        },
    }


def overview() -> dict[str, Any]:
    task_items = tasks()
    project_items = projects()
    goal_items = goals()
    vision_items = vision_requests()
    search_items = search_requests()
    internet_access = internet_access_data()
    workflow_items = workflow_requests()
    world = world_model_data()
    simulation = simulation_data()
    opportunity = opportunity_data()
    allocation = resource_allocation_data()
    blueprints = blueprint_data()
    commerce = commerce_data()
    pod_studio = pod_design_studio_data()
    asset_library = asset_brand_library_data()
    agency = agency_data()
    creator = creator_data()
    kpis = kpi_data()
    finance = finance_data()
    portfolio = portfolio_data()
    command_bus = command_bus_data()
    notifications = notification_data()
    briefs = executive_brief_data()
    daily_operating = daily_operating_data()
    activity = activity_data()
    initiatives = initiative_data()
    employees = employee_data()
    controlled_execution = controlled_execution_data()
    knowledge = knowledge_data()
    knowledge_relationships = knowledge_relationship_data()
    communications = communication_data()
    goal_propagation = goal_propagation_data()
    deliberations = deliberation_data()
    execution_plans = execution_plan_data()
    n8n_studio = n8n_workflow_studio_data()
    workflow_runner = workflow_runner_data()
    self_healing = self_healing_data()
    council_status = council_status_data()
    council_activity = council_activity_data()
    matrix_departments = matrix_department_data()
    council_chambers = council_chamber_data()
    employee_network = employee_network_data()
    health = system_health()
    maintenance = maintenance_data(health)
    presence = raphael_presence_data(
        notifications=notifications,
        briefs=briefs,
        portfolio=portfolio,
        initiatives=initiatives,
        execution=controlled_execution,
        kpis=kpis,
        council_status=council_status,
        activity=activity,
    )
    return {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "mode": current_mode(),
        "counts": {
            "projects": len(project_items),
            "goals_active": sum(1 for item in goal_items if item["status"] == "Active"),
            "tasks_open": sum(1 for item in task_items if item["status"] not in {"Done", "Archived"}),
            "tasks_blocked": sum(1 for item in task_items if item["status"] == "Blocked"),
            "agents": len(agents()),
            "workflow_pending": sum(1 for item in workflow_items if "pending" in item["status"].lower()),
            "vision_pending": sum(1 for item in vision_items if item["status"].lower() == "pending"),
            "search_pending": sum(1 for item in search_items if item["status"].lower() == "pending"),
            "businesses": len(world["records"]["business"]),
            "products": len(world["records"]["product"]),
            "simulations": len(simulation["results"]),
            "opportunities": len(opportunity["records"]),
            "commerce_products": len(commerce["pod_ideas"]) + len(commerce["digital_products"]),
            "pod_concepts": len(pod_studio["concepts"]),
            "brands": len(asset_library["brands"]),
            "creative_assets": len(asset_library["assets"]),
            "agency_services": len(agency["service_offers"]),
            "creator_items": len(creator["content_ideas"]) + len(creator["ebooks"]) + len(creator["offers"]),
            "kpis": len(kpis["records"]),
            "finance_entries": len(finance["records"]),
            "portfolio_lines": len(portfolio["records"]),
            "command_bus_enabled": 1 if command_bus["enabled"] else 0,
            "notifications": len(notifications["records"]),
            "notifications_critical_high": notifications["critical_high_count"],
            "executive_brief_engine": 1 if briefs["enabled"] else 0,
            "activity_today": activity["summary"]["today"],
            "activity_high": activity["summary"]["high_events"],
            "activity_critical": activity["summary"]["critical_events"],
            "initiatives": len(initiatives["records"]),
            "high_initiatives": sum(1 for item in initiatives["records"] if item.get("priority") in {"Critical", "High"}),
            "employees": len(employees["records"]),
            "overloaded_employees": sum(1 for item in employees["records"] if item.get("workload") == "Overloaded"),
            "execution_pending": sum(1 for item in controlled_execution["records"] if item.get("status") == "Pending"),
            "execution_approved": sum(1 for item in controlled_execution["records"] if item.get("status") == "Approved"),
            "knowledge_summaries": len(knowledge["summaries"]),
            "knowledge_inventories": len(knowledge["inventories"]),
            "communication_open_requests": len(communications["open_requests"]),
            "communication_recommendations": len(communications["recommendations"]),
            "goal_cascade_plans": len(goal_propagation["plans"]),
            "deliberations": len(deliberations["records"]),
            "execution_plans": len(execution_plans["records"]),
            "n8n_workflows": len(n8n_studio["records"]),
            "workflow_runner_active": len(workflow_runner["active"]),
            "workflow_runner_failed": len(workflow_runner["failed"]),
        },
        "notes": latest_notes(),
        "projects": project_items,
        "goals": goal_items,
        "tasks": task_items,
        "agents": agents(),
        "councils": councils(),
        "council_status": council_status,
        "council_activity": council_activity,
        "matrix_departments": matrix_departments,
        "council_chambers": council_chambers,
        "employee_network": employee_network,
        "raphael_presence": presence,
        "maintenance": maintenance,
        "council_tasks": council_task_entries(),
        "council_debates": council_debates(),
        "build_requests": build_requests(),
        "identity": identity_data(),
        "world_model": world,
        "simulations": simulation,
        "opportunities": opportunity,
        "allocation": allocation,
        "blueprints": blueprints,
        "commerce": commerce,
        "pod_design_studio": pod_studio,
        "asset_brand_library": asset_library,
        "agency": agency,
        "creator": creator,
        "kpis": kpis,
        "finance": finance,
        "portfolio": portfolio,
        "command_bus": command_bus,
        "notifications": notifications,
        "briefs": briefs,
        "daily_operating": daily_operating,
        "activity": activity,
        "initiatives": initiatives,
        "employees": employees,
        "controlled_execution": controlled_execution,
        "knowledge": knowledge,
        "knowledge_relationships": knowledge_relationships,
        "communications": communications,
        "goal_propagation": goal_propagation,
        "deliberations": deliberations,
        "execution_plans": execution_plans,
        "n8n_workflow_studio": n8n_studio,
        "workflow_runner": workflow_runner,
        "self_healing": self_healing,
        "workflows": workflow_items,
        "actions": action_requests(),
        "vision_requests": vision_items,
        "search_requests": search_items,
        "internet_access": internet_access,
        "health": health,
        "commands": {
            "refresh_command_center": "python raphael.py command-center",
            "prioritize": "python raphael.py prioritize",
            "vision_review": "python raphael.py vision-review",
            "search_review": "python raphael.py search-review",
            "internet_status": "python raphael.py internet-status",
            "internet_request": "python raphael.py internet-request \"question\"",
            "internet_search": "python raphael.py internet-search \"question\"",
            "internet_review": "python raphael.py internet-review",
            "internet_brief": "python raphael.py internet-brief",
            "internet_source_review": "python raphael.py internet-source-review \"https://example.com\"",
            "memory_search": "python raphael.py memory-search \"your query\"",
            "knowledge_status": "python raphael.py knowledge-status",
            "knowledge_scan": "python raphael.py knowledge-scan \"K:\\\\School\"",
            "knowledge_inventory": "python raphael.py knowledge-inventory \"K:\\\\School\"",
            "knowledge_import": "python raphael.py knowledge-import \"K:\\\\School\"",
            "knowledge_summarize": "python raphael.py knowledge-summarize",
            "knowledge_index": "python raphael.py knowledge-index",
            "knowledge_review": "python raphael.py knowledge-review",
            "knowledge_search": "python raphael.py knowledge-search \"compiler project\"",
            "knowledge_classify": "python raphael.py knowledge-classify",
            "knowledge_curation_review": "python raphael.py knowledge-curation-review",
            "knowledge_rename_suggestion": "python raphael.py knowledge-rename-suggestion",
            "knowledge_portfolio_candidates": "python raphael.py knowledge-portfolio-candidates",
            "knowledge_skills_map": "python raphael.py knowledge-skills-map",
            "knowledge_ignore": "python raphael.py knowledge-ignore \"KNOW-ID\"",
            "knowledge_set_course": "python raphael.py knowledge-set-course \"KNOW-ID\" \"CSC4103\"",
            "knowledge_relationships": "python raphael.py knowledge-relationships",
            "knowledge_graph": "python raphael.py knowledge-graph",
            "knowledge_related": "python raphael.py knowledge-related \"KNOW-ID\"",
            "knowledge_path": "python raphael.py knowledge-path \"KNOW-ID-A\" \"KNOW-ID-B\"",
            "knowledge_clusters": "python raphael.py knowledge-clusters",
            "knowledge_career_map": "python raphael.py knowledge-career-map",
            "knowledge_business_map": "python raphael.py knowledge-business-map",
            "knowledge_portfolio_map": "python raphael.py knowledge-portfolio-map",
            "knowledge_tech_map": "python raphael.py knowledge-tech-map",
            "knowledge_skill_map": "python raphael.py knowledge-skill-map",
            "communication_status": "python raphael.py communication-status",
            "communication_review": "python raphael.py communication-review",
            "communication_history": "python raphael.py communication-history",
            "communication_request": "python raphael.py communication-request \"Executive Council\" \"Financial Council\" \"Is Agency expansion financially justified?\"",
            "communication_respond": "python raphael.py communication-respond \"COMM-ID\"",
            "communication_recommend": "python raphael.py communication-recommend \"Agency Expansion\"",
            "communication_escalate": "python raphael.py communication-escalate \"COMM-ID\"",
            "communication_synthesize": "python raphael.py communication-synthesize \"Agency Expansion\"",
            "communication_network": "python raphael.py communication-network",
            "communication_brief": "python raphael.py communication-brief",
            "goal_propagation_status": "python raphael.py goal-propagation-status",
            "propagate_goal": "python raphael.py propagate-goal \"GOAL-ID or Goal Title\"",
            "goal_cascade": "python raphael.py goal-cascade \"GOAL-ID\"",
            "goal_objectives": "python raphael.py goal-objectives \"GOAL-ID\"",
            "goal_kpi_map": "python raphael.py goal-kpi-map \"GOAL-ID\"",
            "goal_initiative_map": "python raphael.py goal-initiative-map \"GOAL-ID\"",
            "goal_review_cycle": "python raphael.py goal-review-cycle \"GOAL-ID\"",
            "goal_propagation_review": "python raphael.py goal-propagation-review",
            "goal_propagation_brief": "python raphael.py goal-propagation-brief",
            "deliberate": "python raphael.py deliberate \"Should I focus on Agency or Commerce?\"",
            "deliberation_status": "python raphael.py deliberation-status",
            "deliberation_review": "python raphael.py deliberation-review",
            "deliberation_brief": "python raphael.py deliberation-brief",
            "deliberation_history": "python raphael.py deliberation-history",
            "deliberation_show": "python raphael.py deliberation-show \"DELIB-ID\"",
            "execution_plan": "python raphael.py execution-plan \"Topic\"",
            "execution_plan_from_deliberation": "python raphael.py execution-plan-from-deliberation \"DELIB-ID\"",
            "execution_plan_review": "python raphael.py execution-plan-review",
            "execution_plan_brief": "python raphael.py execution-plan-brief",
            "execution_plan_history": "python raphael.py execution-plan-history",
            "execution_plan_show": "python raphael.py execution-plan-show \"PLAN-ID\"",
            "n8n_status": "python raphael.py n8n-status",
            "n8n_workflow_plan": "python raphael.py n8n-workflow-plan \"Workflow Idea\"",
            "n8n_workflow_generate": "python raphael.py n8n-workflow-generate \"Workflow Idea\"",
            "n8n_workflow_review": "python raphael.py n8n-workflow-review",
            "n8n_workflow_brief": "python raphael.py n8n-workflow-brief",
            "n8n_workflow_show": "python raphael.py n8n-workflow-show \"WORKFLOW-ID\"",
            "n8n_workflow_export": "python raphael.py n8n-workflow-export \"WORKFLOW-ID\"",
            "n8n_workflow_catalog": "python raphael.py n8n-workflow-catalog",
            "n8n_workflow_graph": "python raphael.py n8n-workflow-graph",
            "n8n_workflow_import_archive": "python raphael.py n8n-workflow-import-archive \"K:\\\\n8n-workflows-main\\\\n8n-workflows-main\\\\workflows\"",
            "workflow_archive_show": "python raphael.py workflow-archive-show \"WFARCH-ID\"",
            "workflow_archive_search": "python raphael.py workflow-archive-search \"query\"",
            "workflow_archive_summary": "python raphael.py workflow-archive-summary \"WFARCH-ID\"",
            "workflow_runner_status": "python raphael.py workflow-runner-status",
            "workflow_list": "python raphael.py workflow-list",
            "workflow_show": "python raphael.py workflow-show \"WORKFLOW-ID\"",
            "workflow_execute": "python raphael.py workflow-execute \"WORKFLOW-ID\"",
            "workflow_monitor": "python raphael.py workflow-monitor \"EXEC-ID\"",
            "workflow_result": "python raphael.py workflow-result \"EXEC-ID\"",
            "workflow_failures": "python raphael.py workflow-failures",
            "workflow_cancel": "python raphael.py workflow-cancel \"EXEC-ID\"",
            "workflow_runner_review": "python raphael.py workflow-review",
            "list_councils": "python raphael.py list-councils",
            "council_status": "python raphael.py council-status",
            "council_debate": "python raphael.py council-debate \"Build MentorMap MVP\"",
            "build_review": "python raphael.py build-review",
            "build_request": "python raphael.py build-request \"Build a Python app that tracks button clicks\"",
            "build_classify": "python raphael.py build-classify \"Build request\"",
            "build_with_council": "python raphael.py build-with-council \"Build request\"",
            "build_council_plan": "python raphael.py build-council-plan \"BUILD-ID\"",
            "build_task_link": "python raphael.py build-task-link \"BUILD-ID\"",
            "build_task_review": "python raphael.py build-task-review",
            "build_complete": "python raphael.py build-complete \"BUILD-ID\"",
            "builder_governance_review": "python raphael.py builder-governance-review",
            "identity_status": "python raphael.py identity-status",
            "identity_review": "python raphael.py identity-review",
            "identity_brief": "python raphael.py identity-brief",
            "world_status": "python raphael.py world-status",
            "world_review": "python raphael.py world-review",
            "world_brief": "python raphael.py world-brief",
            "add_business": "python raphael.py add-business \"Business Name\" \"Description\"",
            "add_product": "python raphael.py add-product \"Product Name\" \"Business Name\" \"Description\"",
            "simulation_status": "python raphael.py simulation-status",
            "simulate": "python raphael.py simulate \"Etsy Store\" \"Agency\"",
            "simulate_many": "python raphael.py simulate-many \"AI Influencer\" \"Etsy Store\" \"Shopify Agency\"",
            "simulate_business": "python raphael.py simulate-business \"Print on Demand Store\"",
            "compare_opportunities": "python raphael.py compare-opportunities",
            "simulation_review": "python raphael.py simulation-review",
            "opportunity_status": "python raphael.py opportunity-status",
            "detect_opportunities": "python raphael.py detect-opportunities",
            "opportunity_review": "python raphael.py opportunity-review",
            "opportunity_brief": "python raphael.py opportunity-brief",
            "add_opportunity": "python raphael.py add-opportunity \"Title\" \"Description\"",
            "score_opportunity": "python raphael.py score-opportunity \"OPPORTUNITY-ID\"",
            "opportunity_delegate": "python raphael.py opportunity-delegate \"OPPORTUNITY-ID\" \"Business Council\"",
            "resource_status": "python raphael.py resource-status",
            "set_resource_profile": "python raphael.py set-resource-profile \"15\" \"0\" \"5\"",
            "allocation_plan": "python raphael.py allocation-plan",
            "allocation_plan_for": "python raphael.py allocation-plan-for \"Goal or Opportunity\"",
            "allocation_review": "python raphael.py allocation-review",
            "allocation_brief": "python raphael.py allocation-brief",
            "allocate_next_hours": "python raphael.py allocate-next-hours \"10\"",
            "blueprint_status": "python raphael.py blueprint-status",
            "blueprint_business": "python raphael.py blueprint-business \"Business Idea\"",
            "blueprint_review": "python raphael.py blueprint-review",
            "blueprint_next_actions": "python raphael.py blueprint-next-actions \"BLUEPRINT-ID\"",
            "blueprint_delegate": "python raphael.py blueprint-delegate \"BLUEPRINT-ID\" \"Business Council\"",
            "commerce_status": "python raphael.py commerce-status",
            "commerce_review": "python raphael.py commerce-review",
            "commerce_brief": "python raphael.py commerce-brief",
            "commerce_product_idea": "python raphael.py commerce-product-idea \"Bible verse shirt\"",
            "commerce_listing_plan": "python raphael.py commerce-listing-plan \"Bible verse shirt\"",
            "commerce_store_plan": "python raphael.py commerce-store-plan \"Print on demand Etsy store\"",
            "commerce_digital_product": "python raphael.py commerce-digital-product \"AI prompt ebook\"",
            "commerce_pipeline": "python raphael.py commerce-pipeline",
            "commerce_delegate": "python raphael.py commerce-delegate \"research Etsy niches\" \"Product Researcher Agent\"",
            "pod_status": "python raphael.py pod-status",
            "pod_tool_status": "python raphael.py pod-tool-status",
            "pod_comfyui_test": "python raphael.py pod-comfyui-test",
            "pod_generation_log": "python raphael.py pod-generation-log \"PODGEN-ID\"",
            "pod_generation_debug": "python raphael.py pod-generation-debug \"PODGEN-ID\"",
            "searxng_status": "python raphael.py searxng-status",
            "searxng_start": "python raphael.py searxng-start",
            "internet_headless_search": "python raphael.py internet-headless-search \"query\"",
            "internet_overview": "python raphael.py internet-overview \"REQUEST-ID\"",
            "internet_snippets": "python raphael.py internet-snippets \"REQUEST-ID\"",
            "internet_latest_overview": "python raphael.py internet-latest-overview",
            "internet_latest_snippets": "python raphael.py internet-latest-snippets",
            "internet_raw_json": "python raphael.py internet-raw-json \"REQUEST-ID\"",
            "internet_analyze_results": "python raphael.py internet-analyze-results \"REQUEST-ID\"",
            "internet_niche_score": "python raphael.py internet-niche-score \"REQUEST-ID\"",
            "pandas_status": "python raphael.py pandas-status",
            "pandas_analyze_csv": "python raphael.py pandas-analyze-csv \"CSV-PATH\"",
            "pod_typography_create": "python raphael.py pod-typography-create \"LAND OF THE FREE\"",
            "pod_compose_design": "python raphael.py pod-compose-design \"IMAGE-PATH\" \"PODTYPE-ID\"",
            "pod_svg_export": "python raphael.py pod-svg-export \"PODCOMP-ID\"",
            "pod_print_export": "python raphael.py pod-print-export \"PODCOMP-ID\"",
            "pod_typography_review": "python raphael.py pod-typography-review",
            "pod_typography_status": "python raphael.py pod-typography-status",
            "pod_concept": "python raphael.py pod-concept \"Christian outdoors mountain cross shirt\"",
            "pod_prompt": "python raphael.py pod-prompt \"PODCON-ID\"",
            "pod_generation_request": "python raphael.py pod-generation-request \"PODCON-ID\" \"sdxl\"",
            "pod_generate": "python raphael.py pod-generate \"PODGEN-ID\"",
            "pod_review_design": "python raphael.py pod-review-design \"C:\\\\RaphaelOS\\\\PODStudio\\\\generated\\\\design.png\"",
            "pod_review_batch": "python raphael.py pod-review-batch \"C:\\\\RaphaelOS\\\\PODStudio\\\\generated\"",
            "pod_refactor_plan": "python raphael.py pod-refactor-plan \"PODREV-ID\"",
            "pod_remove_background": "python raphael.py pod-remove-background \"C:\\\\RaphaelOS\\\\PODStudio\\\\input\\\\design.png\"",
            "pod_upscale": "python raphael.py pod-upscale \"C:\\\\RaphaelOS\\\\PODStudio\\\\input\\\\design.png\"",
            "pod_listing_draft": "python raphael.py pod-listing-draft \"PODCON-ID\"",
            "pod_export_package": "python raphael.py pod-export-package \"PODCON-ID\"",
            "pod_pipeline": "python raphael.py pod-pipeline",
            "pod_review": "python raphael.py pod-review",
            "pod_brief": "python raphael.py pod-brief",
            "asset_status": "python raphael.py asset-status",
            "brand_create": "python raphael.py brand-create \"Brand Name\"",
            "brand_review": "python raphael.py brand-review",
            "brand_brief": "python raphael.py brand-brief",
            "brand_show": "python raphael.py brand-show \"BRAND-ID\"",
            "asset_import": "python raphael.py asset-import \"C:\\\\path\\\\asset.png\"",
            "asset_review": "python raphael.py asset-review \"ASSET-ID\"",
            "asset_search": "python raphael.py asset-search \"vintage outdoors\"",
            "asset_related": "python raphael.py asset-related \"ASSET-ID\"",
            "asset_tag": "python raphael.py asset-tag \"ASSET-ID\"",
            "asset_export": "python raphael.py asset-export \"ASSET-ID\"",
            "prompt_library": "python raphael.py prompt-library",
            "template_library": "python raphael.py template-library",
            "design_system_review": "python raphael.py design-system-review",
            "agency_status": "python raphael.py agency-status",
            "agency_review": "python raphael.py agency-review",
            "agency_brief": "python raphael.py agency-brief",
            "agency_service_offer": "python raphael.py agency-service-offer \"Shopify Integration\"",
            "agency_client_profile": "python raphael.py agency-client-profile \"Local retailer\"",
            "agency_proposal_plan": "python raphael.py agency-proposal-plan \"ERP integration\"",
            "agency_delivery_plan": "python raphael.py agency-delivery-plan \"Shopify Integration\"",
            "agency_pipeline": "python raphael.py agency-pipeline",
            "agency_delegate": "python raphael.py agency-delegate \"draft Shopify integration proposal\" \"Proposal Writer Agent\"",
            "creator_status": "python raphael.py creator-status",
            "creator_review": "python raphael.py creator-review",
            "creator_brief": "python raphael.py creator-brief",
            "creator_content_idea": "python raphael.py creator-content-idea \"AI automation tips\"",
            "creator_content_plan": "python raphael.py creator-content-plan \"AI automation tips\"",
            "creator_script": "python raphael.py creator-script \"AI automation tips\"",
            "creator_ebook_plan": "python raphael.py creator-ebook-plan \"AI automation for local businesses\"",
            "creator_offer_plan": "python raphael.py creator-offer-plan \"AI automation starter kit\"",
            "creator_pipeline": "python raphael.py creator-pipeline",
            "creator_delegate": "python raphael.py creator-delegate \"draft AI automation script\" \"Script Writer Agent\"",
            "kpi_status": "python raphael.py kpi-status",
            "kpi_add": "python raphael.py kpi-add \"Monthly Agency Revenue\" \"Revenue\" \"1000\"",
            "kpi_update": "python raphael.py kpi-update \"KPI-ID\" \"5\" \"Manual update\"",
            "kpi_review": "python raphael.py kpi-review",
            "kpi_brief": "python raphael.py kpi-brief",
            "kpi_dashboard": "python raphael.py kpi-dashboard",
            "kpi_history": "python raphael.py kpi-history \"KPI-ID\"",
            "finance_status": "python raphael.py finance-status",
            "finance_add_revenue": "python raphael.py finance-add-revenue \"Agency\" \"500\" \"Shopify setup\"",
            "finance_add_expense": "python raphael.py finance-add-expense \"Commerce\" \"25\" \"Etsy listing tools\"",
            "finance_summary": "python raphael.py finance-summary",
            "finance_review": "python raphael.py finance-review",
            "finance_brief": "python raphael.py finance-brief",
            "finance_forecast": "python raphael.py finance-forecast",
            "finance_budget": "python raphael.py finance-budget \"Creator\" \"100\"",
            "finance_history": "python raphael.py finance-history \"Agency\"",
            "portfolio_status": "python raphael.py portfolio-status",
            "portfolio_review": "python raphael.py portfolio-review",
            "portfolio_brief": "python raphael.py portfolio-brief",
            "portfolio_scorecard": "python raphael.py portfolio-scorecard",
            "portfolio_roadmap": "python raphael.py portfolio-roadmap",
            "portfolio_decision": "python raphael.py portfolio-decision \"Focus on Agency this week\"",
            "portfolio_compare": "python raphael.py portfolio-compare \"Agency\" \"Commerce\"",
            "portfolio_prioritize": "python raphael.py portfolio-prioritize",
            "portfolio_delegate": "python raphael.py portfolio-delegate \"PORTREC-AGENCY\" \"Agency Council\"",
            "command_bus_status": "python raphael.py command-bus-status",
            "command_bus_test": "python raphael.py command-bus-test \"what should I prioritize today\"",
            "command_bus_review": "python raphael.py command-bus-review",
            "command_list": "python raphael.py command-list",
            "command_help": "python raphael.py command-help \"portfolio\"",
            "notification_status": "python raphael.py notification-status",
            "notification_detect": "python raphael.py notification-detect",
            "notification_review": "python raphael.py notification-review",
            "notification_brief": "python raphael.py notification-brief",
            "notification_list": "python raphael.py notification-list",
            "notification_read": "python raphael.py notification-read \"NOTIF-ID\"",
            "notification_dismiss": "python raphael.py notification-dismiss \"NOTIF-ID\"",
            "notification_escalate": "python raphael.py notification-escalate \"NOTIF-ID\"",
            "brief_status": "python raphael.py brief-status",
            "morning_brief": "python raphael.py morning-brief",
            "evening_review": "python raphael.py evening-review",
            "weekly_brief": "python raphael.py weekly-brief",
            "monthly_review": "python raphael.py monthly-review",
            "executive_brief": "python raphael.py executive-brief",
            "brief_history": "python raphael.py brief-history",
            "brief_preferences": "python raphael.py brief-preferences",
            "daily_start": "python raphael.py daily-start",
            "daily_focus": "python raphael.py daily-focus",
            "daily_plan": "python raphael.py daily-plan",
            "daily_checkin": "python raphael.py daily-checkin \"What changed today\"",
            "daily_end": "python raphael.py daily-end",
            "daily_review": "python raphael.py daily-review",
            "bootstrap_status": "python raphael.py bootstrap-status",
            "bootstrap_start": "python raphael.py bootstrap-start",
            "bootstrap_stop": "python raphael.py bootstrap-stop",
            "bootstrap_restart": "python raphael.py bootstrap-restart",
            "bootstrap_health": "python raphael.py bootstrap-health",
            "bootstrap_review": "python raphael.py bootstrap-review",
            "bootstrap_install_startup": "python raphael.py bootstrap-install-startup",
            "bootstrap_remove_startup": "python raphael.py bootstrap-remove-startup",
            "bootstrap_open_dashboard": "python raphael.py bootstrap-open-dashboard",
            "activity_status": "python raphael.py activity-status",
            "activity_feed": "python raphael.py activity-feed",
            "activity_review": "python raphael.py activity-review",
            "activity_brief": "python raphael.py activity-brief",
            "activity_timeline": "python raphael.py activity-timeline",
            "activity_stats": "python raphael.py activity-stats",
            "activity_log": "python raphael.py activity-log \"System Event\" \"Title\" \"Details\"",
            "activity_read": "python raphael.py activity-read \"EVENT-ID\"",
            "initiative_status": "python raphael.py initiative-status",
            "initiative_detect": "python raphael.py initiative-detect",
            "initiative_review": "python raphael.py initiative-review",
            "initiative_brief": "python raphael.py initiative-brief",
            "initiative_score": "python raphael.py initiative-score \"INITIATIVE-ID\"",
            "initiative_delegate": "python raphael.py initiative-delegate \"INITIATIVE-ID\" \"Business Council\"",
            "initiative_history": "python raphael.py initiative-history",
            "employee_status": "python raphael.py employee-status",
            "employee_registry": "python raphael.py employee-registry",
            "employee_brief": "python raphael.py employee-brief \"Store Manager Agent\"",
            "employee_review": "python raphael.py employee-review \"Store Manager Agent\"",
            "employee_workload": "python raphael.py employee-workload",
            "employee_org_chart": "python raphael.py employee-org-chart",
            "employee_assign_kpi": "python raphael.py employee-assign-kpi \"Store Manager Agent\" \"KPI-ID\"",
            "employee_reassign": "python raphael.py employee-reassign \"Store Manager Agent\" \"Commerce Council\"",
            "employee_task_brief": "python raphael.py employee-task-brief \"Store Manager Agent\"",
            "execution_status": "python raphael.py execution-status",
            "execution_policy": "python raphael.py execution-policy",
            "execution_request": "python raphael.py execution-request \"refresh command center\"",
            "execution_dry_run": "python raphael.py execution-dry-run \"EXEC-ID\"",
            "execution_approve": "python raphael.py execution-approve \"EXEC-ID\"",
            "execution_run": "python raphael.py execution-run \"EXEC-ID\"",
            "execution_review": "python raphael.py execution-review",
            "execution_log": "python raphael.py execution-log",
            "execution_safety_report": "python raphael.py execution-safety-report",
        },
    }


INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Raphael OS Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="/static/css/matrix.css?v=57-presence" />
  <link rel="stylesheet" href="/static/css/employee_network.css?v=56-employee-network-fix1" />
  <style>
    :root {
      color-scheme: dark;
      --bg: #050817;
      --panel: rgba(10, 18, 45, .82);
      --panel2: rgba(8, 14, 34, .94);
      --line: rgba(91, 224, 255, .22);
      --cyan: #31d8ff;
      --pink: #ff37d4;
      --violet: #7a5cff;
      --text: #e9f6ff;
      --muted: #8ea6c8;
      --good: #50f2a6;
      --warn: #ffd166;
      --bad: #ff6b8a;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      color: var(--text);
      font: 14px/1.45 "Segoe UI", Inter, system-ui, sans-serif;
      background:
        linear-gradient(rgba(49,216,255,.06) 1px, transparent 1px),
        linear-gradient(90deg, rgba(49,216,255,.06) 1px, transparent 1px),
        radial-gradient(circle at 20% 0%, rgba(255,55,212,.23), transparent 28%),
        radial-gradient(circle at 85% 10%, rgba(49,216,255,.22), transparent 32%),
        var(--bg);
      background-size: 42px 42px, 42px 42px, auto, auto, auto;
    }
    body:before {
      content: "";
      position: fixed; inset: 0; pointer-events: none;
      background: linear-gradient(120deg, transparent, rgba(49,216,255,.08), transparent);
      mask-image: radial-gradient(circle at center, black, transparent 75%);
    }
    .shell { display: grid; grid-template-columns: 230px 1fr; min-height: 100vh; }
    aside {
      position: sticky; top: 0; height: 100vh; padding: 22px 16px;
      background: rgba(3, 7, 21, .72); border-right: 1px solid var(--line);
      box-shadow: 0 0 32px rgba(49,216,255,.12);
      overflow-y: auto; scrollbar-width: thin;
    }
    .brand { font-size: 20px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .brand span { color: var(--cyan); text-shadow: 0 0 18px var(--cyan); }
    .sub { color: var(--muted); margin: 4px 0 22px; }
    nav button {
      width: 100%; display: block; margin: 7px 0; padding: 10px 12px; color: var(--muted);
      border: 1px solid transparent; border-radius: 8px; background: transparent; text-align: left; cursor: pointer;
    }
    nav button.active, nav button:hover {
      color: var(--text); border-color: rgba(49,216,255,.38); background: rgba(49,216,255,.08);
      box-shadow: inset 0 0 18px rgba(49,216,255,.08);
    }
    main { padding: 24px; }
    header {
      display: flex; justify-content: space-between; align-items: flex-start; gap: 18px; margin-bottom: 18px;
      padding: 18px; border: 1px solid rgba(255,55,212,.38); border-radius: 10px;
      background: linear-gradient(135deg, rgba(255,55,212,.1), rgba(49,216,255,.08));
      box-shadow: 0 0 28px rgba(255,55,212,.16);
    }
    h1 { margin: 0; font-size: 26px; }
    h2 { margin: 0 0 12px; font-size: 16px; color: var(--cyan); }
    .grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 14px; }
    .card {
      grid-column: span 4; padding: 15px; border: 1px solid var(--line); border-radius: 8px;
      background: var(--panel); box-shadow: 0 0 22px rgba(49,216,255,.08);
      min-width: 0;
    }
    .wide { grid-column: span 8; }
    .full { grid-column: 1 / -1; }
    .stat { font-size: 28px; font-weight: 700; color: var(--text); }
    .muted { color: var(--muted); }
    .pill {
      display: inline-flex; gap: 6px; align-items: center; padding: 4px 8px; margin: 3px 4px 3px 0;
      border: 1px solid rgba(49,216,255,.28); border-radius: 999px; color: var(--muted); background: rgba(49,216,255,.06);
    }
    .ok { color: var(--good); } .warn { color: var(--warn); } .bad { color: var(--bad); }
    pre {
      white-space: pre-wrap; overflow-wrap: anywhere; margin: 0; color: #d9eaff;
      font: 12px/1.45 Consolas, ui-monospace, monospace;
    }
    table { width: 100%; border-collapse: collapse; }
    th, td { padding: 9px 7px; border-bottom: 1px solid rgba(91,224,255,.13); text-align: left; vertical-align: top; }
    th { color: var(--cyan); font-weight: 600; }
    .bar { height: 7px; border-radius: 999px; background: rgba(255,255,255,.08); overflow: hidden; margin-top: 8px; }
    .bar i { display: block; height: 100%; background: linear-gradient(90deg, var(--cyan), var(--pink)); }
    .copy {
      border: 1px solid rgba(255,55,212,.38); color: var(--text); border-radius: 8px; background: rgba(255,55,212,.09);
      padding: 8px 10px; cursor: pointer; margin: 4px 5px 4px 0;
    }
    .copy:hover { box-shadow: 0 0 18px rgba(255,55,212,.18); }
    .empty { color: var(--muted); padding: 14px; border: 1px dashed rgba(91,224,255,.18); border-radius: 8px; }
    .maintenance-hero { display: flex; align-items: center; justify-content: space-between; gap: 18px; }
    .maintenance-hero.healthy { border-color: rgba(80,242,166,.35); }
    .maintenance-hero.attention { border-color: rgba(255,107,138,.42); }
    .maintenance-state { display: inline-flex; padding: 4px 8px; border-radius: 999px; border: 1px solid currentColor; font-size: 11px; }
    .error-banner {
      display: grid; gap: 7px; border-color: rgba(255,107,138,.5);
      background: linear-gradient(135deg, rgba(255,107,138,.12), rgba(8,14,34,.92));
      box-shadow: 0 0 24px rgba(255,107,138,.12);
    }
    .maintenance-error {
      display: grid; gap: 3px; margin: 6px 0; padding: 9px;
      border: 1px solid rgba(255,107,138,.16); border-radius: 8px; background: rgba(255,107,138,.05);
    }
    .maintenance-error strong { color: #ff9aae; }
    .maintenance-error span { color: var(--muted); overflow-wrap: anywhere; }
    .raphael-core {
      position: relative; width: min(680px, 100%); height: clamp(340px, 52vw, 600px); margin: 0 auto 18px;
      border-radius: 14px; overflow: hidden; display: grid; place-items: center;
      background: #000008;
      border: 1px solid rgba(91,224,255,.18);
      box-shadow: 0 0 42px rgba(49,216,255,.16), inset 0 0 44px rgba(123,111,255,.12);
    }
    .raphael-core canvas {
      width: 100%; height: 100%; display: block;
    }
    .raphael-core:after {
      content: ""; position: absolute; inset: 0; pointer-events: none;
      background:
        linear-gradient(rgba(255,255,255,.045) 1px, transparent 1px),
        radial-gradient(circle at center, transparent 0 58%, rgba(0,0,8,.24) 76%, rgba(0,0,8,.7) 100%);
      background-size: 100% 4px, auto;
      mix-blend-mode: screen;
    }
    .core-text {
      position: absolute; left: 0; right: 0; bottom: 22px; z-index: 1; text-align: center;
      text-transform: uppercase; letter-spacing: .14em; color: rgba(180,190,255,.82);
      text-shadow: 0 0 18px rgba(123,111,255,.65), 0 0 34px rgba(49,216,255,.32);
    }
    .chat-log { display: flex; flex-direction: column; gap: 12px; max-height: 520px; overflow: auto; padding-right: 4px; }
    .bubble { border: 1px solid rgba(91,224,255,.18); border-radius: 10px; padding: 12px; background: rgba(8,14,34,.72); }
    .bubble.user { border-color: rgba(255,55,212,.28); background: rgba(255,55,212,.08); }
    .bubble.raphael { border-color: rgba(255,209,102,.35); background: rgba(255,209,102,.07); }
    .chat-input {
      width: 100%; min-height: 92px; resize: vertical; color: var(--text); border: 1px solid rgba(49,216,255,.32);
      border-radius: 10px; background: rgba(2,7,22,.82); padding: 12px; outline: none;
    }
    .chat-input:focus { box-shadow: 0 0 0 3px rgba(49,216,255,.12), 0 0 22px rgba(49,216,255,.16); }
    .mic-button { min-width: 44px; border: 1px solid rgba(49,216,255,.42); background: rgba(49,216,255,.08); color: #bff6ff; border-radius: 10px; padding: 9px 12px; }
    .mic-button[data-active="true"] { background: rgba(255,75,180,.18); border-color: rgba(255,75,180,.7); box-shadow: 0 0 20px rgba(255,75,180,.25); }
    .voice-state { text-transform: uppercase; letter-spacing: .08em; font-size: 11px; }
    .voice-error { color: #ff9fae; }
    .primary {
      border: 1px solid rgba(255,209,102,.52); color: #fff9d6; border-radius: 10px;
      background: linear-gradient(90deg, rgba(255,209,102,.18), rgba(49,216,255,.14)); padding: 10px 14px; cursor: pointer;
    }
    .primary:hover { box-shadow: 0 0 22px rgba(255,209,102,.24); }
    @media (max-width: 980px) {
      .shell { grid-template-columns: 1fr; }
      aside { position: relative; height: auto; }
      .card, .wide { grid-column: 1 / -1; }
    }
  </style>
</head>
<body class="matrix-view">
<div class="shell">
  <aside id="classic-sidebar">
    <div class="brand">Raphael <span>OS</span></div>
    <div class="sub">Local command layer</div>
    <nav id="nav"></nav>
  </aside>
  <main>
    <header>
      <div>
        <h1 id="title">Command Center</h1>
        <div id="subtitle" class="muted">Read-only localhost dashboard</div>
      </div>
      <div class="muted" style="text-align:right">
        <button class="copy" id="bootstrap-health-pill" onclick="active='maintenance'; render();">Core: Loading · AI: Loading · Creative: Loading · Voice: Loading</button>
        <button class="copy" id="view-toggle" data-matrix-action="toggle-view">Classic View</button>
        <button class="copy" id="activity-counter" onclick="active='activity'; render();">Activity 0</button>
        <button class="copy" id="notification-bell" onclick="active='notifications'; render();">Notifications 0</button>
        <div id="generated">Loading...</div>
      </div>
    </header>
    <section id="matrix-root" class="matrix-root"></section>
    <section id="content" class="grid"></section>
  </main>
</div>
<script src="/static/js/matrix_config.js?v=63b-pod-studio"></script>
<script src="/static/js/transitions.js?v=56-employee-network"></script>
<script src="/static/js/hud.js?v=56-employee-network"></script>
<script src="/static/js/raphael_orb.js?v=57-presence-2"></script>
<script src="/static/js/galaxy_map.js?v=57-presence"></script>
<script src="/static/js/employee_network.js?v=56-employee-network"></script>
<script src="/static/js/matrix.js?v=59-communications"></script>
<script src="/static/js/business_dashboard.js?v=1"></script>
<script src="/static/js/missions.js?v=1"></script>
<script>
const pages = [
  ["home", "Home / Command Center"], ["chat", "Dashboard Chat"], ["daily", "Daily Operating Loop"], ["knowledge", "Knowledge Ingestion"], ["relationships", "Knowledge Relationships"], ["n8nstudio", "n8n Workflow Studio"], ["workflowrunner", "Workflow Runner"], ["communications", "Inter-Council Communications"], ["commandbus", "Command Bus"], ["notifications", "Notifications"], ["activity", "Activity Stream"], ["briefs", "Executive Briefs"], ["identity", "Identity"], ["world", "World Model"], ["simulations", "Simulations"], ["opportunities", "Opportunities"], ["allocation", "Resource Allocation"], ["blueprints", "Business Blueprints"], ["commerce", "Commerce"], ["podstudio", "POD Design Studio"], ["assetlibrary", "Asset & Brand Library"], ["agency", "Agency"], ["creator", "Creator"], ["kpis", "KPIs"], ["finance", "Financial Intelligence"], ["portfolio", "Business Portfolio"], ["initiatives", "Executive Initiatives"], ["employees", "Digital Employees"], ["executionplans", "Execution Plans"], ["execution", "Controlled Execution"], ["builder", "Builder"], ["projects", "Projects"], ["goals", "Goals"], ["goalpropagation", "Goal Propagation"], ["deliberations", "Deliberations"], ["tasks", "Tasks"],
  ["agents", "Agents"], ["councils", "Councils"], ["workflows", "Workflows"], ["memory", "Memory Search"], ["voice", "Voice Status"],
  ["vision", "Vision Requests"], ["search", "Internet Access"], ["health", "System Health"], ["selfhealing", "Self-Healing"], ["maintenance", "Maintenance"]
];
var data = null;
var active = "home";
var serviceActionState = null;
var dashboardChatTestState = null;
var workflowActionState = null;
var selfHealingActionState = null;
let chatMessages = [
  { role: "raphael", text: "Raphael is online. Type a command or ask a question.", meta: "Ready" }
];

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function statusClass(value) {
  const s = String(value || "").toLowerCase();
  if (s.includes("done") || s.includes("completed") || s.includes("active") || s === "ok" || s === "true" || s === "healthy" || s === "running" || s === "external") return "ok";
  if (s.includes("pending") || s.includes("waiting") || s.includes("in progress")) return "warn";
  if (s.includes("blocked") || s.includes("failed") || s === "false") return "bad";
  return "muted";
}
function copyCommand(cmd) {
  navigator.clipboard.writeText(cmd);
}
function card(title, body, cls="card") {
  return `<article class="${cls}"><h2>${esc(title)}</h2>${body}</article>`;
}
function table(rows, cols) {
  if (!rows.length) return `<div class="empty">No records found.</div>`;
  return `<table><thead><tr>${cols.map(c=>`<th>${esc(c[0])}</th>`).join("")}</tr></thead><tbody>` +
    rows.map(row => `<tr>${cols.map(c=>`<td>${c[2] ? c[2](row[c[1]], row) : esc(row[c[1]])}</td>`).join("")}</tr>`).join("") +
    `</tbody></table>`;
}
function renderHome() {
  const c = data.counts;
  const notes = data.notes.map(n => card(n.label, n.exists ? `<div class="muted">${esc(n.updated)}</div><pre>${esc(n.content)}</pre>` : `<div class="empty">Missing note: ${esc(n.path)}</div>`, "card wide")).join("");
  const latestBrief = data.briefs && data.briefs.latest && data.briefs.latest.exists
    ? card("Latest Executive Brief", `<div class="muted">${esc(data.briefs.latest.updated)}</div><pre>${esc(data.briefs.latest.content)}</pre><button class="copy" onclick="active='briefs'; render();">Open Executive Briefs</button>`, "card full")
    : "";
  const recentActivity = data.activity && data.activity.recent
    ? card("Recent Activity", table(data.activity.recent, [["Time","Timestamp"],["Type","Event Type"],["Title","Title"],["Severity","Severity"]]) + `<button class="copy" onclick="active='activity'; render();">Open Activity Stream</button>`, "card full")
    : "";
  return [
    latestBrief,
    card("Current Mode", `<div class="stat">${esc(data.mode.mode)}</div><pre>${esc(data.mode.focus)}</pre>`),
    card("Open Tasks", `<div class="stat">${c.tasks_open}</div><span class="${c.tasks_blocked ? "bad" : "ok"}">${c.tasks_blocked} blocked</span>`),
    card("Requests", `<span class="pill">Vision ${c.vision_pending}</span><span class="pill">Search ${c.search_pending}</span><span class="pill">Workflows ${c.workflow_pending}</span>`),
    recentActivity,
    card("Copy CLI Commands", Object.values(data.commands).map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join(""), "card full"),
    notes
  ].join("");
}
function renderInternetOverviewCard(overview, result = {}) {
  if (!overview || !overview.request_id) {
    return `<article class="card full"><h2>AI Overview</h2><div class="empty">No internet overview has been saved yet.</div></article>`;
  }
  const points = (overview.key_points || []).slice(0, 3).map(point => `<li>${esc(point)}</li>`).join("");
  const sources = (overview.sources || []).slice(0, 3).map((source, index) => `
    <li><strong>${index + 1}. ${esc(source.title || source.url || "Source")}</strong> <span class="muted">${esc(source.note || "")}</span></li>
  `).join("");
  return `
    <article class="card full ai-overview-card">
      <h2>AI Overview</h2>
      <span class="pill">${esc(overview.request_id)}</span>
      <span class="pill">Confidence ${esc(overview.confidence || "Low")}</span>
      <h3>Answer</h3>
      <p>${esc(overview.answer || "No source-backed answer could be generated.")}</p>
      <h3>Key points</h3>
      <ul>${points || "<li>No key points available.</li>"}</ul>
      <h3>Sources</h3>
      <ol>${sources || "<li>No sources available.</li>"}</ol>
      <p class="muted">${esc(overview.confidence_reason || "Insufficient evidence.")}</p>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('show sources')">Show Sources</button>
        <button class="copy" onclick="sendQuickChat('show snippets')">Show Snippets</button>
        <button class="copy" onclick="sendQuickChat('raw JSON')">Show Raw JSON</button>
        <button class="copy" onclick="sendQuickChat('save to knowledge')">Save to Knowledge</button>
      </div>
    </article>
  `;
}
function renderChat() {
  const examples = ["hello Raphael", "what should I prioritize today?", "summarize Secure Email Service", "ask Developer Agent what this project needs", "memory search portfolio review"];
  const quick = [
    ["Command Center", "command center"],
    ["Prioritize", "what should I prioritize today?"],
    ["List Councils", "list councils"],
    ["Council Status", "council status"],
    ["Council Task Review", "council task review"],
    ["Executive Summary", "executive summary on Secure Email Service"],
    ["Debate Topic", "debate Build MentorMap MVP"],
    ["Detect Initiatives", "detect initiatives"],
    ["Brief Initiatives", "brief initiatives"],
    ["Employee Registry", "show employee registry"],
    ["Employee Workload", "show employee workload"],
    ["Run Initiative Detection", "run initiative detection"],
    ["Refresh KPI Dashboard", "run KPI dashboard refresh"],
    ["Morning Brief", "give me a morning brief"],
    ["Executive Brief", "executive brief"],
    ["Weekly Brief", "weekly brief"],
    ["Build Python App", "build a Python app that tracks button clicks"]
  ];
  return `
    <article class="card wide">
      <h2>Raphael Command Core</h2>
      <div class="raphael-core">
        <canvas id="raphael-orb" width="680" height="600" aria-label="Raphael command orb"></canvas>
      </div>
      <div class="flex flex-wrap gap-2 text-xs">
        <span class="pill">Safe CLI allowlist</span>
        <span class="pill">Ollama general mode</span>
        <span class="pill">Confirm gated actions</span>
        <span class="pill">No arbitrary shell</span>
      </div>
    </article>
    <article class="card">
      <h2>Quick Controls</h2>
      <div>${quick.map(([label, phrase]) => `<button class="copy" onclick="sendQuickChat('${esc(phrase)}')">${esc(label)}</button>`).join("")}</div>
      <h2 class="mt-4">Try Saying</h2>
      <div>${examples.map(x => `<button class="copy" onclick="useChatExample('${esc(x)}')">${esc(x)}</button>`).join("")}</div>
      <p class="muted mt-3">Browser voice places transcript text into Dashboard Chat and routes it through the Command Bus. Raphael does not save or upload audio. Piper remains available through <code>R:/RaphaelOS/voice_gateway.py</code>.</p>
    </article>
    <article class="card full">
      <h2>Dashboard Chat</h2>
      ${chatMessages.some(m => m.awaiting) ? `<div class="mb-3 rounded-lg border border-amber-300/50 bg-amber-300/10 p-3 text-amber-100">Pending action: type <strong>confirm</strong> to continue or <strong>cancel</strong> to stop it.</div>` : ""}
      <div id="chat-log" class="chat-log mb-4">${chatMessages.map((m, i) => renderBubble(m, i)).join("")}</div>
      <textarea id="chat-input" class="chat-input" placeholder="Ask Raphael..."></textarea>
      <div class="mt-3 flex flex-wrap items-center gap-2">
        <button class="primary" onclick="sendChat()">Send to Raphael</button>
        <button id="chat-mic" class="mic-button" data-active="${dashboardVoiceState === "listening"}" onclick="toggleDashboardVoice()" title="Speak to Raphael" aria-label="Speak to Raphael">🎙</button>
        <button class="copy" onclick="useChatExample('confirm')">confirm</button>
        <button class="copy" onclick="useChatExample('cancel')">cancel</button>
        <label class="muted text-xs"><input id="chat-tts-enabled" type="checkbox" ${dashboardVoiceSpeakResponses ? "checked" : ""} onchange="dashboardVoiceSpeakResponses=this.checked"> speak responses</label>
        <span id="voice-state" class="voice-state muted">${esc(dashboardVoiceState)}</span>
        <span id="chat-status" class="muted"></span>
      </div>
      <div id="voice-message" class="${dashboardVoiceState === "error" ? "voice-error" : "muted"} mt-2 text-xs">${esc(dashboardVoiceMessage)}</div>
    </article>
    ${renderInternetOverviewCard(data.internet_access?.latest_overview, data.internet_access?.latest_result)}
  `;
}
function hexColor(hex, alpha) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return `rgba(${r},${g},${b},${alpha})`;
}
function setRaphaelOrbSpeaking() {
  const canvas = document.getElementById("raphael-orb");
  if (canvas) {
    canvas.dataset.mode = "speaking";
  }
}
function setRaphaelOrbIdle() {
  const canvas = document.getElementById("raphael-orb");
  if (canvas) canvas.dataset.mode = "idle";
}
let dashboardSpeechRecognition = null;
let dashboardVoiceState = "idle";
let dashboardVoiceMessage = "";
let dashboardVoiceFinalTranscript = "";
let dashboardVoiceSpeakResponses = false;
let dashboardVoiceSubmitted = false;
let taskFocusId = "";

function dashboardSpeechRecognitionClass() {
  return window.SpeechRecognition || window.webkitSpeechRecognition || null;
}
function dashboardVoiceInputEnabled() {
  return data?.maintenance?.system_health?.dashboard_chat?.voice_input_enabled !== false;
}
function voiceFallbackMessage() {
  return "Browser speech recognition is unavailable. Use: python R:/RaphaelOS/voice_gateway.py voice-once (or chat).";
}
function setDashboardVoiceState(state, message = "") {
  dashboardVoiceState = state;
  dashboardVoiceMessage = message;
  const stateNode = document.getElementById("voice-state");
  if (stateNode) stateNode.textContent = state;
  const messageNode = document.getElementById("voice-message");
  if (messageNode) {
    messageNode.textContent = message;
    messageNode.className = `${state === "error" ? "voice-error" : "muted"} mt-2 text-xs`;
  }
  const mic = document.getElementById("chat-mic");
  if (mic) mic.dataset.active = state === "listening" ? "true" : "false";
  const canvas = document.getElementById("raphael-orb");
  if (canvas) canvas.dataset.mode = state;
  window.RaphaelOrb?.setState(state);
}
function initDashboardVoiceBridge() {
  if (!dashboardVoiceInputEnabled()) {
    dashboardVoiceMessage = "Browser microphone input is disabled in config/settings.json. Use R:/RaphaelOS/voice_gateway.py if voice input is needed.";
    const mic = document.getElementById("chat-mic");
    if (mic) mic.disabled = true;
    const message = document.getElementById("voice-message");
    if (message) message.textContent = dashboardVoiceMessage;
    return;
  }
  if (!dashboardSpeechRecognitionClass()) {
    dashboardVoiceMessage = voiceFallbackMessage();
    const mic = document.getElementById("chat-mic");
    if (mic) mic.disabled = true;
    const message = document.getElementById("voice-message");
    if (message) message.textContent = dashboardVoiceMessage;
  }
}
function toggleDashboardVoice() {
  if (!dashboardVoiceInputEnabled()) {
    setDashboardVoiceState("error", "Browser microphone input is disabled in config/settings.json.");
    return;
  }
  if (dashboardSpeechRecognition && dashboardVoiceState === "listening") {
    dashboardSpeechRecognition.stop();
    return;
  }
  const Recognition = dashboardSpeechRecognitionClass();
  if (!Recognition) {
    setDashboardVoiceState("error", voiceFallbackMessage());
    return;
  }
  dashboardVoiceFinalTranscript = "";
  dashboardVoiceSubmitted = false;
  const recognition = new Recognition();
  dashboardSpeechRecognition = recognition;
  recognition.lang = navigator.language || "en-US";
  recognition.continuous = false;
  recognition.interimResults = true;
  recognition.maxAlternatives = 1;
  recognition.onstart = () => setDashboardVoiceState("listening", "Listening… Speak naturally. Audio is not saved by Raphael.");
  recognition.onaudiostart = () => setDashboardVoiceState("listening", "Listening…");
  recognition.onresult = event => {
    setDashboardVoiceState("transcribing", "Transcribing through the browser speech interface…");
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; i += 1) {
      const transcript = event.results[i][0]?.transcript || "";
      if (event.results[i].isFinal) dashboardVoiceFinalTranscript += transcript;
      else interim += transcript;
    }
    const input = document.getElementById("chat-input");
    if (input) input.value = (dashboardVoiceFinalTranscript || interim).trim();
    if (dashboardVoiceFinalTranscript.trim() && !dashboardVoiceSubmitted) {
      dashboardVoiceSubmitted = true;
      setDashboardVoiceState("thinking", "Transcript ready. Routing through Dashboard Chat and Command Bus…");
      recognition.stop();
      setTimeout(() => sendChat({ fromVoice: true }), 80);
    }
  };
  recognition.onerror = event => {
    const permission = ["not-allowed", "service-not-allowed"].includes(event.error);
    setDashboardVoiceState("error", permission
      ? "Microphone permission was denied. Allow microphone access for localhost, or use R:/RaphaelOS/voice_gateway.py."
      : `Speech recognition error: ${event.error}. ${voiceFallbackMessage()}`);
  };
  recognition.onend = () => {
    dashboardSpeechRecognition = null;
    if (!dashboardVoiceFinalTranscript && !["thinking", "speaking", "error"].includes(dashboardVoiceState)) {
      setDashboardVoiceState("idle", "Listening stopped. No audio was saved.");
    }
  };
  try {
    recognition.start();
  } catch (error) {
    setDashboardVoiceState("error", "Unable to start browser microphone: " + error);
  }
}
function speakDashboardResponse(text) {
  if (!dashboardVoiceSpeakResponses || !("speechSynthesis" in window) || !text) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(String(text).slice(0, 1600));
  utterance.onstart = () => setDashboardVoiceState("speaking", "Speaking response…");
  utterance.onend = () => setDashboardVoiceState("idle", "Ready. No audio was saved.");
  utterance.onerror = () => setDashboardVoiceState("error", "Browser text-to-speech failed.");
  window.speechSynthesis.speak(utterance);
}
function initRaphaelOrb() {
  const canvas = document.getElementById("raphael-orb");
  if (!canvas || canvas.dataset.started === "true") return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  canvas.dataset.started = "true";
  canvas.dataset.mode = "idle";
  const cx = 340, cy = 300;
  let t = 0;
  const rings = [
    { r: 60,  speed: 0.008, segments: 8,  width: 3,   color: "#7B6FFF" },
    { r: 90,  speed: -0.005, segments: 12, width: 2,   color: "#5B8FFF" },
    { r: 120, speed: 0.004, segments: 16, width: 1.5, color: "#8B5FEF" },
    { r: 155, speed: -0.003, segments: 24, width: 1,   color: "#4B7FFF" },
    { r: 190, speed: 0.002, segments: 32, width: 1,   color: "#6B4FDF" },
    { r: 230, speed: -0.0015, segments: 48, width: .7, color: "#3B6FEF" },
  ];
  const particles = Array.from({length: 80}, () => ({
    angle: Math.random() * Math.PI * 2,
    r: 20 + Math.random() * 200,
    speed: (Math.random() - .5) * .02,
    size: Math.random() * 2.5 + .5,
    alpha: Math.random(),
    color: Math.random() > .5 ? "#8B7FFF" : "#5BAFFF"
  }));
  const dataArcs = Array.from({length: 6}, (_, i) => ({
    r: 105 + i * 22,
    startAngle: Math.random() * Math.PI * 2,
    span: .3 + Math.random() * 1.2,
    speed: (Math.random() > .5 ? 1 : -1) * (.01 + Math.random() * .02),
    width: 2 + Math.random() * 3,
    color: `hsl(${230 + i * 15}, 80%, ${60 + i * 3}%)`
  }));
  function mode() { return canvas.dataset.mode || "idle"; }
  function drawCoreGlow() {
    const active = mode() === "speaking";
    let og = ctx.createRadialGradient(cx, cy, 0, cx, cy, 260);
    og.addColorStop(0, "rgba(80,60,200,0.18)");
    og.addColorStop(.5, "rgba(40,80,220,0.08)");
    og.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = og;
    ctx.beginPath(); ctx.arc(cx, cy, 260, 0, Math.PI*2); ctx.fill();

    const pulse = .85 + Math.sin(t * 3) * .15 + (active ? Math.sin(t * 18) * .1 : 0);
    let cg = ctx.createRadialGradient(cx, cy, 0, cx, cy, 55 * pulse);
    cg.addColorStop(0, "rgba(255,255,255,0.95)");
    cg.addColorStop(.15, "rgba(180,160,255,0.9)");
    cg.addColorStop(.4, "rgba(100,120,255,0.7)");
    cg.addColorStop(.7, "rgba(60,80,220,0.4)");
    cg.addColorStop(1, "rgba(40,40,180,0)");
    ctx.fillStyle = cg;
    ctx.beginPath(); ctx.arc(cx, cy, 55 * pulse, 0, Math.PI*2); ctx.fill();

    let ig = ctx.createRadialGradient(cx, cy, 0, cx, cy, 20);
    ig.addColorStop(0, "rgba(255,255,255,1)");
    ig.addColorStop(.5, "rgba(200,210,255,0.8)");
    ig.addColorStop(1, "rgba(150,160,255,0)");
    ctx.fillStyle = ig;
    ctx.beginPath(); ctx.arc(cx, cy, 20, 0, Math.PI*2); ctx.fill();
  }
  function drawRayBurst() {
    const numRays = mode() === "speaking" ? 24 : 18;
    for (let i = 0; i < numRays; i++) {
      const angle = (i / numRays) * Math.PI * 2 + t * .3;
      const len = 40 + Math.random() * 180;
      const alpha = .03 + Math.random() * .07;
      ctx.strokeStyle = `rgba(140,160,255,${alpha})`;
      ctx.lineWidth = .5;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.cos(angle) * len, cy + Math.sin(angle) * len);
      ctx.stroke();
    }
  }
  function drawRings() {
    rings.forEach(ring => {
      const segAngle = (Math.PI * 2) / ring.segments;
      const offset = t * ring.speed * 60;
      for (let i = 0; i < ring.segments; i++) {
        const a = i * segAngle + offset;
        const gap = segAngle * .15;
        ctx.save();
        ctx.strokeStyle = hexColor(ring.color, .6 + Math.sin(t * 2 + i) * .2);
        ctx.lineWidth = ring.width;
        ctx.shadowBlur = 8;
        ctx.shadowColor = ring.color;
        ctx.beginPath();
        ctx.arc(cx, cy, ring.r, a + gap, a + segAngle - gap);
        ctx.stroke();
        ctx.restore();
      }
    });
  }
  function drawDataArcs() {
    dataArcs.forEach(arc => {
      arc.startAngle += arc.speed;
      ctx.save();
      ctx.strokeStyle = arc.color.replace("hsl", "hsla").replace(")", ", 0.5)");
      ctx.lineWidth = arc.width;
      ctx.shadowBlur = 6;
      ctx.shadowColor = arc.color;
      ctx.beginPath();
      ctx.arc(cx, cy, arc.r, arc.startAngle, arc.startAngle + arc.span);
      ctx.stroke();
      for (let k = 0; k < 4; k++) {
        const ta = arc.startAngle + (arc.span / 4) * k;
        ctx.beginPath();
        ctx.moveTo(cx + Math.cos(ta) * (arc.r - 4), cy + Math.sin(ta) * (arc.r - 4));
        ctx.lineTo(cx + Math.cos(ta) * (arc.r + 4), cy + Math.sin(ta) * (arc.r + 4));
        ctx.stroke();
      }
      ctx.restore();
    });
  }
  function drawHexCore() {
    const radius = 42 + Math.sin(t * 2) * 3;
    ctx.save();
    ctx.strokeStyle = "rgba(180,190,255,0.5)";
    ctx.lineWidth = 1.5;
    ctx.shadowBlur = 10;
    ctx.shadowColor = "#7B8FFF";
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2 + t * .5;
      const x = cx + Math.cos(a) * radius;
      const y = cy + Math.sin(a) * radius;
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.stroke();
    ctx.restore();
  }
  function drawParticles() {
    particles.forEach(p => {
      p.angle += p.speed;
      p.alpha = .3 + Math.abs(Math.sin(t * 1.5 + p.angle)) * .7;
      ctx.save();
      ctx.fillStyle = p.color;
      ctx.globalAlpha = p.alpha;
      ctx.shadowBlur = 6;
      ctx.shadowColor = p.color;
      ctx.beginPath();
      ctx.arc(cx + Math.cos(p.angle) * p.r, cy + Math.sin(p.angle) * p.r, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });
  }
  function drawSpeakingWave() {
    if (mode() !== "speaking") return;
    for (let ring = 0; ring < 3; ring++) {
      const baseR = 62 + ring * 8;
      ctx.save();
      ctx.strokeStyle = `rgba(160,180,255,${.4 - ring * .1})`;
      ctx.lineWidth = 2 - ring * .5;
      ctx.beginPath();
      for (let i = 0; i <= 120; i++) {
        const a = (i / 120) * Math.PI * 2;
        const wave = Math.sin(a * 8 + t * 20 + ring * 2) * (6 - ring * 1.5);
        const r = baseR + wave;
        const x = cx + Math.cos(a) * r;
        const y = cy + Math.sin(a) * r;
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.stroke();
      ctx.restore();
    }
  }
  function drawLabel() {
    ctx.save();
    ctx.font = "500 13px Consolas, monospace";
    ctx.fillStyle = "rgba(140,160,255,0.72)";
    ctx.textAlign = "center";
    ctx.fillText(mode() === "idle" ? "AWAITING COMMAND" : "PROCESSING...", cx, cy + 280);
    for (let i = 0; i < 5; i++) {
      const active = Math.floor((t * 3) % 5) === i;
      ctx.fillStyle = active ? "rgba(140,180,255,0.9)" : "rgba(80,80,150,0.4)";
      ctx.beginPath();
      ctx.arc(cx - 20 + i * 10, cy + 265, 2, 0, Math.PI*2);
      ctx.fill();
    }
    ctx.restore();
  }
  function draw() {
    if (!canvas.isConnected) return;
    ctx.clearRect(0, 0, 680, 600);
    ctx.fillStyle = "#000008";
    ctx.fillRect(0, 0, 680, 600);
    drawRayBurst();
    drawParticles();
    drawDataArcs();
    drawRings();
    drawHexCore();
    drawCoreGlow();
    drawSpeakingWave();
    drawLabel();
    t += .016;
    requestAnimationFrame(draw);
  }
  draw();
}
function hasCode(text) {
  return /```|\\b(def|class|function|const|let|import)\\b/.test(text || "");
}
function formatResponseText(text) {
  const escaped = esc(text);
  if (escaped.includes("```")) {
    return escaped.replace(/```([\\s\\S]*?)```/g, '<pre class="mt-2 rounded-lg border border-cyan-300/20 bg-black/30 p-3">$1</pre>');
  }
  return `<div class="whitespace-pre-wrap">${escaped}</div>`;
}
function renderBubble(message, index) {
  const who = message.role === "user" ? "Aaron" : "Raphael";
  const cls = message.role === "user" ? "user" : "raphael";
  const meta = message.meta ? `<div class="muted text-xs mt-2">${esc(message.meta)}</div>` : "";
  const body = (message.text || "").length > 900
    ? `<details open><summary class="cursor-pointer text-cyan-200">Long response</summary>${formatResponseText(message.text)}</details>`
    : formatResponseText(message.text);
  const command = message.command ? `<div class="mt-2 rounded border border-cyan-300/20 p-2"><div class="muted text-xs">Command</div><code>${esc(message.command)}</code></div>` : "";
  const status = message.status ? `<div class="mt-2"><span class="pill">${esc(message.status)}</span>${message.awaiting ? '<span class="pill">awaiting confirmation</span>' : ''}</div>` : "";
  const actions = message.role === "raphael" ? `<div class="mt-2"><button class="copy" onclick="copyChatResponse(${index})">copy response</button>${hasCode(message.text) ? `<button class="copy" onclick="createFileInstead(${index})">create file instead</button>` : ""}</div>` : "";
  return `<div class="bubble ${cls}"><strong>${who}</strong><div class="mt-1">${body}</div>${command}${status}${meta}${actions}</div>`;
}
function useChatExample(text) {
  const input = document.getElementById("chat-input");
  if (input) {
    input.value = text;
    input.focus();
  }
}
function sendQuickChat(text) {
  const input = document.getElementById("chat-input");
  if (input) {
    input.value = text;
    sendChat();
  } else {
    sendDashboardPhrase(text);
  }
}
function copyChatResponse(index) {
  navigator.clipboard.writeText(chatMessages[index]?.text || "");
}
function createFileInstead(index) {
  const text = chatMessages[index]?.text || "";
  useChatExample("build a file from this response: " + text.slice(0, 300));
}
async function sendChat(options = {}) {
  const input = document.getElementById("chat-input");
  const status = document.getElementById("chat-status");
  const phrase = (input?.value || "").trim();
  if (!phrase) return;
  chatMessages.push({ role: "user", text: phrase });
  input.value = "";
  status.textContent = "Raphael is thinking...";
  setDashboardVoiceState("thinking", options.fromVoice ? "Voice transcript sent through Command Bus." : "Routing through Command Bus…");
  render();
  if (window.RaphaelOrb) window.RaphaelOrb.setState("thinking");
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: phrase })
    });
    const payload = await res.json();
    const meta = `${payload.intent || "unknown"}${payload.confirmation_required ? " · confirmation required" : ""}`;
    chatMessages.push({ role: "raphael", text: payload.response || "No response.", meta, command: payload.command || "", status: payload.status || "", awaiting: !!payload.awaiting_confirmation });
    if (window.RaphaelMatrix) window.RaphaelMatrix.noteCommandResult(payload.response || payload.status || "");
    updateOrbFromChatPayload(payload);
    window.RaphaelOrb?.refreshPresence();
    setDashboardVoiceState("speaking", "Raphael response received.");
    speakDashboardResponse(payload.response || "");
  } catch (err) {
    chatMessages.push({ role: "raphael", text: "Dashboard chat failed safely: " + err, meta: "Error" });
    if (window.RaphaelOrb) window.RaphaelOrb.setState("error");
  }
  render();
  if (!dashboardVoiceSpeakResponses && dashboardVoiceState !== "error") {
    setDashboardVoiceState("speaking", "Raphael response received.");
    setTimeout(() => setDashboardVoiceState("recommendation_ready", "Response ready."), 1400);
  } else {
    setDashboardVoiceState(dashboardVoiceState, dashboardVoiceMessage);
  }
  const log = document.getElementById("chat-log");
  if (log) log.scrollTop = log.scrollHeight;
}
async function sendDashboardPhrase(phrase) {
  if (!phrase) return;
  if (window.RaphaelOrb) window.RaphaelOrb.setState("thinking");
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: phrase })
    });
    const payload = await res.json();
    chatMessages.push({ role: "user", text: phrase });
    chatMessages.push({ role: "raphael", text: payload.response || "No response.", meta: payload.intent || "matrix", command: payload.command || "", status: payload.status || "", awaiting: !!payload.awaiting_confirmation });
    if (window.RaphaelMatrix) window.RaphaelMatrix.noteCommandResult(payload.response || payload.status || "");
    updateOrbFromChatPayload(payload);
    window.RaphaelOrb?.refreshPresence();
  } catch (err) {
    chatMessages.push({ role: "raphael", text: "Dashboard command failed safely: " + err, meta: "Error" });
    if (window.RaphaelOrb) window.RaphaelOrb.setState("error");
  }
  if (window.RaphaelMatrix && document.body.classList.contains("matrix-view")) window.RaphaelMatrix.renderMatrixHome();
}
function updateOrbFromChatPayload(payload) {
  if (!window.RaphaelOrb) return;
  const status = String(payload?.status || "").toLowerCase();
  const response = String(payload?.response || "").toLowerCase();
  if (payload?.awaiting_confirmation || payload?.confirmation_required) {
    window.RaphaelOrb.setState("warning");
    window.RaphaelOrb.setStatusText("CONFIRMATION REQUIRED");
    return;
  }
  if (status.includes("failed") || status.includes("refused") || status.includes("blocked") || response.includes("blocked")) {
    window.RaphaelOrb.setState("error");
    window.RaphaelOrb.setStatusText("ACTION BLOCKED");
    return;
  }
  window.RaphaelOrb.setState("speaking");
  window.RaphaelOrb.setStatusText("RAPHAEL IS RESPONDING");
  setTimeout(() => {
    if (!chatMessages.some(message => message.awaiting)) window.RaphaelOrb?.setState("recommendation_ready");
  }, 1400);
}
function renderCommandBus() {
  const bus = data.command_bus;
  const commands = [
    data.commands.command_bus_status,
    data.commands.command_bus_test,
    data.commands.command_bus_review,
    data.commands.command_list,
    data.commands.command_help
  ];
  return `
    <article class="card full">
      <h2>Command Bus</h2>
      <span class="pill">Enabled ${bus.enabled}</span>
      <span class="pill">Log all routes ${bus.log_all}</span>
      <span class="pill">Write confirmations ${bus.requires_confirmation}</span>
      <span class="pill">Execution ${bus.allow_execution}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('what should I prioritize today')">test: prioritize</button>
        <button class="copy" onclick="sendQuickChat('list councils')">test: councils</button>
        <button class="copy" onclick="sendQuickChat('which business should I focus on')">test: portfolio</button>
        <button class="copy" onclick="sendQuickChat('send email to client')">test: blocked</button>
      </div>
      <p class="muted mt-3">Central routing and logging only. No safety boundary is weakened; writes, delegation, execution, finance updates, KPI updates, and builder actions still require confirmation.</p>
    </article>
    <article class="card wide"><h2>Command Registry</h2>${bus.registry.exists ? `<div class="muted">${esc(bus.registry.updated)}</div><pre>${esc(bus.registry.content)}</pre>` : `<div class="empty">No command registry yet.</div>`}</article>
    <article class="card wide"><h2>Command Safety Policy</h2>${bus.safety.exists ? `<div class="muted">${esc(bus.safety.updated)}</div><pre>${esc(bus.safety.content)}</pre>` : `<div class="empty">No safety policy yet.</div>`}</article>
    <article class="card wide"><h2>Command Review</h2>${bus.review.exists ? `<div class="muted">${esc(bus.review.updated)}</div><pre>${esc(bus.review.content)}</pre>` : `<div class="empty">No command review yet.</div>`}</article>
    <article class="card wide"><h2>Command Routing Log</h2>${bus.routing_log.exists ? `<div class="muted">${esc(bus.routing_log.updated)}</div><pre>${esc(bus.routing_log.content)}</pre>` : `<div class="empty">No routing log yet.</div>`}</article>
    <article class="card wide"><h2>Command Bus Overview</h2>${bus.overview.exists ? `<div class="muted">${esc(bus.overview.updated)}</div><pre>${esc(bus.overview.content)}</pre>` : `<div class="empty">No overview yet.</div>`}</article>
  `;
}
function renderProjects() {
  return card("Projects", table(data.projects, [
    ["Project", "name"], ["Status", "status", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
    ["Score", "score", v=>v ? `<div>${v}/100</div><div class="bar"><i style="width:${v}%"></i></div>` : "n/a"],
    ["Summary", "has_summary", v=>v ? "yes" : "no"], ["Health", "has_health", v=>v ? "yes" : "no"]
  ]), "card full");
}
function renderBuilder() {
  const rows = data.build_requests || [];
  return `
    <article class="card full">
      <h2>Builder Mode</h2>
      <p class="muted">Sandbox-first app/file generation. Builder files are created under <code>R:/RaphaelOS/builder/workspace</code> first.</p>
      <button class="copy" onclick="copyCommand('${esc(data.commands.build_classify)}')">${esc(data.commands.build_classify)}</button>
      <button class="copy" onclick="copyCommand('${esc(data.commands.build_with_council)}')">${esc(data.commands.build_with_council)}</button>
      <button class="copy" onclick="copyCommand('${esc(data.commands.build_review)}')">${esc(data.commands.build_review)}</button>
      <button class="copy" onclick="copyCommand('${esc(data.commands.builder_governance_review)}')">${esc(data.commands.builder_governance_review)}</button>
      <button class="copy" onclick="sendQuickChat('build a Python app that tracks button clicks')">chat: build click tracker</button>
    </article>
    <article class="card full">
      <h2>Build Requests</h2>
      ${table(rows, [
        ["ID","id"],
        ["Complexity","complexity",v=>v ? `<span class="${statusClass(v)}">${esc(v)}</span>` : "unclassified"],
        ["Task ID","task_id",v=>v ? `<code>${esc(v)}</code>` : "unlinked"],
        ["Task Set","task_set",v=>v ? `<code>${esc(v)}</code>` : "n/a"],
        ["Task Status","task_status",v=>v ? `<span class="${statusClass(v)}">${esc(v)}</span>` : "unknown"],
        ["Agent","assigned_agent"],
        ["Councils","councils"],
        ["Deliberation","deliberation_id",v=>v ? `<code>${esc(v)}</code>` : "n/a"],
        ["Execution Plan","execution_plan_id",v=>v ? `<code>${esc(v)}</code>` : "n/a"],
        ["Safety","safety_status"],
        ["Next Command","next_command",v=>v ? `<code>${esc(v)}</code>` : "n/a"],
        ["Description","description"],
        ["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Workspace","workspace",v=>v ? `<code>${esc(v)}</code>` : "n/a"],
        ["Created","created"]
      ])}
    </article>
    <article class="card full">
      <h2>Build Governance & Files</h2>
      ${rows.length ? rows.map(r => `<div class="bubble raphael"><strong>${esc(r.id)}</strong><div class="mt-1"><span class="pill">${esc(r.complexity || "Unclassified")}</span><span class="pill">Task ${esc(r.task_id || "unlinked")}</span><span class="pill">${esc(r.task_status || "unknown")}</span><span class="pill">${esc(r.safety_status || "sandbox only")}</span></div><div class="muted mt-2">${esc(r.councils || "No councils required")}</div>${r.files ? `<pre class="mt-2">${esc(r.files)}</pre>` : `<div class="empty mt-2">No generated files yet.</div>`}<button class="copy" onclick="quickBuildAction('classify','${esc(r.id)}')">Classify build</button><button class="copy" onclick="quickBuildAction('plan','${esc(r.id)}')">Council plan</button><button class="copy" ${String(r.complexity).startsWith("3") && r.status === "Awaiting Plan Approval" ? `onclick="quickBuildAction('approve','${esc(r.id)}')"` : "disabled"}>Approve council plan</button><button class="copy" ${!r.files && (!String(r.complexity).startsWith("3") || r.status === "Approved") ? `onclick="quickBuildAction('generate','${esc(r.id)}')"` : "disabled"}>Generate after approval</button><button class="copy" ${r.task_id ? `onclick="openRelatedTask('${esc(r.task_id)}')"` : "disabled"}>Open related task</button><button class="copy" ${r.deliberation_id ? `onclick="active='deliberations'; render();"` : "disabled"}>Open deliberation</button><button class="copy" ${r.execution_plan_id ? `onclick="active='executionplans'; render();"` : "disabled"}>Open execution plan</button><button class="copy" ${r.files ? `onclick="sendQuickChat('mark build ${esc(r.id)} ready for review')"` : "disabled"}>Mark build complete</button></div>`).join("") : `<div class="empty">No Builder requests yet.</div>`}
    </article>
  `;
}
function quickBuildAction(action, buildId) {
  const build = (data.build_requests || []).find(item => item.id === buildId);
  if (!build) return;
  if (action === "classify") sendQuickChat(`classify this build: ${build.description}`);
  if (action === "plan") sendQuickChat(`create council plan for ${build.id}`);
  if (action === "approve") sendQuickChat(`approve council plan for ${build.id}`);
  if (action === "generate") sendQuickChat(`generate build ${build.id}`);
}
function renderIdentity() {
  const identity = data.identity;
  const fileCards = identity.files.map(file => card(file.name.replace(".md", ""), file.exists ? `<div class="muted">${esc(file.updated)}</div><pre>${esc(file.content)}</pre>` : `<div class="empty">Missing identity file: ${esc(file.path)}</div>`, "card wide")).join("");
  return `
    <article class="card full">
      <h2>Identity Layer</h2>
      <span class="pill">Enabled ${identity.enabled}</span>
      <span class="pill">Style ${esc(identity.communication_style)}</span>
      <span class="pill">Length ${esc(identity.response_length_default)}</span>
      <span class="pill">Uncertainty ${identity.always_disclose_uncertainty}</span>
      <span class="pill">Actionable ${identity.prefer_actionable_recommendations}</span>
      <span class="pill">Escalate ${identity.escalate_when_uncertain}</span>
      <div class="mt-3">
        <button class="copy" onclick="copyCommand('${esc(data.commands.identity_status)}')">${esc(data.commands.identity_status)}</button>
        <button class="copy" onclick="copyCommand('${esc(data.commands.identity_review)}')">${esc(data.commands.identity_review)}</button>
        <button class="copy" onclick="copyCommand('${esc(data.commands.identity_brief)}')">${esc(data.commands.identity_brief)}</button>
        <button class="copy" onclick="sendQuickChat('who are you?')">chat: who are you?</button>
        <button class="copy" onclick="sendQuickChat('explain your rules')">chat: explain rules</button>
      </div>
    </article>
    ${fileCards}
  `;
}
function renderWorldModel() {
  const world = data.world_model;
  const records = world.records;
  const commands = [
    data.commands.world_status,
    data.commands.world_review,
    data.commands.world_brief,
    data.commands.add_business,
    data.commands.add_product
  ];
  const recordTable = (rows, includeBusiness=false) => table(rows, [
    ["ID", "id"],
    ["Name", "name"],
    ["Type", "type"],
    ...(includeBusiness ? [["Business", "business"]] : []),
    ["Status", "status", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
    ["Council", "council"],
    ["Description", "description"]
  ]);
  return `
    <article class="card full">
      <h2>World Model</h2>
      <span class="pill">Enabled ${world.enabled}</span>
      <span class="pill">Update confirmation ${world.requires_confirmation}</span>
      <span class="pill">Businesses ${records.business.length}</span>
      <span class="pill">Products ${records.product.length}</span>
      <span class="pill">Revenue ${records.revenue_stream.length}</span>
      <span class="pill">Platforms ${records.platform.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('world status')">chat: world status</button>
        <button class="copy" onclick="sendQuickChat('review the world model')">chat: review world model</button>
        <button class="copy" onclick="sendQuickChat('give me a world brief')">chat: world brief</button>
      </div>
      <p class="muted mt-3">Read-only dashboard view. Add/update world model records through confirmed safe CLI/chat commands only.</p>
    </article>
    <article class="card full"><h2>Businesses</h2>${recordTable(records.business)}</article>
    <article class="card full"><h2>Products</h2>${recordTable(records.product, true)}</article>
    <article class="card full"><h2>Revenue Streams</h2>${recordTable(records.revenue_stream, true)}</article>
    <article class="card full"><h2>Platforms</h2>${recordTable(records.platform)}</article>
    <article class="card full"><h2>Assets</h2>${recordTable(records.asset)}</article>
    <article class="card full"><h2>Relationships</h2>${recordTable(records.relationship)}</article>
    <article class="card wide"><h2>World Review</h2>${world.review.exists ? `<div class="muted">${esc(world.review.updated)}</div><pre>${esc(world.review.content)}</pre>` : `<div class="empty">World review has not been generated yet.</div>`}</article>
    <article class="card wide"><h2>World Brief</h2>${world.brief.exists ? `<div class="muted">${esc(world.brief.updated)}</div><pre>${esc(world.brief.content)}</pre>` : `<div class="empty">World brief has not been generated yet.</div>`}</article>
  `;
}
function renderSimulations() {
  const sim = data.simulations;
  const commands = [
    data.commands.simulation_status,
    data.commands.simulate,
    data.commands.simulate_many,
    data.commands.simulate_business,
    data.commands.compare_opportunities,
    data.commands.simulation_review
  ];
  return `
    <article class="card full">
      <h2>Simulation Engine</h2>
      <span class="pill">Enabled ${sim.enabled}</span>
      <span class="pill">Saved result confirmation ${sim.requires_confirmation}</span>
      <span class="pill">Results ${sim.results.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('simulate Etsy store versus agency')">chat: simulate Etsy vs agency</button>
        <button class="copy" onclick="sendQuickChat('compare AI influencer, Etsy store, and Shopify agency')">chat: compare three</button>
        <button class="copy" onclick="sendQuickChat('compare opportunities')">chat: compare opportunities</button>
      </div>
      <p class="muted mt-3">Advisory scoring only. No business actions, platform access, spending, or external search are performed.</p>
    </article>
    <article class="card full">
      <h2>Recent Simulations</h2>
      ${table(sim.results, [
        ["ID", "id"],
        ["Type", "type"],
        ["Options", "options"],
        ["Recommendation", "recommendation"],
        ["Created", "created"]
      ])}
    </article>
    <article class="card wide">
      <h2>Simulation Criteria</h2>
      ${sim.criteria.exists ? `<div class="muted">${esc(sim.criteria.updated)}</div><pre>${esc(sim.criteria.content)}</pre>` : `<div class="empty">Simulation criteria have not been generated yet.</div>`}
    </article>
    <article class="card wide">
      <h2>Simulation Review</h2>
      ${sim.review.exists ? `<div class="muted">${esc(sim.review.updated)}</div><pre>${esc(sim.review.content)}</pre>` : `<div class="empty">Simulation review has not been generated yet.</div>`}
    </article>
    <article class="card full">
      <h2>Simulation Results Index</h2>
      ${sim.results_index.exists ? `<div class="muted">${esc(sim.results_index.updated)}</div><pre>${esc(sim.results_index.content)}</pre>` : `<div class="empty">No simulation results index yet.</div>`}
    </article>
  `;
}
function renderOpportunities() {
  const opp = data.opportunities;
  const commands = [
    data.commands.opportunity_status,
    data.commands.detect_opportunities,
    data.commands.opportunity_review,
    data.commands.opportunity_brief,
    data.commands.add_opportunity,
    data.commands.score_opportunity,
    data.commands.opportunity_delegate
  ];
  return `
    <article class="card full">
      <h2>Opportunity Detection Engine</h2>
      <span class="pill">Enabled ${opp.enabled}</span>
      <span class="pill">Delegation confirmation ${opp.requires_confirmation}</span>
      <span class="pill">Threshold ${opp.threshold}</span>
      <span class="pill">Opportunities ${opp.records.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('detect opportunities')">chat: detect opportunities</button>
        <button class="copy" onclick="sendQuickChat('review opportunities')">chat: review opportunities</button>
        <button class="copy" onclick="sendQuickChat('brief opportunities')">chat: brief opportunities</button>
      </div>
      <p class="muted mt-3">Recommendation layer only. No store creation, platform access, spending, uploads, external browsing, or automatic delegation.</p>
    </article>
    <article class="card full">
      <h2>Opportunity Inbox</h2>
      ${table(opp.records, [
        ["ID", "id"],
        ["Title", "title"],
        ["Type", "type"],
        ["Score", "score"],
        ["Risk", "risk"],
        ["Status", "status", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Council", "council"],
        ["Next", "next"]
      ])}
    </article>
    <article class="card wide"><h2>Opportunity Scores</h2>${opp.scores.exists ? `<div class="muted">${esc(opp.scores.updated)}</div><pre>${esc(opp.scores.content)}</pre>` : `<div class="empty">No scored opportunities yet.</div>`}</article>
    <article class="card wide"><h2>Opportunity Review</h2>${opp.review.exists ? `<div class="muted">${esc(opp.review.updated)}</div><pre>${esc(opp.review.content)}</pre>` : `<div class="empty">No opportunity review yet.</div>`}</article>
    <article class="card full"><h2>Opportunity Brief</h2>${opp.brief.exists ? `<div class="muted">${esc(opp.brief.updated)}</div><pre>${esc(opp.brief.content)}</pre>` : `<div class="empty">No opportunity brief yet.</div>`}</article>
  `;
}
function renderAllocation() {
  const allocation = data.allocation;
  const p = allocation.profile;
  const commands = [
    data.commands.resource_status,
    data.commands.set_resource_profile,
    data.commands.allocation_plan,
    data.commands.allocation_plan_for,
    data.commands.allocate_next_hours,
    data.commands.allocation_review,
    data.commands.allocation_brief
  ];
  return `
    <article class="card full">
      <h2>Resource Allocation</h2>
      <span class="pill">Enabled ${allocation.enabled}</span>
      <span class="pill">Delegation confirmation ${allocation.requires_confirmation}</span>
      <span class="pill">Hours ${esc(p.weekly_hours)}</span>
      <span class="pill">Budget ${esc(p.weekly_budget)}</span>
      <span class="pill">Focus slots ${esc(p.focus_slots)}</span>
      <span class="pill">Mode ${esc(p.mode)}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('allocate my next 10 hours')">chat: next 10 hours</button>
        <button class="copy" onclick="sendQuickChat('what should I work on this week')">chat: this week</button>
        <button class="copy" onclick="sendQuickChat('make a resource plan')">chat: resource plan</button>
        <button class="copy" onclick="sendQuickChat('allocate resources for print on demand')">chat: print on demand</button>
      </div>
      <p class="muted mt-3">Recommendations only. No spending, task execution, platform access, or external action.</p>
    </article>
    <article class="card wide"><h2>Resource Profile</h2><pre>${esc(JSON.stringify(p, null, 2))}</pre></article>
    <article class="card wide"><h2>Allocation Rules</h2>${allocation.rules.exists ? `<div class="muted">${esc(allocation.rules.updated)}</div><pre>${esc(allocation.rules.content)}</pre>` : `<div class="empty">No allocation rules yet.</div>`}</article>
    <article class="card full"><h2>Allocation Plan</h2>${allocation.plan.exists ? `<div class="muted">${esc(allocation.plan.updated)}</div><pre>${esc(allocation.plan.content)}</pre>` : `<div class="empty">No allocation plan yet.</div>`}</article>
    <article class="card wide"><h2>Allocation Review</h2>${allocation.review.exists ? `<div class="muted">${esc(allocation.review.updated)}</div><pre>${esc(allocation.review.content)}</pre>` : `<div class="empty">No allocation review yet.</div>`}</article>
    <article class="card wide"><h2>Allocation Brief</h2>${allocation.brief.exists ? `<div class="muted">${esc(allocation.brief.updated)}</div><pre>${esc(allocation.brief.content)}</pre>` : `<div class="empty">No allocation brief yet.</div>`}</article>
  `;
}
function renderBlueprints() {
  const bp = data.blueprints;
  const commands = [
    data.commands.blueprint_status,
    data.commands.blueprint_business,
    data.commands.blueprint_review,
    data.commands.blueprint_next_actions,
    data.commands.blueprint_delegate
  ];
  return `
    <article class="card full">
      <h2>Business Blueprints</h2>
      <span class="pill">Enabled ${bp.enabled}</span>
      <span class="pill">Delegation confirmation ${bp.requires_confirmation}</span>
      <span class="pill">Depth ${esc(bp.depth)}</span>
      <span class="pill">Blueprints ${bp.records.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('create a blueprint for a print on demand Etsy store')">chat: Etsy POD blueprint</button>
        <button class="copy" onclick="sendQuickChat('blueprint an AI influencer ebook business')">chat: AI influencer ebook</button>
        <button class="copy" onclick="sendQuickChat('make a business blueprint for a Shopify agency')">chat: Shopify agency</button>
        <button class="copy" onclick="sendQuickChat('review blueprints')">chat: review blueprints</button>
      </div>
      <p class="muted mt-3">Planning only. No store creation, platform access, product upload, spending, outreach, or external browsing.</p>
    </article>
    <article class="card full">
      <h2>Recent Blueprints</h2>
      ${table(bp.records, [
        ["ID", "id"],
        ["Business", "name"],
        ["Type", "type"],
        ["Council", "council"],
        ["Concept", "concept"],
        ["Next", "next"]
      ])}
    </article>
    <article class="card wide"><h2>Blueprint Index</h2>${bp.index.exists ? `<div class="muted">${esc(bp.index.updated)}</div><pre>${esc(bp.index.content)}</pre>` : `<div class="empty">No blueprint index yet.</div>`}</article>
    <article class="card wide"><h2>Blueprint Review</h2>${bp.review.exists ? `<div class="muted">${esc(bp.review.updated)}</div><pre>${esc(bp.review.content)}</pre>` : `<div class="empty">No blueprint review yet.</div>`}</article>
    <article class="card full"><h2>Blueprint Template</h2>${bp.template.exists ? `<div class="muted">${esc(bp.template.updated)}</div><pre>${esc(bp.template.content)}</pre>` : `<div class="empty">No blueprint template yet.</div>`}</article>
  `;
}
function renderCommerce() {
  const commerce = data.commerce;
  const commands = [
    data.commands.commerce_status,
    data.commands.commerce_review,
    data.commands.commerce_brief,
    data.commands.commerce_product_idea,
    data.commands.commerce_listing_plan,
    data.commands.commerce_store_plan,
    data.commands.commerce_digital_product,
    data.commands.commerce_pipeline,
    data.commands.commerce_delegate
  ];
  const noteTable = rows => table(rows, [
    ["Name", "name"],
    ["Idea", "idea"],
    ["Target / Niche", "target"],
    ["Next", "next"],
    ["Updated", "updated"]
  ]);
  return `
    <article class="card full">
      <h2>Commerce Council</h2>
      <span class="pill">Enabled ${commerce.enabled}</span>
      <span class="pill">Delegation confirmation ${commerce.requires_confirmation}</span>
      <span class="pill">No platform actions ${commerce.no_platform_actions}</span>
      <span class="pill">Products ${commerce.pod_ideas.length + commerce.digital_products.length}</span>
      <span class="pill">Listing plans ${commerce.listing_plans.length}</span>
      <div class="mt-2">${commerce.platforms.map(p => `<span class="pill">${esc(p)}</span>`).join("")}</div>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('commerce status')">chat: commerce status</button>
        <button class="copy" onclick="sendQuickChat('commerce review')">chat: commerce review</button>
        <button class="copy" onclick="sendQuickChat('create product idea Bible verse shirt')">chat: product idea</button>
        <button class="copy" onclick="sendQuickChat('make listing plan for Bible verse shirt')">chat: listing plan</button>
        <button class="copy" onclick="sendQuickChat('make store plan for print on demand Etsy store')">chat: store plan</button>
        <button class="copy" onclick="sendQuickChat('create digital product idea AI prompt ebook')">chat: digital product</button>
        <button class="copy" onclick="sendQuickChat('show commerce pipeline')">chat: pipeline</button>
        <button class="copy" onclick="active='podstudio'; render();">Open POD Design Studio</button>
      </div>
      <p class="muted mt-3">Planning and preparation only. No store creation, product upload, platform login, spending, publishing, or external browsing.</p>
    </article>
    <article class="card wide"><h2>Commerce Brief</h2>${commerce.brief.exists ? `<div class="muted">${esc(commerce.brief.updated)}</div><pre>${esc(commerce.brief.content)}</pre>` : `<div class="empty">No commerce brief yet.</div>`}</article>
    <article class="card wide"><h2>Product Pipeline</h2>${commerce.pipeline.exists ? `<div class="muted">${esc(commerce.pipeline.updated)}</div><pre>${esc(commerce.pipeline.content)}</pre>` : `<div class="empty">No commerce pipeline yet.</div>`}</article>
    <article class="card full"><h2>POD Ideas</h2>${noteTable(commerce.pod_ideas)}</article>
    <article class="card full"><h2>Listing Plans</h2>${noteTable(commerce.listing_plans)}</article>
    <article class="card full"><h2>Store Plans</h2>${noteTable(commerce.store_plans)}</article>
    <article class="card full"><h2>Digital Products</h2>${noteTable(commerce.digital_products)}</article>
    <article class="card wide"><h2>Commerce Review</h2>${commerce.review.exists ? `<div class="muted">${esc(commerce.review.updated)}</div><pre>${esc(commerce.review.content)}</pre>` : `<div class="empty">No commerce review yet.</div>`}</article>
    <article class="card wide"><h2>Task Board</h2>${commerce.task_board.exists ? `<div class="muted">${esc(commerce.task_board.updated)}</div><pre>${esc(commerce.task_board.content)}</pre>` : `<div class="empty">No commerce task board yet.</div>`}</article>
    <article class="card wide"><h2>Strategy</h2>${commerce.strategy.exists ? `<div class="muted">${esc(commerce.strategy.updated)}</div><pre>${esc(commerce.strategy.content)}</pre>` : `<div class="empty">No commerce strategy yet.</div>`}</article>
    <article class="card wide"><h2>KPI Draft</h2>${commerce.kpis.exists ? `<div class="muted">${esc(commerce.kpis.updated)}</div><pre>${esc(commerce.kpis.content)}</pre>` : `<div class="empty">No commerce KPI draft yet.</div>`}</article>
  `;
}
function renderPODStudio() {
  const pod = data.pod_design_studio;
  const commands = ["pod_status","pod_tool_status","pod_comfyui_test","pod_generation_log","pod_generation_debug","pod_concept","pod_prompt","pod_generation_request","pod_generate","pod_review_design","pod_review_batch","pod_refactor_plan","pod_remove_background","pod_upscale","pod_typography_create","pod_compose_design","pod_svg_export","pod_print_export","pod_typography_review","pod_typography_status","pod_listing_draft","pod_export_package","pod_pipeline","pod_review","pod_brief"];
  const concept = pod.concepts[0]?.id || "";
  const request = pod.requests[0] || {};
  const generatedFolder = request.output_folder || (request.id ? `${pod.runtime}/generated/${request.id}` : `${pod.runtime}/generated`);
  const typography = pod.typography || {assets:[],compositions:[],svg_exports:[],print_exports:[]};
  const typeAsset = typography.assets[0] || {};
  const composition = typography.compositions[0] || {};
  const generatedImage = pod.generated[0]?.path || "";
  return `
    <article class="card full">
      <h2>POD Design Studio</h2>
      <span class="pill">Enabled ${pod.enabled}</span>
      <span class="pill">Concepts ${pod.concepts.length}</span>
      <span class="pill">Requests ${pod.requests.length}</span>
      <span class="pill">Generated assets ${pod.generated.length}</span>
      <span class="pill">Reviews ${pod.reviews.length}</span>
      <span class="pill">Publishing ${pod.safety.publishing}</span>
      <div class="mt-3">${commands.map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}</div>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('pod status')">chat: status</button>
        <button class="copy" onclick="sendQuickChat('create pod concept Christian mountain cross shirt')">chat: concept</button>
        <button class="copy" onclick="sendQuickChat('generate pod prompt')">chat: prompt</button>
        <button class="copy" onclick="sendQuickChat('show pod pipeline')">chat: pipeline</button>
        <button class="copy" onclick="sendQuickChat('create pod listing draft')">chat: listing</button>
      </div>
      <h3 class="mt-3">POD Pipeline Quick Actions</h3>
      <div>
        <button class="copy" ${concept ? `onclick="sendQuickChat('generate pod prompt ${esc(concept)}')"` : "disabled"}>1. Generate Prompt</button>
        <button class="copy" ${concept ? `onclick="sendQuickChat('create pod generation request ${esc(concept)} sdxl')"` : "disabled"}>2. Create SDXL Request</button>
        <button class="copy" ${concept ? `onclick="sendQuickChat('create pod generation request ${esc(concept)} flux')"` : "disabled"}>3. Create Flux Request</button>
        <button class="copy" ${request.id ? `onclick="sendQuickChat('generate pod design ${esc(request.id)}')"` : "disabled"}>4. Generate Designs</button>
        <button class="copy" ${request.image_count > 0 ? `onclick="sendQuickChat('review pod batch ${esc(generatedFolder.replace(/\\/g, "\\\\"))}')"` : "disabled"}>5. Review Batch</button>
        <button class="copy" onclick="sendQuickChat('create typography')">6. Create Typography</button>
        <button class="copy" ${generatedImage && typeAsset.id ? `onclick="sendQuickChat('compose pod design ${esc(generatedImage.replace(/\\/g, "\\\\"))} ${esc(typeAsset.id)}')"` : "disabled"}>7. Compose Design</button>
        <button class="copy" ${composition.id ? `onclick="sendQuickChat('export SVG ${esc(composition.id)}')"` : "disabled"}>8. Export SVG</button>
        <button class="copy" ${composition.id ? `onclick="sendQuickChat('export print-ready design ${esc(composition.id)}')"` : "disabled"}>9. Export Print File</button>
        <button class="copy" ${concept ? `onclick="sendQuickChat('create pod listing draft ${esc(concept)}')"` : "disabled"}>10. Create Listing Draft</button>
        <button class="copy" ${concept ? `onclick="sendQuickChat('export pod package ${esc(concept)}')"` : "disabled"}>11. Export Package</button>
      </div>
      <p class="muted mt-3">Local production only. Generation, tool execution, and export require confirmation. No Etsy/Printify action, credentials, spending, or external APIs.</p>
    </article>
    <article class="card wide"><h2>Tool Status</h2><pre>${esc(pod.tools.content)}</pre></article>
    <article class="card wide"><h2>Product Pipeline</h2><pre>${esc(pod.pipeline.content)}</pre></article>
    <article class="card full"><h2>Concepts</h2>${table(pod.concepts, [["ID","id"],["Idea","name"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card full"><h2>Design Prompts</h2>${table(pod.prompts, [["Concept","id"],["Name","name"],["Updated","updated"]])}</article>
    <article class="card full"><h2>Generation Requests</h2>${table(pod.requests, [["ID","id"],["Concept","concept"],["Model","model"],["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],["Prompt ID","prompt_id"],["Images","image_count"],["Output Folder","output_folder"],["Error","error"],["Updated","updated"]])}</article>
    <article class="card full"><h2>ComfyUI Output Bridge</h2>
      <div><strong>Open generated folder:</strong> <code>${esc(generatedFolder)}</code></div>
      ${request.status === "Generated" && !request.image_count ? `<div class="bad mt-3">Generation is marked Generated but the output folder is empty. Run the generation log diagnostic.</div>` : ""}
      ${request.error && request.error !== "None" ? `<pre class="bad mt-3">${esc(request.error)}</pre>` : ""}
      <button class="copy" onclick="sendQuickChat('test pod comfyui')">Run ComfyUI diagnostic</button>
      ${request.id ? `<button class="copy" onclick="sendQuickChat('show pod generation log ${esc(request.id)}')">Show generation log</button>` : ""}
      ${request.id && request.error && request.error !== "None" ? `<button class="copy" onclick="copyCommand('${esc(request.debug_command)}')">Copy generation debug command</button>
        <details class="mt-3"><summary>Generation debug files</summary>
          <div><strong>Submitted payload:</strong> <code>${esc(request.submitted_payload)}</code></div>
          <div><strong>ComfyUI error:</strong> <code>${esc(request.comfyui_error_file)}</code></div>
        </details>` : ""}
      ${pod.comfyui_diagnostic.content ? `<pre>${esc(pod.comfyui_diagnostic.content)}</pre>` : ""}
    </article>
    <article class="card full"><h2>Generated Variants</h2>${table(pod.generated, [["File","name"],["Path","path"],["Bytes","size"]])}</article>
    <article class="card full">
      <h2>Typography & Composition Engine</h2>
      <span class="pill">Enabled ${typography.enabled}</span>
      <span class="pill">Inkscape ${typography.inkscape_enabled}</span>
      <span class="pill">Typography ${typography.assets.length}</span>
      <span class="pill">Compositions ${typography.compositions.length}</span>
      <span class="pill">SVG exports ${typography.svg_exports.length}</span>
      <span class="pill">Print exports ${typography.print_exports.length}</span>
      <div class="muted mt-3">Configured Inkscape: ${esc(typography.inkscape_path || "Not configured")}</div>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('create typography')">Create Typography</button>
        <button class="copy" ${generatedImage && typeAsset.id ? `onclick="sendQuickChat('compose pod design ${esc(generatedImage.replace(/\\/g, "\\\\"))} ${esc(typeAsset.id)}')"` : "disabled"}>Compose Design</button>
        <button class="copy" ${composition.id ? `onclick="sendQuickChat('export SVG ${esc(composition.id)}')"` : "disabled"}>Export SVG</button>
        <button class="copy" ${composition.id ? `onclick="sendQuickChat('export print-ready design ${esc(composition.id)}')"` : "disabled"}>Export Print-Ready PNG</button>
        <button class="copy" onclick="sendQuickChat('typography review')">Review Typography</button>
      </div>
    </article>
    <article class="card full"><h2>Typography Assets</h2>${table(typography.assets, [["ID","id"],["Phrase","name"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card full"><h2>Compositions</h2>${table(typography.compositions, [["ID","id"],["Concept","concept"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card wide"><h2>SVG Exports</h2>${table(typography.svg_exports, [["Composition","id"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card wide"><h2>Print Exports</h2>${table(typography.print_exports, [["Composition","id"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card wide"><h2>Typography Review</h2><pre>${esc(typography.reviews.content)}</pre></article>
    <article class="card wide"><h2>Composition Reviews</h2><pre>${esc(typography.composition_reviews.content)}</pre></article>
    <article class="card full"><h2>Design Reviews</h2>${table(pod.reviews, [["ID","id"],["Score","score"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card full"><h2>Listing Drafts</h2>${table(pod.listings, [["Concept","id"],["Name","name"],["Updated","updated"]])}</article>
    <article class="card full"><h2>Export Packages</h2>${table(pod.exports, [["Concept","id"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card wide"><h2>Studio Review</h2><pre>${esc(pod.review.content)}</pre></article>
    <article class="card wide"><h2>Studio Brief</h2><pre>${esc(pod.brief.content)}</pre></article>`;
}
function renderAssetLibrary() {
  const lib = data.asset_brand_library;
  const commands = ["asset_status","brand_create","brand_review","brand_brief","brand_show","asset_import","asset_review","asset_search","asset_related","asset_tag","asset_export","prompt_library","template_library","design_system_review"];
  return `
    <article class="card full">
      <h2>Asset & Brand Library</h2>
      <span class="pill">Enabled ${lib.enabled}</span>
      <span class="pill">Brands ${lib.brands.length}</span>
      <span class="pill">Assets ${lib.assets.length}</span>
      <span class="pill">Import confirmation ${lib.safety.import_confirmation}</span>
      <span class="pill">Export confirmation ${lib.safety.export_confirmation}</span>
      <span class="pill">Image memory ${lib.safety.memory_images}</span>
      <div class="mt-3">${commands.map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}</div>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('show asset library')">chat: asset library</button>
        <button class="copy" onclick="sendQuickChat('create brand New Brand')">chat: create brand</button>
        <button class="copy" onclick="sendQuickChat('show prompt library')">chat: prompts</button>
        <button class="copy" onclick="sendQuickChat('show templates')">chat: templates</button>
        <button class="copy" onclick="sendQuickChat('review brand')">chat: brand review</button>
      </div>
      <p class="muted mt-3">Metadata-first local reuse. Originals remain unchanged; no upload, publishing, cloud sync, credentials, or spending.</p>
    </article>
    <article class="card wide"><h2>Brand Registry</h2><pre>${esc(lib.brand_registry.content)}</pre></article>
    <article class="card wide"><h2>Asset Registry</h2><pre>${esc(lib.asset_registry.content)}</pre></article>
    <article class="card full"><h2>Brands</h2>${table(lib.brands, [["ID","id"],["Name","name"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card full"><h2>Visual Asset Explorer</h2>${table(lib.assets, [["ID","id"],["Name","name"],["Type","type"],["Tags","tags"],["Status","status"],["Updated","updated"]])}</article>
    <article class="card wide"><h2>Prompt Library</h2><pre>${esc(lib.prompt_library.content)}</pre></article>
    <article class="card wide"><h2>Template Library</h2><pre>${esc(lib.template_library.content)}</pre></article>
    <article class="card wide"><h2>Design Systems</h2><pre>${esc(lib.design_systems.content)}</pre></article>
    <article class="card wide"><h2>Asset Relationships & Reviews</h2><pre>${esc(lib.asset_review.content)}</pre></article>
    <article class="card full"><h2>Asset Reviews</h2>${table(lib.reviews, [["ID","id"],["Name","name"],["Status","status"],["Updated","updated"]])}</article>`;
}
function renderAgency() {
  const agency = data.agency;
  const commands = [
    data.commands.agency_status,
    data.commands.agency_review,
    data.commands.agency_brief,
    data.commands.agency_service_offer,
    data.commands.agency_client_profile,
    data.commands.agency_proposal_plan,
    data.commands.agency_delivery_plan,
    data.commands.agency_pipeline,
    data.commands.agency_delegate
  ];
  const noteTable = rows => table(rows, [
    ["Name", "name"],
    ["Subject", "subject"],
    ["Target / Context", "target"],
    ["Next", "next"],
    ["Updated", "updated"]
  ]);
  return `
    <article class="card full">
      <h2>Agency Council</h2>
      <span class="pill">Enabled ${agency.enabled}</span>
      <span class="pill">Delegation confirmation ${agency.requires_confirmation}</span>
      <span class="pill">No external outreach ${agency.no_external_outreach}</span>
      <span class="pill">Service offers ${agency.service_offers.length}</span>
      <span class="pill">Client profiles ${agency.client_profiles.length}</span>
      <span class="pill">Proposals ${agency.proposal_plans.length}</span>
      <span class="pill">Delivery plans ${agency.delivery_plans.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('agency status')">chat: agency status</button>
        <button class="copy" onclick="sendQuickChat('agency review')">chat: agency review</button>
        <button class="copy" onclick="sendQuickChat('create service offer Shopify Integration')">chat: service offer</button>
        <button class="copy" onclick="sendQuickChat('create proposal plan ERP integration')">chat: proposal plan</button>
        <button class="copy" onclick="sendQuickChat('create client profile local retailer')">chat: client profile</button>
        <button class="copy" onclick="sendQuickChat('show agency pipeline')">chat: pipeline</button>
      </div>
      <p class="muted mt-3">Planning and management only. No outreach, emails, CRM access, contracts, invoicing, payment processing, spending, external APIs, or external systems.</p>
    </article>
    <article class="card wide"><h2>Agency Brief</h2>${agency.brief.exists ? `<div class="muted">${esc(agency.brief.updated)}</div><pre>${esc(agency.brief.content)}</pre>` : `<div class="empty">No agency brief yet.</div>`}</article>
    <article class="card wide"><h2>Agency Pipeline</h2>${agency.pipeline.exists ? `<div class="muted">${esc(agency.pipeline.updated)}</div><pre>${esc(agency.pipeline.content)}</pre>` : `<div class="empty">No agency pipeline yet.</div>`}</article>
    <article class="card full"><h2>Service Offers</h2>${noteTable(agency.service_offers)}</article>
    <article class="card full"><h2>Client Profiles</h2>${noteTable(agency.client_profiles)}</article>
    <article class="card full"><h2>Proposal Plans</h2>${noteTable(agency.proposal_plans)}</article>
    <article class="card full"><h2>Delivery Plans</h2>${noteTable(agency.delivery_plans)}</article>
    <article class="card wide"><h2>Agency Review</h2>${agency.review.exists ? `<div class="muted">${esc(agency.review.updated)}</div><pre>${esc(agency.review.content)}</pre>` : `<div class="empty">No agency review yet.</div>`}</article>
    <article class="card wide"><h2>Task Board</h2>${agency.task_board.exists ? `<div class="muted">${esc(agency.task_board.updated)}</div><pre>${esc(agency.task_board.content)}</pre>` : `<div class="empty">No agency task board yet.</div>`}</article>
    <article class="card wide"><h2>Service Catalog</h2>${agency.catalog.exists ? `<div class="muted">${esc(agency.catalog.updated)}</div><pre>${esc(agency.catalog.content)}</pre>` : `<div class="empty">No agency service catalog yet.</div>`}</article>
    <article class="card wide"><h2>KPI Draft</h2>${agency.kpis.exists ? `<div class="muted">${esc(agency.kpis.updated)}</div><pre>${esc(agency.kpis.content)}</pre>` : `<div class="empty">No agency KPI draft yet.</div>`}</article>
  `;
}
function renderCreator() {
  const creator = data.creator;
  const commands = [
    data.commands.creator_status,
    data.commands.creator_review,
    data.commands.creator_brief,
    data.commands.creator_content_idea,
    data.commands.creator_content_plan,
    data.commands.creator_script,
    data.commands.creator_ebook_plan,
    data.commands.creator_offer_plan,
    data.commands.creator_pipeline,
    data.commands.creator_delegate
  ];
  const noteTable = rows => table(rows, [
    ["Name", "name"],
    ["Subject", "subject"],
    ["Audience / Pillar", "audience"],
    ["Next", "next"],
    ["Updated", "updated"]
  ]);
  return `
    <article class="card full">
      <h2>Creator Council</h2>
      <span class="pill">Enabled ${creator.enabled}</span>
      <span class="pill">Delegation confirmation ${creator.requires_confirmation}</span>
      <span class="pill">No publishing ${creator.no_publishing}</span>
      <span class="pill">Ideas ${creator.content_ideas.length}</span>
      <span class="pill">Plans ${creator.content_plans.length}</span>
      <span class="pill">Scripts ${creator.scripts.length}</span>
      <span class="pill">Ebooks ${creator.ebooks.length}</span>
      <span class="pill">Offers ${creator.offers.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('creator status')">chat: creator status</button>
        <button class="copy" onclick="sendQuickChat('creator review')">chat: creator review</button>
        <button class="copy" onclick="sendQuickChat('create content idea AI automation tips')">chat: content idea</button>
        <button class="copy" onclick="sendQuickChat('create content plan AI automation tips')">chat: content plan</button>
        <button class="copy" onclick="sendQuickChat('create script AI automation tips')">chat: script</button>
        <button class="copy" onclick="sendQuickChat('create ebook plan AI automation for local businesses')">chat: ebook</button>
        <button class="copy" onclick="sendQuickChat('show creator pipeline')">chat: pipeline</button>
      </div>
      <p class="muted mt-3">Planning only. No posting, uploads, email sends, social account access, platform logins, account creation, or publishing.</p>
    </article>
    <article class="card wide"><h2>Creator Brief</h2>${creator.brief.exists ? `<div class="muted">${esc(creator.brief.updated)}</div><pre>${esc(creator.brief.content)}</pre>` : `<div class="empty">No creator brief yet.</div>`}</article>
    <article class="card wide"><h2>Creator Pipeline</h2>${creator.pipeline.exists ? `<div class="muted">${esc(creator.pipeline.updated)}</div><pre>${esc(creator.pipeline.content)}</pre>` : `<div class="empty">No creator pipeline yet.</div>`}</article>
    <article class="card full"><h2>Content Ideas</h2>${noteTable(creator.content_ideas)}</article>
    <article class="card full"><h2>Content Plans</h2>${noteTable(creator.content_plans)}</article>
    <article class="card full"><h2>Scripts</h2>${noteTable(creator.scripts)}</article>
    <article class="card full"><h2>Ebooks</h2>${noteTable(creator.ebooks)}</article>
    <article class="card full"><h2>Offers</h2>${noteTable(creator.offers)}</article>
    <article class="card wide"><h2>Creator Review</h2>${creator.review.exists ? `<div class="muted">${esc(creator.review.updated)}</div><pre>${esc(creator.review.content)}</pre>` : `<div class="empty">No creator review yet.</div>`}</article>
    <article class="card wide"><h2>Task Board</h2>${creator.task_board.exists ? `<div class="muted">${esc(creator.task_board.updated)}</div><pre>${esc(creator.task_board.content)}</pre>` : `<div class="empty">No creator task board yet.</div>`}</article>
    <article class="card wide"><h2>Content Calendar</h2>${creator.calendar.exists ? `<div class="muted">${esc(creator.calendar.updated)}</div><pre>${esc(creator.calendar.content)}</pre>` : `<div class="empty">No creator content calendar yet.</div>`}</article>
    <article class="card wide"><h2>KPI Draft</h2>${creator.kpis.exists ? `<div class="muted">${esc(creator.kpis.updated)}</div><pre>${esc(creator.kpis.content)}</pre>` : `<div class="empty">No creator KPI draft yet.</div>`}</article>
  `;
}
function renderKPIs() {
  const kpis = data.kpis;
  const commands = [
    data.commands.kpi_status,
    data.commands.kpi_dashboard,
    data.commands.kpi_review,
    data.commands.kpi_brief,
    data.commands.kpi_add,
    data.commands.kpi_update,
    data.commands.kpi_history
  ];
  return `
    <article class="card full">
      <h2>KPI System</h2>
      <span class="pill">Enabled ${kpis.enabled}</span>
      <span class="pill">Update confirmation ${kpis.requires_confirmation}</span>
      <span class="pill">External collection ${kpis.auto_external}</span>
      <span class="pill">KPIs ${kpis.records.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('show KPI dashboard')">chat: dashboard</button>
        <button class="copy" onclick="sendQuickChat('review KPIs')">chat: review</button>
        <button class="copy" onclick="sendQuickChat('add KPI monthly agency revenue target 1000')">chat: add KPI</button>
      </div>
      <p class="muted mt-3">Reporting only. No external metric collection, financial access, platform access, spending, publishing, uploads, messages, or business execution.</p>
    </article>
    <article class="card full">
      <h2>KPI Registry</h2>
      ${table(kpis.records, [
        ["ID", "id"],
        ["Name", "name"],
        ["Category", "category"],
        ["Owner", "owner"],
        ["Current", "current"],
        ["Target", "target"],
        ["Status", "status", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Updated", "updated"]
      ])}
    </article>
    <article class="card wide"><h2>KPI Dashboard</h2>${kpis.dashboard.exists ? `<div class="muted">${esc(kpis.dashboard.updated)}</div><pre>${esc(kpis.dashboard.content)}</pre>` : `<div class="empty">No KPI dashboard yet.</div>`}</article>
    <article class="card wide"><h2>KPI Review</h2>${kpis.review.exists ? `<div class="muted">${esc(kpis.review.updated)}</div><pre>${esc(kpis.review.content)}</pre>` : `<div class="empty">No KPI review yet.</div>`}</article>
    <article class="card wide"><h2>KPI Brief</h2>${kpis.brief.exists ? `<div class="muted">${esc(kpis.brief.updated)}</div><pre>${esc(kpis.brief.content)}</pre>` : `<div class="empty">No KPI brief yet.</div>`}</article>
    <article class="card wide"><h2>KPI Targets</h2>${kpis.targets.exists ? `<div class="muted">${esc(kpis.targets.updated)}</div><pre>${esc(kpis.targets.content)}</pre>` : `<div class="empty">No KPI targets yet.</div>`}</article>
    <article class="card full"><h2>KPI History</h2>${kpis.history.exists ? `<div class="muted">${esc(kpis.history.updated)}</div><pre>${esc(kpis.history.content)}</pre>` : `<div class="empty">No KPI history yet.</div>`}</article>
  `;
}
function renderFinance() {
  const finance = data.finance;
  const commands = [
    data.commands.finance_status,
    data.commands.finance_summary,
    data.commands.finance_review,
    data.commands.finance_brief,
    data.commands.finance_forecast,
    data.commands.finance_add_revenue,
    data.commands.finance_add_expense,
    data.commands.finance_budget,
    data.commands.finance_history
  ];
  const fmt = value => `${esc(finance.currency)} ${Number(value || 0).toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
  return `
    <article class="card full">
      <h2>Financial Intelligence</h2>
      <span class="pill">Enabled ${finance.enabled}</span>
      <span class="pill">Update confirmation ${finance.requires_confirmation}</span>
      <span class="pill">External accounts ${finance.external_accounts}</span>
      <span class="pill">Currency ${esc(finance.currency)}</span>
      <span class="pill">Entries ${finance.records.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('show financial summary')">chat: summary</button>
        <button class="copy" onclick="sendQuickChat('review finances')">chat: review</button>
        <button class="copy" onclick="sendQuickChat('financial forecast')">chat: forecast</button>
        <button class="copy" onclick="sendQuickChat('add revenue Agency 500 Shopify setup')">chat: add revenue</button>
        <button class="copy" onclick="sendQuickChat('add expense Commerce 25 Etsy listing tools')">chat: add expense</button>
        <button class="copy" onclick="sendQuickChat('set budget Creator 100')">chat: set budget</button>
      </div>
      <p class="muted mt-3">Manual local tracking only. No bank connections, payment processor access, invoices, tax filing, purchases, money movement, external APIs, or platform actions.</p>
    </article>
    <article class="card"><h2>Total Revenue</h2><div class="stat">${fmt(finance.totals.revenue)}</div></article>
    <article class="card"><h2>Total Expenses</h2><div class="stat">${fmt(finance.totals.expenses)}</div></article>
    <article class="card"><h2>Net Profit/Loss</h2><div class="stat">${fmt(finance.totals.net)}</div></article>
    <article class="card"><h2>Budgets</h2><div class="stat">${fmt(finance.totals.budgets)}</div></article>
    <article class="card full">
      <h2>Financial Ledger</h2>
      ${table(finance.records, [
        ["ID", "id"],
        ["Date", "date"],
        ["Type", "type", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Business", "business"],
        ["Amount", "amount", v=>fmt(v)],
        ["Description", "description"],
        ["Category", "category"],
        ["KPI", "kpi"],
        ["Initiative", "initiative"]
      ])}
    </article>
    <article class="card wide"><h2>Profit Summary</h2>${finance.profit.exists ? `<div class="muted">${esc(finance.profit.updated)}</div><pre>${esc(finance.profit.content)}</pre>` : `<div class="empty">No profit summary yet.</div>`}</article>
    <article class="card wide"><h2>Revenue Tracker</h2>${finance.revenue.exists ? `<div class="muted">${esc(finance.revenue.updated)}</div><pre>${esc(finance.revenue.content)}</pre>` : `<div class="empty">No revenue tracker yet.</div>`}</article>
    <article class="card wide"><h2>Expense Tracker</h2>${finance.expenses.exists ? `<div class="muted">${esc(finance.expenses.updated)}</div><pre>${esc(finance.expenses.content)}</pre>` : `<div class="empty">No expense tracker yet.</div>`}</article>
    <article class="card wide"><h2>Budget Plan</h2>${finance.budget.exists ? `<div class="muted">${esc(finance.budget.updated)}</div><pre>${esc(finance.budget.content)}</pre>` : `<div class="empty">No budget plan yet.</div>`}</article>
    <article class="card wide"><h2>Financial Review</h2>${finance.review.exists ? `<div class="muted">${esc(finance.review.updated)}</div><pre>${esc(finance.review.content)}</pre>` : `<div class="empty">No financial review yet.</div>`}</article>
    <article class="card wide"><h2>Financial Brief</h2>${finance.brief.exists ? `<div class="muted">${esc(finance.brief.updated)}</div><pre>${esc(finance.brief.content)}</pre>` : `<div class="empty">No financial brief yet.</div>`}</article>
    <article class="card wide"><h2>Financial Forecast</h2>${finance.forecast.exists ? `<div class="muted">${esc(finance.forecast.updated)}</div><pre>${esc(finance.forecast.content)}</pre>` : `<div class="empty">No financial forecast yet.</div>`}</article>
  `;
}
function renderPortfolio() {
  const portfolio = data.portfolio;
  const commands = [
    data.commands.portfolio_status,
    data.commands.portfolio_scorecard,
    data.commands.portfolio_review,
    data.commands.portfolio_brief,
    data.commands.portfolio_roadmap,
    data.commands.portfolio_compare,
    data.commands.portfolio_prioritize,
    data.commands.portfolio_decision,
    data.commands.portfolio_delegate
  ];
  return `
    <article class="card full">
      <h2>Business Portfolio Manager</h2>
      <span class="pill">Enabled ${portfolio.enabled}</span>
      <span class="pill">Delegation confirmation ${portfolio.requires_confirmation}</span>
      <span class="pill">Business lines ${portfolio.records.length}</span>
      <span class="pill">Top focus ${esc(portfolio.top.business || "Unknown")}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('portfolio review')">chat: review</button>
        <button class="copy" onclick="sendQuickChat('portfolio brief')">chat: brief</button>
        <button class="copy" onclick="sendQuickChat('portfolio scorecard')">chat: scorecard</button>
        <button class="copy" onclick="sendQuickChat('portfolio roadmap')">chat: roadmap</button>
        <button class="copy" onclick="sendQuickChat('which business should I focus on')">chat: focus</button>
        <button class="copy" onclick="sendQuickChat('compare Agency and Commerce')">chat: compare</button>
        <button class="copy" onclick="sendQuickChat('record portfolio decision focus on Agency this week')">chat: decision</button>
      </div>
      <p class="muted mt-3">Analysis and recommendation only. No business execution, spending, outreach, publishing, uploads, platform access, or external APIs.</p>
    </article>
    <article class="card full">
      <h2>Portfolio Scorecard</h2>
      ${table(portfolio.records, [
        ["Recommendation ID", "id"],
        ["Business", "business"],
        ["Council", "council"],
        ["Focus", "score", v=>v ? `<div>${esc(v)}/100</div><div class="bar"><i style="width:${esc(v)}%"></i></div>` : "n/a"],
        ["Revenue", "revenue"],
        ["Expenses", "expenses"],
        ["Profit", "profit"],
        ["Potential", "potential"],
        ["Speed", "speed"],
        ["Strategic", "strategic"],
        ["Momentum", "momentum"],
        ["Recommended Action", "action"]
      ])}
    </article>
    <article class="card wide"><h2>Portfolio Brief</h2>${portfolio.brief.exists ? `<div class="muted">${esc(portfolio.brief.updated)}</div><pre>${esc(portfolio.brief.content)}</pre>` : `<div class="empty">No portfolio brief yet.</div>`}</article>
    <article class="card wide"><h2>Portfolio Review</h2>${portfolio.review.exists ? `<div class="muted">${esc(portfolio.review.updated)}</div><pre>${esc(portfolio.review.content)}</pre>` : `<div class="empty">No portfolio review yet.</div>`}</article>
    <article class="card wide"><h2>Portfolio Roadmap</h2>${portfolio.roadmap.exists ? `<div class="muted">${esc(portfolio.roadmap.updated)}</div><pre>${esc(portfolio.roadmap.content)}</pre>` : `<div class="empty">No portfolio roadmap yet.</div>`}</article>
    <article class="card wide"><h2>Business Portfolio</h2>${portfolio.portfolio.exists ? `<div class="muted">${esc(portfolio.portfolio.updated)}</div><pre>${esc(portfolio.portfolio.content)}</pre>` : `<div class="empty">No business portfolio yet.</div>`}</article>
    <article class="card wide"><h2>Portfolio Decisions</h2>${portfolio.decisions.exists ? `<div class="muted">${esc(portfolio.decisions.updated)}</div><pre>${esc(portfolio.decisions.content)}</pre>` : `<div class="empty">No portfolio decisions yet.</div>`}</article>
  `;
}
function renderNotifications() {
  const n = data.notifications;
  const commands = [
    data.commands.notification_status,
    data.commands.notification_detect,
    data.commands.notification_review,
    data.commands.notification_brief,
    data.commands.notification_list,
    data.commands.notification_read,
    data.commands.notification_dismiss,
    data.commands.notification_escalate
  ];
  const sectors = Object.entries(n.sector_counts || {}).map(([name,count]) => `<span class="pill">${esc(name)} ${esc(count)}</span>`).join("");
  return `
    <article class="card full">
      <h2>Notification Center</h2>
      <span class="pill">Enabled ${n.enabled}</span>
      <span class="pill">Auto detect ${n.auto_detect}</span>
      <span class="pill">Escalation confirmation ${n.requires_confirmation}</span>
      <span class="pill">Active ${n.records.length}</span>
      <span class="pill">New Critical/High ${n.critical_high_count}</span>
      <div class="mt-3">${sectors}</div>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('show notifications')">chat: list</button>
        <button class="copy" onclick="sendQuickChat('detect notifications')">chat: detect</button>
        <button class="copy" onclick="sendQuickChat('notification brief')">chat: brief</button>
      </div>
      <p class="muted mt-3">Notify only. No automatic execution, spending, emails, uploads, publishing, source edits, or external actions.</p>
    </article>
    <article class="card full">
      <h2>Notification Inbox</h2>
      ${table(n.records, [
        ["ID", "id"],
        ["Severity", "severity", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Type", "type"],
        ["Status", "status", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Title", "title"],
        ["Source", "source"],
        ["Action", "action"],
        ["Created", "created"]
      ])}
    </article>
    <article class="card wide"><h2>Notification Brief</h2>${n.brief.exists ? `<div class="muted">${esc(n.brief.updated)}</div><pre>${esc(n.brief.content)}</pre>` : `<div class="empty">No notification brief yet.</div>`}</article>
    <article class="card wide"><h2>Notification Review</h2>${n.review.exists ? `<div class="muted">${esc(n.review.updated)}</div><pre>${esc(n.review.content)}</pre>` : `<div class="empty">No notification review yet.</div>`}</article>
    <article class="card wide"><h2>Notification Rules</h2>${n.rules.exists ? `<div class="muted">${esc(n.rules.updated)}</div><pre>${esc(n.rules.content)}</pre>` : `<div class="empty">No notification rules yet.</div>`}</article>
    <article class="card wide"><h2>Notification History</h2>${n.history.exists ? `<div class="muted">${esc(n.history.updated)}</div><pre>${esc(n.history.content)}</pre>` : `<div class="empty">No notification history yet.</div>`}</article>
  `;
}
function renderExecutiveBriefs() {
  const b = data.briefs;
  const commands = [
    data.commands.brief_status,
    data.commands.morning_brief,
    data.commands.evening_review,
    data.commands.weekly_brief,
    data.commands.monthly_review,
    data.commands.executive_brief,
    data.commands.brief_history,
    data.commands.brief_preferences
  ];
  return `
    <article class="card">
      <h2>Executive Brief Engine</h2>
      <div class="stat">${b.enabled ? "Enabled" : "Disabled"}</div>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('give me a morning brief')">chat: morning</button>
        <button class="copy" onclick="sendQuickChat('executive brief')">chat: executive</button>
        <button class="copy" onclick="sendQuickChat('weekly brief')">chat: weekly</button>
        <button class="copy" onclick="sendQuickChat('monthly review')">chat: monthly</button>
        <button class="copy" onclick="sendQuickChat('evening review')">chat: evening</button>
      </div>
    </article>
    <article class="card">
      <h2>Copy CLI Commands</h2>
      ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
    </article>
    <article class="card full"><h2>Latest Brief</h2>${b.latest.exists ? `<div class="muted">${esc(b.latest.updated)}</div><pre>${esc(b.latest.content)}</pre>` : `<div class="empty">No latest brief yet.</div>`}</article>
    <article class="card wide"><h2>Morning Brief</h2>${b.morning.exists ? `<div class="muted">${esc(b.morning.updated)}</div><pre>${esc(b.morning.content)}</pre>` : `<div class="empty">No morning brief yet.</div>`}</article>
    <article class="card wide"><h2>Evening Review</h2>${b.evening.exists ? `<div class="muted">${esc(b.evening.updated)}</div><pre>${esc(b.evening.content)}</pre>` : `<div class="empty">No evening review yet.</div>`}</article>
    <article class="card wide"><h2>Weekly Executive Brief</h2>${b.weekly.exists ? `<div class="muted">${esc(b.weekly.updated)}</div><pre>${esc(b.weekly.content)}</pre>` : `<div class="empty">No weekly brief yet.</div>`}</article>
    <article class="card wide"><h2>Monthly Business Review</h2>${b.monthly.exists ? `<div class="muted">${esc(b.monthly.updated)}</div><pre>${esc(b.monthly.content)}</pre>` : `<div class="empty">No monthly review yet.</div>`}</article>
    <article class="card wide"><h2>Brief Preferences</h2>${b.preferences.exists ? `<div class="muted">${esc(b.preferences.updated)}</div><pre>${esc(b.preferences.content)}</pre>` : `<div class="empty">No brief preferences yet.</div>`}</article>
    <article class="card wide"><h2>Brief History</h2>${b.history.exists ? `<div class="muted">${esc(b.history.updated)}</div><pre>${esc(b.history.content)}</pre>` : `<div class="empty">No brief history yet.</div>`}</article>
  `;
}
function renderDailyOperatingLoop() {
  const d = data.daily_operating;
  const commands = [
    data.commands.daily_start,
    data.commands.daily_focus,
    data.commands.daily_plan,
    data.commands.daily_checkin,
    data.commands.daily_end,
    data.commands.daily_review
  ];
  const blocks = d.plan_blocks || {};
  const end = d.end_sections || {};
  return `
    <article class="card">
      <h2>Today's Focus</h2>
      <div class="muted">${esc(d.date)}</div>
      <pre>${esc(d.focus)}</pre>
      <button class="copy" onclick="sendQuickChat('Raphael what should I focus on')">Refresh focus</button>
    </article>
    <article class="card">
      <h2>Daily Actions</h2>
      <button class="copy" onclick="sendQuickChat('Raphael start my day')">Start my day</button>
      <button class="copy" onclick="sendQuickChat('Raphael plan my day')">Plan my day</button>
      <button class="copy" onclick="sendQuickChat('Raphael check in')">Check in</button>
      <button class="copy" onclick="sendQuickChat('Raphael end my day')">End my day</button>
    </article>
    <article class="card full">
      <h2>Top Tasks</h2>
      <pre>${esc(d.tasks)}</pre>
    </article>
    <article class="card full">
      <h2>Warnings</h2>
      <pre>${esc(d.warnings)}</pre>
    </article>
    <article class="card wide">
      <h2>Today's Plan</h2>
      <h3>Focus Block 1</h3><pre>${esc(blocks.focus_1 || "Run daily-plan.")}</pre>
      <h3>Focus Block 2</h3><pre>${esc(blocks.focus_2 || "Run daily-plan.")}</pre>
      <h3>Admin Block</h3><pre>${esc(blocks.admin || "Run daily-plan.")}</pre>
      <h3>Optional Creative / Business</h3><pre>${esc(blocks.optional || "Run daily-plan.")}</pre>
    </article>
    <article class="card wide">
      <h2>Check-ins</h2>
      ${d.checkins.exists ? `<div class="muted">${esc(d.checkins.updated)}</div><pre>${esc(d.checkins.content)}</pre>` : `<div class="empty">No check-in recorded today.</div>`}
    </article>
    <article class="card full">
      <h2>End Review</h2>
      ${d.end_review.exists ? `
        <h3>What Got Done</h3><pre>${esc(end.done)}</pre>
        <h3>What Moved</h3><pre>${esc(end.moved)}</pre>
        <h3>Blockers</h3><pre>${esc(end.blockers)}</pre>
        <h3>Tomorrow</h3><pre>${esc(end.tomorrow)}</pre>
      ` : `<div class="empty">No end-of-day review generated yet.</div>`}
    </article>
    <article class="card full">
      <h2>CLI Commands</h2>
      ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
      <div class="muted mt-3">${esc(d.safety)}</div>
    </article>
  `;
}
function renderActivityStream() {
  const a = data.activity;
  const commands = [
    data.commands.activity_status,
    data.commands.activity_feed,
    data.commands.activity_review,
    data.commands.activity_brief,
    data.commands.activity_timeline,
    data.commands.activity_stats,
    data.commands.activity_log,
    data.commands.activity_read
  ];
  return `
    <article class="card">
      <h2>Activity Stream</h2>
      <div class="stat">${a.summary.today}</div>
      <div class="muted">events today</div>
      <span class="pill">Week ${a.summary.week}</span>
      <span class="pill">High ${a.summary.high_events}</span>
      <span class="pill">Critical ${a.summary.critical_events}</span>
    </article>
    <article class="card">
      <h2>Matrix Prep</h2>
      <div class="muted">Most active council</div>
      <div class="stat" style="font-size:20px">${esc(a.summary.most_active_council)}</div>
      <div class="muted mt-3">Most active business</div>
      <div class="stat" style="font-size:20px">${esc(a.summary.most_active_business)}</div>
    </article>
    <article class="card">
      <h2>Copy CLI Commands</h2>
      ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('show activity')">chat: show activity</button>
        <button class="copy" onclick="sendQuickChat('activity brief')">chat: brief</button>
        <button class="copy" onclick="sendQuickChat('what happened recently')">chat: recent</button>
      </div>
    </article>
    <article class="card full"><h2>Live Feed</h2>${table(a.recent, [["Event ID","Event ID"],["Time","Timestamp"],["Type","Event Type"],["Severity","Severity"],["Title","Title"],["Source","Source System"]])}</article>
    <article class="card wide"><h2>Activity Brief</h2>${a.brief.exists ? `<div class="muted">${esc(a.brief.updated)}</div><pre>${esc(a.brief.content)}</pre>` : `<div class="empty">No activity brief yet.</div>`}</article>
    <article class="card wide"><h2>Activity Review</h2>${a.review.exists ? `<div class="muted">${esc(a.review.updated)}</div><pre>${esc(a.review.content)}</pre>` : `<div class="empty">No activity review yet.</div>`}</article>
    <article class="card wide"><h2>Activity Timeline</h2>${a.timeline.exists ? `<div class="muted">${esc(a.timeline.updated)}</div><pre>${esc(a.timeline.content)}</pre>` : `<div class="empty">No activity timeline yet.</div>`}</article>
    <article class="card wide"><h2>Activity Statistics</h2>${a.stats.exists ? `<div class="muted">${esc(a.stats.updated)}</div><pre>${esc(a.stats.content)}</pre>` : `<div class="empty">No activity statistics yet.</div>`}</article>
  `;
}
function renderInitiatives() {
  const initiatives = data.initiatives;
  const commands = [
    data.commands.initiative_status,
    data.commands.initiative_detect,
    data.commands.initiative_review,
    data.commands.initiative_brief,
    data.commands.initiative_score,
    data.commands.initiative_delegate,
    data.commands.initiative_history
  ];
  return `
    <article class="card full">
      <h2>Executive Initiative Engine</h2>
      <span class="pill">Enabled ${initiatives.enabled}</span>
      <span class="pill">Delegation confirmation ${initiatives.requires_confirmation}</span>
      <span class="pill">Auto execute ${initiatives.auto_execute}</span>
      <span class="pill">Threshold ${initiatives.threshold}</span>
      <span class="pill">Initiatives ${initiatives.records.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('detect initiatives')">chat: detect</button>
        <button class="copy" onclick="sendQuickChat('review initiatives')">chat: review</button>
        <button class="copy" onclick="sendQuickChat('brief initiatives')">chat: brief</button>
        <button class="copy" onclick="sendQuickChat('what initiatives should I focus on')">chat: focus</button>
      </div>
      <p class="muted mt-3">Recommendations only. No execution, spending, platform access, emails, publishing, uploads, source edits, arbitrary shell commands, or autonomous delegation.</p>
    </article>
    <article class="card full">
      <h2>Top Recommended Initiatives</h2>
      ${table(initiatives.top, [
        ["ID", "id"],
        ["Title", "title"],
        ["Type", "type"],
        ["Score", "score", v=>v ? `<div>${esc(v)}/100</div><div class="bar"><i style="width:${esc(v)}%"></i></div>` : "n/a"],
        ["Priority", "priority", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Council", "council"],
        ["Action", "action"]
      ])}
    </article>
    <article class="card full">
      <h2>Initiative Inbox</h2>
      ${table(initiatives.records, [
        ["ID", "id"],
        ["Title", "title"],
        ["Status", "status", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Priority", "priority"],
        ["Council", "council"],
        ["Evidence", "evidence"],
        ["Created", "created"]
      ])}
    </article>
    <article class="card wide"><h2>Initiative Brief</h2>${initiatives.brief.exists ? `<div class="muted">${esc(initiatives.brief.updated)}</div><pre>${esc(initiatives.brief.content)}</pre>` : `<div class="empty">No initiative brief yet.</div>`}</article>
    <article class="card wide"><h2>Initiative Review</h2>${initiatives.review.exists ? `<div class="muted">${esc(initiatives.review.updated)}</div><pre>${esc(initiatives.review.content)}</pre>` : `<div class="empty">No initiative review yet.</div>`}</article>
    <article class="card wide"><h2>Initiative Scores</h2>${initiatives.scores.exists ? `<div class="muted">${esc(initiatives.scores.updated)}</div><pre>${esc(initiatives.scores.content)}</pre>` : `<div class="empty">No initiative scores yet.</div>`}</article>
    <article class="card full"><h2>Initiative History</h2>${initiatives.history.exists ? `<div class="muted">${esc(initiatives.history.updated)}</div><pre>${esc(initiatives.history.content)}</pre>` : `<div class="empty">No initiative history yet.</div>`}</article>
  `;
}
function renderEmployees() {
  const employees = data.employees;
  if (window.RaphaelEmployeeNetwork) {
    return window.RaphaelEmployeeNetwork.renderPage(data.employee_network, employees);
  }
  const commands = [
    data.commands.employee_status,
    data.commands.employee_registry,
    data.commands.employee_org_chart,
    data.commands.employee_workload,
    data.commands.employee_brief,
    data.commands.employee_review,
    data.commands.employee_task_brief,
    data.commands.employee_assign_kpi,
    data.commands.employee_reassign
  ];
  return `
    <article class="card full">
      <h2>Digital Employee System</h2>
      <span class="pill">Enabled ${employees.enabled}</span>
      <span class="pill">Reviews ${employees.reviews_enabled}</span>
      <span class="pill">Reassignment confirmation ${employees.requires_reassignment_confirmation}</span>
      <span class="pill">Employees ${employees.records.length}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('show employee registry')">chat: registry</button>
        <button class="copy" onclick="sendQuickChat('show org chart')">chat: org chart</button>
        <button class="copy" onclick="sendQuickChat('show employee workload')">chat: workload</button>
        <button class="copy" onclick="sendQuickChat('brief Product Researcher Agent')">chat: brief employee</button>
        <button class="copy" onclick="sendQuickChat('review employee Store Manager Agent')">chat: review employee</button>
      </div>
      <p class="muted mt-3">Organization and evaluation only. No task execution, business execution, platform access, external action, source edits, spending, uploads, messages, or publishing.</p>
    </article>
    <article class="card full">
      <h2>Employee Registry</h2>
      ${table(employees.records, [
        ["ID", "id"],
        ["Employee", "name"],
        ["Role", "role"],
        ["Department", "department"],
        ["Manager", "manager"],
        ["Workload", "workload", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Performance", "performance", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Reviewed", "reviewed"]
      ])}
    </article>
    <article class="card wide"><h2>Org Chart</h2>${employees.org_chart.exists ? `<div class="muted">${esc(employees.org_chart.updated)}</div><pre>${esc(employees.org_chart.content)}</pre>` : `<div class="empty">No org chart yet.</div>`}</article>
    <article class="card wide"><h2>Workload Review</h2>${employees.workload.exists ? `<div class="muted">${esc(employees.workload.updated)}</div><pre>${esc(employees.workload.content)}</pre>` : `<div class="empty">No workload review yet.</div>`}</article>
    <article class="card wide"><h2>Employee KPI Map</h2>${employees.kpi_map.exists ? `<div class="muted">${esc(employees.kpi_map.updated)}</div><pre>${esc(employees.kpi_map.content)}</pre>` : `<div class="empty">No KPI map yet.</div>`}</article>
    <article class="card wide"><h2>Performance Reviews</h2>${employees.performance.exists ? `<div class="muted">${esc(employees.performance.updated)}</div><pre>${esc(employees.performance.content)}</pre>` : `<div class="empty">No performance reviews yet.</div>`}</article>
    <article class="card wide"><h2>Employee Brief</h2>${employees.brief.exists ? `<div class="muted">${esc(employees.brief.updated)}</div><pre>${esc(employees.brief.content)}</pre>` : `<div class="empty">No employee brief yet.</div>`}</article>
  `;
}
function renderExecution() {
  const exec = data.controlled_execution;
  const commands = [
    data.commands.execution_status,
    data.commands.execution_policy,
    data.commands.execution_request,
    data.commands.execution_dry_run,
    data.commands.execution_approve,
    data.commands.execution_run,
    data.commands.execution_review,
    data.commands.execution_log,
    data.commands.execution_safety_report
  ];
  return `
    <article class="card full">
      <h2>Controlled Execution Framework</h2>
      <span class="pill">Enabled ${exec.enabled}</span>
      <span class="pill">Confirmation ${exec.requires_confirmation}</span>
      <span class="pill">Dashboard ${exec.dashboard_enabled}</span>
      <span class="pill">Voice ${exec.voice_enabled}</span>
      <span class="pill">Max level ${exec.max_level}</span>
      <span class="pill">External ${exec.external_enabled}</span>
      <span class="pill">Dry run default ${exec.dry_run_default}</span>
      <div class="mt-3">
        ${commands.map(cmd => `<button class="copy" onclick="copyCommand('${esc(cmd)}')">${esc(cmd)}</button>`).join("")}
        <button class="copy" onclick="sendQuickChat('run initiative detection')">chat: run initiative detection</button>
        <button class="copy" onclick="sendQuickChat('run KPI dashboard refresh')">chat: refresh KPI dashboard</button>
        <button class="copy" onclick="sendQuickChat('show execution policy')">chat: policy</button>
        <button class="copy" onclick="sendQuickChat('show execution log')">chat: log</button>
      </div>
      <p class="muted mt-3">Operational but not unrestricted. Execution requests require approval and can only run allowlisted internal Raphael functions. External actions remain blocked.</p>
    </article>
    <article class="card full">
      <h2>Execution Requests</h2>
      ${table(exec.records, [
        ["ID", "id"],
        ["Action", "description"],
        ["Level", "level"],
        ["Type", "type"],
        ["System", "system"],
        ["Risk", "risk", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Status", "status", v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],
        ["Created", "created"]
      ])}
    </article>
    <article class="card wide"><h2>Execution Policy</h2>${exec.policy.exists ? `<div class="muted">${esc(exec.policy.updated)}</div><pre>${esc(exec.policy.content)}</pre>` : `<div class="empty">No execution policy yet.</div>`}</article>
    <article class="card wide"><h2>Execution Allowlist</h2>${exec.allowlist.exists ? `<div class="muted">${esc(exec.allowlist.updated)}</div><pre>${esc(exec.allowlist.content)}</pre>` : `<div class="empty">No execution allowlist yet.</div>`}</article>
    <article class="card wide"><h2>Execution Review</h2>${exec.review.exists ? `<div class="muted">${esc(exec.review.updated)}</div><pre>${esc(exec.review.content)}</pre>` : `<div class="empty">No execution review yet.</div>`}</article>
    <article class="card full"><h2>Execution Log</h2>${exec.log.exists ? `<div class="muted">${esc(exec.log.updated)}</div><pre>${esc(exec.log.content)}</pre>` : `<div class="empty">No execution log yet.</div>`}</article>
    <article class="card wide"><h2>Safety Report</h2>${exec.safety.exists ? `<div class="muted">${esc(exec.safety.updated)}</div><pre>${esc(exec.safety.content)}</pre>` : `<div class="empty">No safety report yet.</div>`}</article>
  `;
}
function renderGoals() {
  return `
    ${card("Goals", table(data.goals, [["ID","id"],["Title","title"],["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],["Priority","priority"],["Next Milestone","milestone"]]), "card full")}
    <article class="card full">
      <h2>Propagate Goal</h2>
      <p class="muted">Generate an advisory cascade plan. This does not create tasks, KPIs, initiatives, delegations, or execution.</p>
      <button class="copy" onclick="copyCommand('${esc(data.commands.propagate_goal)}')">${esc(data.commands.propagate_goal)}</button>
      <button class="copy" onclick="window.active='goalpropagation'; render()">open Goal Propagation</button>
    </article>`;
}
function renderGoalPropagation() {
  const gp = data.goal_propagation;
  const cascades = gp.plans.map(plan => `
    <article class="card full">
      <h2>${esc(plan.goal_id)} · ${esc(plan.title)}</h2>
      <div class="muted">${esc(plan.updated)}</div>
      <div class="mt-3"><span class="pill">${esc(plan.goal_id)}</span><span> → </span>${plan.councils.map(c => `<span class="pill">${esc(c)}</span>`).join("")}</div>
      <div class="mt-2">${plan.employees.slice(0,12).map(e => `<span class="pill">${esc(e.council)} → ${esc(e.employee)}</span>`).join("") || `<span class="muted">No employee responsibilities parsed.</span>`}</div>
    </article>`).join("") || `<article class="card full"><div class="empty">No cascade plans generated yet.</div></article>`;
  const notes = [gp.registry, gp.cascade_index, gp.council_objectives, gp.department_objectives, gp.employee_objectives, gp.kpi_map, gp.initiative_map, gp.review_cycles, gp.review, gp.brief];
  return `
    <article class="card full">
      <h2>Goal Propagation Commands</h2>
      ${["goal_propagation_status","propagate_goal","goal_cascade","goal_objectives","goal_kpi_map","goal_initiative_map","goal_review_cycle","goal_propagation_review","goal_propagation_brief"].map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}
      <p class="muted mt-3">Planning and recommendations only. Confirmation remains required for task, KPI, and initiative creation.</p>
    </article>
    ${cascades}
    ${notes.map(note => `<article class="card wide"><h2>${esc(note.label)}</h2>${note.exists ? `<div class="muted">${esc(note.updated)}</div><pre>${esc(note.content)}</pre>` : `<div class="empty">Not generated yet.</div>`}</article>`).join("")}`;
}
function renderDeliberations() {
  const d = data.deliberations;
  const rows = d.records.map(item => `
    <article class="card full">
      <h2>${esc(item.id)} · ${esc(item.question)}</h2>
      <div><span class="pill">${esc(item.status)}</span><span class="pill">Confidence ${esc(item.confidence)}</span></div>
      <div class="mt-2">${item.councils.map(council => `<span class="pill">${esc(council)}</span>`).join("")}</div>
      <h2 class="mt-3">Final Recommendation</h2>
      <p>${esc(item.recommendation)}</p>
      <h2 class="mt-3">Aaron Decisions Needed</h2>
      <pre>${esc(item.decisions)}</pre>
    </article>`).join("") || `<article class="card full"><div class="empty">No deliberations recorded.</div></article>`;
  return `
    <article class="card full">
      <h2>Deliberation Commands</h2>
      ${["deliberate","deliberation_status","deliberation_review","deliberation_brief","deliberation_history","deliberation_show"].map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}
      <p class="muted mt-3">Deliberations recommend only. They do not execute, delegate, message, spend, publish, or bypass approval systems.</p>
    </article>
    ${rows}
    ${[d.overview,d.history,d.review,d.brief].map(note => `<article class="card wide"><h2>${esc(note.label)}</h2>${note.exists ? `<div class="muted">${esc(note.updated)}</div><pre>${esc(note.content)}</pre>` : `<div class="empty">Not generated yet.</div>`}</article>`).join("")}`;
}
function renderExecutionPlans() {
  const p = data.execution_plans;
  const rows = p.records.map(item => `
    <article class="card full">
      <h2>${esc(item.id)} · ${esc(item.topic)}</h2>
      <div><span class="pill">${esc(item.status)}</span>${item.councils.map(council => `<span class="pill">${esc(council)}</span>`).join("")}</div>
      <h2 class="mt-3">Objective</h2><p>${esc(item.objective)}</p>
      <h2 class="mt-3">Recommended Strategy</h2><p>${esc(item.strategy)}</p>
      <h2 class="mt-3">Source Records</h2><pre>${esc(item.sources)}</pre>
      <h2 class="mt-3">Aaron Decisions Needed</h2><pre>${esc(item.decisions)}</pre>
    </article>`).join("") || `<article class="card full"><div class="empty">No execution plans recorded.</div></article>`;
  return `
    <article class="card full">
      <h2>Execution Planning Commands</h2>
      ${["execution_plan","execution_plan_from_deliberation","execution_plan_review","execution_plan_brief","execution_plan_history","execution_plan_show"].map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}
      <p class="muted mt-3">Planning only. Task creation, execution, delegation, outreach, publishing, spending, and external actions remain separately confirmation-gated or blocked.</p>
    </article>
    ${rows}
    ${[p.overview,p.history,p.review,p.brief].map(note => `<article class="card wide"><h2>${esc(note.label)}</h2>${note.exists ? `<div class="muted">${esc(note.updated)}</div><pre>${esc(note.content)}</pre>` : `<div class="empty">Not generated yet.</div>`}</article>`).join("")}`;
}
function renderTasks() {
  const rows = taskFocusId ? data.tasks.filter(task => task.id === taskFocusId) : data.tasks;
  const focus = taskFocusId
    ? `<div class="mb-3"><span class="pill">Focused task ${esc(taskFocusId)}</span><button class="copy" onclick="taskFocusId=''; render();">Show all tasks</button></div>`
    : "";
  return card("Tasks", focus + table(rows, [["ID","id"],["Task","task"],["Agent","agent"],["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],["Priority","priority"],["Project","project"]]), "card full");
}
function openRelatedTask(taskId) {
  taskFocusId = taskId || "";
  active = "tasks";
  render();
}
function renderAgents() {
  return card("Agents", table(data.agents, [["Agent","name"],["Open Tasks","open_tasks"],["Total Tasks","total_tasks"],["Brief","has_brief",v=>v?"yes":"no"],["AI Brief","has_ai_brief",v=>v?"yes":"no"]]), "card full");
}
function renderCouncils() {
  const rows = data.councils.map(c => `
    <article class="card wide">
      <h2>${esc(c.name)}</h2>
      <p class="muted">${esc(c.purpose)}</p>
      <div class="mt-2">${c.members.map(m => `<span class="pill">${esc(m)}</span>`).join("")}</div>
      <div class="mt-3"><span class="pill">Tasks ${c.tasks.length}</span><span class="pill">Brief ${c.has_brief ? "yes" : "no"}</span><span class="pill">Review ${c.has_review ? "yes" : "no"}</span></div>
      <div class="mt-3">
        <button class="copy" onclick="window.RaphaelMatrix.openCouncilChamber('${esc(c.name)}')">open chamber</button>
        <button class="copy" onclick="copyCommand('python raphael.py council-brief &quot;${esc(c.name)}&quot;')">copy brief command</button>
        <button class="copy" onclick="copyCommand('python raphael.py council-review &quot;${esc(c.name)}&quot;')">copy review command</button>
      </div>
    </article>`).join("");
  return `
    <article class="card full">
      <h2>Council Commands</h2>
      <button class="copy" onclick="copyCommand('${esc(data.commands.list_councils)}')">${esc(data.commands.list_councils)}</button>
      <button class="copy" onclick="copyCommand('${esc(data.commands.council_status)}')">${esc(data.commands.council_status)}</button>
      <button class="copy" onclick="copyCommand('${esc(data.commands.council_debate)}')">${esc(data.commands.council_debate)}</button>
    </article>
    ${rows}
    <article class="card full"><h2>Council Tasks</h2>${table(data.council_tasks, [["ID","id"],["Council","council"],["Task","task"],["Agent","agent"],["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`]])}</article>
    <article class="card full"><h2>Recent Debates</h2>${table(data.council_debates, [["Council","council"],["Debate","name"],["Updated","updated"]])}</article>
  `;
}
function renderWorkflows() {
  return card("Workflow Requests", table(data.workflows, [["ID","id"],["Workflow","workflow_name"],["Project","project"],["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],["Risk","risk_level"]]), "card full");
}
function renderN8nStudio() {
  const studio = data.n8n_workflow_studio;
  const commands = ["n8n_status","n8n_workflow_plan","n8n_workflow_generate","n8n_workflow_review","n8n_workflow_brief","n8n_workflow_show","n8n_workflow_export","n8n_workflow_catalog","n8n_workflow_graph","n8n_workflow_import_archive","workflow_archive_show","workflow_archive_search","workflow_archive_summary"];
  const registry = studio.records.slice(0, 250);
  const archive = studio.archive_records.slice(0, 250);
  const archiveDetails = (studio.archive_details || []).slice(0, 25);
  const categories = Object.entries(studio.categories).sort((a,b)=>b[1]-a[1]);
  const graph = categories.map(([category,count], index) => `
    <div class="card">
      <h2>${esc(category)}</h2>
      <div class="stat">${esc(count)}</div>
      <div class="muted">workflow relationships</div>
    </div>`).join("");
  return `
    <article class="card full">
      <h2>n8n Workflow Studio</h2>
      <p>Workflow architecture, inactive JSON drafting, archive analysis, sanitized export, and approved localhost execution through Workflow Runner.</p>
      ${commands.map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}
      <p class="muted mt-3">Execution is limited to registered, approved, credential-free local workflows. Activation, external calls, and source edits remain blocked.</p>
    </article>
    <article class="card full"><h2>Workflow Registry (${studio.records.length})</h2>${table(registry, [["ID","id"],["Name","name"],["Category","category"],["Origin","origin"],["Nodes","nodes"],["Status","status"]])}</article>
    <article class="card full"><h2>Workflow Templates</h2><pre>${esc(studio.templates.content)}</pre></article>
    <article class="card full"><h2>Workflow Knowledge</h2><pre>${esc(studio.knowledge.content)}</pre></article>
    <article class="card full"><h2>Workflow Reviews</h2><pre>${esc(studio.reviews.content)}</pre></article>
    <article class="card full"><h2>Workflow Graph</h2><div class="grid">${graph}</div></article>
    <article class="card full"><h2>Workflow Archive Explorer (${studio.archive_records.length})</h2>${table(archive, [["ID","id"],["Workflow","name"],["Category","category"],["Nodes","nodes"],["Source File","source_workflow"],["Services","services",v=>esc((v||[]).join(", "))]])}</article>
    <article class="card full">
      <h2>Archive Details</h2>
      ${archiveDetails.length ? archiveDetails.map(row=>`
        <section class="maintenance-error">
          <strong>${esc(row.workflow_id)} · ${esc(row.workflow_name)}</strong>
          <span class="pill">Category ${esc(row.category)}</span>
          <span class="pill">Nodes ${esc(row.node_count)}</span>
          <span class="pill ${statusClass(row.risk_level)}">Risk ${esc(row.risk_level)}</span>
          <p>${esc(row.description)}</p>
          <div class="muted">Node Types: ${esc((row.node_types || []).join(", "))}</div>
          <div class="muted">Triggers: ${esc((row.triggers || []).join(", ") || "None detected")}</div>
          <div class="muted">External Services: ${esc((row.external_services || []).join(", ") || "None detected")}</div>
          <div class="muted">Credentials Required: ${esc((row.credentials_required || []).join(", ") || "None declared")}</div>
          <div class="muted">Reusable Patterns: ${esc((row.reusable_patterns || []).join("; "))}</div>
          <div class="muted">Potential Raphael Uses: ${esc((row.potential_raphael_uses || []).join("; "))}</div>
          <button class="copy" onclick="copyCommand('python raphael.py workflow-archive-show &quot;${esc(row.workflow_id)}&quot;')">Copy show command</button>
          <button class="copy" onclick="copyCommand('python raphael.py workflow-archive-summary &quot;${esc(row.workflow_id)}&quot;')">Copy summary command</button>
        </section>`).join("") : `<div class="empty">No archive details found. Run n8n-workflow-import-archive first.</div>`}
    </article>
    <article class="card wide"><h2>Workflow Brief</h2><pre>${esc(studio.brief.content)}</pre></article>
    <article class="card wide"><h2>Export History</h2><pre>${esc(studio.history.content)}</pre></article>`;
}
async function refreshWorkflowRunner() {
  const response = await fetch("/api/workflow-runner");
  if (!response.ok) throw new Error(`Workflow Runner refresh failed (${response.status}).`);
  data.workflow_runner = await response.json();
  if (active === "workflowrunner") render();
}
async function workflowRunnerPost(endpoint, body) {
  const response = await fetch(endpoint, {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(body)
  });
  let payload = {};
  try { payload = await response.json(); }
  catch (_) { payload = {error:`Workflow API returned non-JSON response (${response.status}).`}; }
  return {response,payload};
}
async function workflowRunnerAction(action, identifier, confirmationKey="") {
  const endpoint = `/api/workflow-runner/${action}`;
  const key = action === "execute" ? "workflow_id" : "exec_id";
  workflowActionState = {kind:"working", message:`${action} requested for ${identifier}.`};
  render();
  try {
    let {response,payload} = await workflowRunnerPost(endpoint, {[key]:identifier, confirmation_key:confirmationKey});
    if (payload.confirmation_required) {
      workflowActionState = {kind:"pending", message:payload.message, command:payload.command};
      render();
      const approved = window.confirm(`${payload.message || "Confirmation required."}\n\n${payload.command || ""}`);
      if (!approved) {
        workflowActionState = {kind:"warn", message:"Workflow action cancelled before execution."};
        render();
        return;
      }
      ({response,payload} = await workflowRunnerPost(endpoint, {[key]:identifier, confirmation_key:payload.confirmation_key}));
    }
    if (!response.ok || !payload.ok) throw new Error(payload.error || payload.message || `Workflow action failed (${response.status}).`);
    if (payload.workflow_runner) data.workflow_runner = payload.workflow_runner;
    workflowActionState = {kind:"success", message:payload.message || `${action} completed.`};
    await refreshWorkflowRunner();
  } catch (error) {
    workflowActionState = {kind:"error", message:String(error?.message || error)};
    render();
  }
}
async function workflowRunnerRead(action, execId) {
  workflowActionState = {kind:"working", message:`Loading ${action} for ${execId}.`};
  render();
  try {
    const {response,payload} = await workflowRunnerPost(`/api/workflow-runner/${action}`, {exec_id:execId});
    if (!response.ok || !payload.ok) throw new Error(payload.error || `Workflow ${action} failed.`);
    if (payload.workflow_runner) data.workflow_runner = payload.workflow_runner;
    workflowActionState = {kind:"success", message:`${action} loaded for ${execId}.`, detail:JSON.stringify(payload.result,null,2)};
    render();
  } catch (error) {
    workflowActionState = {kind:"error", message:String(error?.message || error)};
    render();
  }
}
function renderWorkflowRunner() {
  const runner = data.workflow_runner || {};
  const workflows = runner.workflows || [];
  const executions = runner.executions || [];
  const action = workflowActionState ? `<article class="card full ${workflowActionState.kind === "error" ? "error-banner" : ""}">
    <h2>Workflow Action</h2><p>${esc(workflowActionState.message || "")}</p>
    ${workflowActionState.command ? `<code>${esc(workflowActionState.command)}</code>` : ""}
    ${workflowActionState.detail ? `<pre>${esc(workflowActionState.detail)}</pre>` : ""}
  </article>` : "";
  const workflowRows = workflows.map(row => ({...row, actions:`<button class="copy" onclick="workflowRunnerAction('execute','${esc(row.workflow_id)}')">Execute</button>`}));
  const executionRows = executions.map(row => ({...row, actions:
    `<button class="copy" onclick="workflowRunnerRead('monitor','${esc(row.exec_id)}')">Monitor</button>` +
    `<button class="copy" onclick="workflowRunnerRead('result','${esc(row.exec_id)}')">Review Result</button>` +
    (!["completed","failed","cancelled"].includes(row.status) ? `<button class="copy" onclick="workflowRunnerAction('cancel','${esc(row.exec_id)}')">Cancel</button>` : "")
  }));
  return `${action}
    <article class="card full">
      <h2>Workflow Runner</h2>
      <span class="pill">Available ${workflows.length}</span>
      <span class="pill">Active ${(runner.active||[]).length}</span>
      <span class="pill">Queued ${(runner.queued||[]).length}</span>
      <span class="pill">Completed ${(runner.completed||[]).length}</span>
      <span class="pill">Failed ${(runner.failed||[]).length}</span>
      <span class="pill">n8n ${runner.n8n?.healthy ? "Online" : "Offline"}</span>
      <p class="muted mt-3">Registered local workflows only. Execution and cancellation use Command Bus confirmation.</p>
      ${["workflow_runner_status","workflow_list","workflow_failures","workflow_runner_review"].map(key=>`<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}
    </article>
    <article class="card full"><h2>Available Workflows</h2>${table(workflowRows, [["ID","workflow_id"],["Name","name"],["Category","category"],["Mode","execution_mode"],["Risk","risk_level"],["Approval","approval_required"],["Enabled","enabled"],["Actions","actions",v=>v]])}</article>
    <article class="card full"><h2>Executions</h2>${table(executionRows, [["Execution","exec_id"],["Workflow","workflow_name"],["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],["Approval","approval_status"],["Stage","current_stage"],["Duration","duration_seconds"],["Task","task_id"],["Actions","actions",v=>v]])}</article>
    <article class="card wide"><h2>Execution Logs</h2>${executions.length ? `<pre>${esc(JSON.stringify(executions.slice(0,5).map(row=>({exec_id:row.exec_id,logs:row.logs?.slice(-8),errors:row.errors})),null,2))}</pre>` : `<div class="empty">No executions yet.</div>`}</article>
    <article class="card wide"><h2>Failures and Recovery</h2>${runner.failures_note?.exists ? `<pre>${esc(runner.failures_note.content)}</pre>` : `<div class="empty">No failure record.</div>`}</article>`;
}
function renderMemory() {
  return card("Memory Search", `<p class="muted">Read-only dashboard mode. Copy this command and run it in the terminal:</p><button class="copy" onclick="copyCommand('${esc(data.commands.memory_search)}')">${esc(data.commands.memory_search)}</button>`, "card full");
}
function renderVoice() {
  const h = data.health;
  return [
    card("Piper", `<div>Engine: <span class="pill">${esc(h.piper.engine)}</span></div><div>Executable: <span class="${statusClass(h.piper.exe_exists)}">${h.piper.exe_exists}</span></div><div>Voice model: <span class="${statusClass(h.piper.model_exists)}">${h.piper.model_exists}</span></div>`),
    card("Voice Commands", `<button class="copy" onclick="copyCommand('python C:\\\\RaphaelOS\\\\voice_gateway.py assistant-status')">assistant-status</button><button class="copy" onclick="copyCommand('python C:\\\\RaphaelOS\\\\voice_gateway.py wake-chat')">wake-chat</button>`, "card wide")
  ].join("");
}
function renderVision() {
  return card("Vision Requests", table(data.vision_requests, [["ID","id"],["File","file_name"],["Type","file_type"],["Question","question"],["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],["Created","created"]]), "card full");
}
function renderSearch() {
  const internet = data.internet_access || {};
  const commands = ["internet_status","searxng_status","searxng_start","internet_headless_search","internet_latest_overview","internet_latest_snippets","internet_raw_json","internet_analyze_results","internet_niche_score","pandas_status","pandas_analyze_csv","internet_review","internet_brief","internet_source_review"];
  const resultItems = (internet.results || []).flatMap(result => (result.items || []).map(item => ({request_id:result.request_id, ...item})));
  const overviewRows = (internet.results || []).map(result => {
    const overview = result.ai_overview || {};
    return {
      request_id: result.request_id,
      question: result.question,
      answer: overview.answer || result.summary || "",
      confidence: overview.confidence || "",
      sources: (overview.sources || []).map(source => source.title || source.url).join("; ")
    };
  });
  return `
    <article class="card full">
      <h2>Permissioned Internet Access</h2>
      <span class="pill">Enabled ${esc(internet.enabled)}</span>
      <span class="pill">Confirmation ${esc(internet.requires_confirmation)}</span>
      <span class="pill">Provider ${esc(internet.provider)}</span>
      <span class="pill ${internet.searxng?.healthy ? "ok" : "bad"}">SearXNG ${internet.searxng?.healthy ? "Online" : "Offline"}</span>
      <span class="pill">Headless ${esc(internet.headless_enabled)}</span>
      <span class="pill">AI Overview ${esc(internet.ai_overview_default)}</span>
      <span class="pill">Pandas ${esc(internet.pandas_enabled)}</span>
      <div class="mt-3">${commands.map(key=>`<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}</div>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('review internet requests')">Review Requests</button>
        <button class="copy" onclick="sendQuickChat('search the web for current Etsy trends')">Headless Search</button>
        <button class="copy" onclick="sendQuickChat('POD niche research for summer shirts')">POD Niche Research</button>
        <button class="copy" onclick="sendQuickChat('look up current software docs for FastAPI')">Software Docs</button>
      </div>
      <p class="muted">Searches require confirmation. No autonomous browsing, login, credentials, spending, posting, uploading, email, messaging, or platform action.</p>
    </article>
    ${renderInternetOverviewCard(internet.latest_overview, internet.latest_result)}
    <article class="card full"><h2>Pending Search Requests</h2>${table(internet.pending || [], [["ID","request_id"],["Question","question"],["Status","status",v=>`<span class="${statusClass(v)}">${esc(v)}</span>`],["Created","created"]])}</article>
    <article class="card full"><h2>Completed Searches</h2>${table(internet.completed || [], [["ID","request_id"],["Question","question"],["Status","status"],["Completed","completed"]])}</article>
    <article class="card full"><h2>AI Overview History</h2>${table(overviewRows, [["Request","request_id"],["Question","question"],["Answer","answer"],["Confidence","confidence"],["Sources","sources"]])}</article>
    <article class="card full"><h2>Headless Search Results</h2>${table(resultItems, [["Request","request_id"],["Rank","rank"],["Title","title"],["URL","url"],["Snippet","snippet"],["Reliability","reliability"],["Timestamp","timestamp"]])}</article>
    <article class="card full"><h2>Saved Sources</h2>${table(internet.sources || [], [["URL","url",v=>`<span class="muted">${esc(v)}</span>`],["Request","request_id"],["Reliability","reliability"],["Title","title"],["Notes","notes"],["Reviewed","reviewed"]])}</article>
    <article class="card full"><h2>Niche Scoring</h2>${table(internet.niche_scores || [], [["Request","request_id"],["Demand","demand_signal"],["Competition","competition_signal"],["Evergreen","evergreen_potential"],["Product Fit","product_fit"],["Source Quality","source_quality"],["Confidence","confidence"],["Overall","overall_niche_score"]])}</article>
    <article class="card wide"><h2>Source Reliability Notes</h2>${internet.source_review?.exists ? `<pre>${esc(internet.source_review.content)}</pre>` : `<div class="empty">No source reviews yet.</div>`}</article>
    <article class="card wide"><h2>Internet Safety Policy</h2>${internet.safety_policy?.exists ? `<pre>${esc(internet.safety_policy.content)}</pre>` : `<div class="empty">Run internet-status to initialize Internet Access.</div>`}</article>
    <article class="card wide"><h2>Internet Brief</h2>${internet.brief?.exists ? `<pre>${esc(internet.brief.content)}</pre>` : `<div class="empty">Run internet-brief.</div>`}</article>
    <article class="card wide"><h2>Legacy Search Requests</h2>${table(data.search_requests, [["ID","id"],["Question","question"],["Status","status"],["Created","created"]])}</article>
  `;
}
function renderHealth() {
  const h = data.health;
  return [
    card("Qdrant", `<div class="${statusClass(h.qdrant.ok)}">${h.qdrant.ok ? "Online" : "Unavailable"}</div><pre>${esc(h.qdrant.detail)}</pre>`),
    card("Ollama", `<div class="${statusClass(h.ollama.ok)}">${h.ollama.ok ? "Online" : "Unavailable"}</div><div>${h.ollama.models.map(m=>`<span class="pill">${esc(m)}</span>`).join("")}</div>`),
    card("Vision Model", `<div>${esc(h.vision.model)}</div><div class="${statusClass(h.vision.available)}">Available: ${h.vision.available}</div><div>Enabled: ${h.vision.enabled}</div>`),
    card("Paths", `<pre>${esc(JSON.stringify(h.paths, null, 2))}</pre>`, "card full")
  ].join("");
}
function renderKnowledge() {
  const k = data.knowledge;
  const commands = ["knowledge_status", "knowledge_scan", "knowledge_import", "knowledge_classify", "knowledge_curation_review", "knowledge_rename_suggestion", "knowledge_skills_map", "knowledge_portfolio_candidates", "knowledge_index", "knowledge_search"];
  return `
    <article class="card full">
      <h2>Knowledge Ingestion Engine</h2>
      <span class="pill">Summaries ${k.summaries.length}</span>
      <span class="pill">Inventories ${k.inventories.length}</span>
      <span class="pill">Source ${esc(k.safety.source_access)}</span>
      <span class="pill">Raw indexing ${esc(k.safety.raw_indexing)}</span>
      <div class="mt-3">${commands.map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}</div>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('scan knowledge folder K:\\\\School')">chat: scan</button>
        <button class="copy" onclick="sendQuickChat('import knowledge folder K:\\\\School')">chat: import</button>
        <button class="copy" onclick="sendQuickChat('summarize knowledge')">chat: summarize</button>
        <button class="copy" onclick="sendQuickChat('index knowledge')">chat: index</button>
        <button class="copy" onclick="sendQuickChat('search knowledge compiler project')">chat: search</button>
        <button class="copy" onclick="sendQuickChat('classify knowledge')">chat: classify</button>
        <button class="copy" onclick="sendQuickChat('show knowledge skills map')">chat: skills map</button>
        <button class="copy" onclick="sendQuickChat('show portfolio candidates')">chat: portfolio candidates</button>
      </div>
      <p class="muted mt-3">Originals remain on the source drive. Raphael writes Markdown inventories and summaries only, and Qdrant receives generated Markdown rather than raw files.</p>
    </article>
    <article class="card full"><h2>Generated Summaries</h2>${table(k.summaries, [["ID","id"],["Curated Name","suggested_title"],["Original Summary","title"],["Type","project_type"],["Course","course"],["Status","status"],["Portfolio","portfolio_score"],["Ignored","ignored",v=>v ? "yes" : "no"]])}</article>
    <article class="card wide"><h2>Inventories</h2>${table(k.inventories, [["Inventory","name"],["Updated","updated"],["Path","path"]])}</article>
    <article class="card wide"><h2>Curation Review</h2>${k.curation_review.exists ? `<pre>${esc(k.curation_review.content)}</pre>` : `<div class="empty">Run knowledge-curation-review.</div>`}</article>
    <article class="card wide"><h2>Rename Suggestions</h2>${k.rename_suggestions.exists ? `<pre>${esc(k.rename_suggestions.content)}</pre>` : `<div class="empty">Run knowledge-rename-suggestion.</div>`}</article>
    <article class="card wide"><h2>Skills Map</h2>${k.skills_map.exists ? `<pre>${esc(k.skills_map.content)}</pre>` : `<div class="empty">Run knowledge-skills-map.</div>`}</article>
    <article class="card wide"><h2>Portfolio Candidate Ranking</h2>${k.portfolio_candidates.exists ? `<pre>${esc(k.portfolio_candidates.content)}</pre>` : `<div class="empty">Run knowledge-portfolio-candidates.</div>`}</article>
    <article class="card wide"><h2>Ignored Items</h2>${k.ignored_items.exists ? `<pre>${esc(k.ignored_items.content)}</pre>` : `<div class="empty">No ignored items.</div>`}</article>
  `;
}
function exploreRelatedKnowledge() {
  const value = (document.getElementById("relationship-id")?.value || "").trim();
  if (value) sendQuickChat(`show related projects for ${value}`);
}
function exploreKnowledgePath() {
  const source = (document.getElementById("relationship-source")?.value || "").trim();
  const target = (document.getElementById("relationship-target")?.value || "").trim();
  if (source && target) {
    const input = document.getElementById("chat-input");
    active = "chat";
    render();
    if (input) input.value = `knowledge path ${source} ${target}`;
    sendQuickChat(`knowledge path ${source} ${target}`);
  }
}
function renderKnowledgeRelationships() {
  const r = data.knowledge_relationships;
  const commands = ["knowledge_relationships","knowledge_graph","knowledge_clusters","knowledge_career_map","knowledge_business_map","knowledge_portfolio_map","knowledge_tech_map","knowledge_skill_map"];
  return `
    <article class="card full">
      <h2>Knowledge Relationships</h2>
      <span class="pill">Items ${r.items}</span>
      <span class="pill">Nodes ${r.nodes}</span>
      <span class="pill">Relationships ${r.relationships}</span>
      <div class="mt-3">${commands.map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}</div>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('show knowledge graph')">chat: graph</button>
        <button class="copy" onclick="sendQuickChat('show career map')">chat: career</button>
        <button class="copy" onclick="sendQuickChat('show portfolio map')">chat: portfolio</button>
        <button class="copy" onclick="sendQuickChat('show technology map')">chat: technology</button>
      </div>
    </article>
    <article class="card full">
      <h2>Relationship Explorer</h2>
      <div class="chat-input-row"><input id="relationship-id" placeholder="KNOW-ID"><button class="primary" onclick="exploreRelatedKnowledge()">Show Related</button></div>
      <div class="chat-input-row mt-3"><input id="relationship-source" placeholder="KNOW-ID-A"><input id="relationship-target" placeholder="KNOW-ID-B"><button class="primary" onclick="exploreKnowledgePath()">Find Path</button></div>
    </article>
    <article class="card wide"><h2>Graph Overview</h2>${r.graph.exists ? `<pre>${esc(r.graph.content)}</pre>` : `<div class="empty">Run knowledge-graph.</div>`}</article>
    <article class="card wide"><h2>Clusters</h2>${r.clusters.exists ? `<pre>${esc(r.clusters.content)}</pre>` : `<div class="empty">Run knowledge-clusters.</div>`}</article>
    <article class="card wide"><h2>Career Map</h2>${r.career.exists ? `<pre>${esc(r.career.content)}</pre>` : `<div class="empty">Run knowledge-career-map.</div>`}</article>
    <article class="card wide"><h2>Business Map</h2>${r.business.exists ? `<pre>${esc(r.business.content)}</pre>` : `<div class="empty">Run knowledge-business-map.</div>`}</article>
    <article class="card wide"><h2>Portfolio Map</h2>${r.portfolio.exists ? `<pre>${esc(r.portfolio.content)}</pre>` : `<div class="empty">Run knowledge-portfolio-map.</div>`}</article>
    <article class="card wide"><h2>Technology Map</h2>${r.technology.exists ? `<pre>${esc(r.technology.content)}</pre>` : `<div class="empty">Run knowledge-tech-map.</div>`}</article>
    <article class="card wide"><h2>Skills Map</h2>${r.skills.exists ? `<pre>${esc(r.skills.content)}</pre>` : `<div class="empty">Run knowledge-skill-map.</div>`}</article>
    <article class="card wide"><h2>Relationship Review</h2>${r.review.exists ? `<pre>${esc(r.review.content)}</pre>` : `<div class="empty">Run knowledge-relationships.</div>`}</article>
  `;
}
function renderCommunications() {
  const c = data.communications;
  const commands = ["communication_status","communication_review","communication_history","communication_request","communication_respond","communication_recommend","communication_escalate","communication_synthesize","communication_network","communication_brief"];
  return `
    <article class="card full">
      <h2>Inter-Council Communications</h2>
      <span class="pill">Open ${c.open_requests.length}</span>
      <span class="pill">Responses ${c.responses.length}</span>
      <span class="pill">Recommendations ${c.recommendations.length}</span>
      <span class="pill">Syntheses ${c.syntheses.length}</span>
      <div class="mt-3">${commands.map(key => `<button class="copy" onclick="copyCommand('${esc(data.commands[key])}')">${esc(data.commands[key])}</button>`).join("")}</div>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('show council communications')">chat: communications</button>
        <button class="copy" onclick="sendQuickChat('request financial assessment')">chat: financial assessment</button>
        <button class="copy" onclick="sendQuickChat('request portfolio assessment')">chat: portfolio assessment</button>
        <button class="copy" onclick="sendQuickChat('synthesize recommendations')">chat: synthesize</button>
      </div>
      <p class="muted mt-3">Internal advisory records only. No execution, approvals, autonomous decisions, or external messages.</p>
    </article>
    <article class="card full"><h2>Open Requests</h2>${table(c.open_requests, [["ID","id"],["From","from_council"],["To","to_council"],["Type","request_type"],["Topic","topic"],["Question","question"]])}</article>
    <article class="card full"><h2>Recent Responses</h2>${table(c.responses.slice().reverse().slice(0,10), [["ID","id"],["Request","request_id"],["Council","from_council"],["Position","response_type"],["Topic","topic"],["Confidence","confidence_score"]])}</article>
    <article class="card full"><h2>Recommendations</h2>${table(c.recommendations.slice().reverse().slice(0,10), [["ID","id"],["Topic","topic"],["Recommendation","recommendation"],["Confidence","confidence_score"],["Status","status"]])}</article>
    <article class="card full"><h2>Executive Syntheses</h2>${table(c.syntheses.slice().reverse().slice(0,10), [["ID","id"],["Topic","topic"],["Executive Recommendation","executive_recommendation"],["Confidence","confidence_score"],["Status","status"]])}</article>
    <article class="card wide"><h2>Communication Graph</h2>${c.network.exists ? `<pre>${esc(c.network.content)}</pre>` : `<div class="empty">Run communication-network.</div>`}</article>
    <article class="card wide"><h2>Communication Review</h2>${c.review.exists ? `<pre>${esc(c.review.content)}</pre>` : `<div class="empty">Run communication-review.</div>`}</article>
    <article class="card wide"><h2>Communication Brief</h2>${c.brief.exists ? `<pre>${esc(c.brief.content)}</pre>` : `<div class="empty">Run communication-brief.</div>`}</article>
    <article class="card wide"><h2>Communication History</h2>${c.history.exists ? `<pre>${esc(c.history.content)}</pre>` : `<div class="empty">No communication history yet.</div>`}</article>
  `;
}
function maintenanceState(value) {
  return value ? `<span class="maintenance-state ok">Healthy</span>` : `<span class="maintenance-state bad">Needs attention</span>`;
}
function serviceEndpoint(action) {
  const endpoints = {
    start:"/api/services/start",
    stop:"/api/services/stop",
    restart:"/api/services/restart",
    health:"/api/services/health",
    start_stack:"/api/services/start-stack",
    open:"/api/services/open"
  };
  return endpoints[action] || "";
}
function setServiceActionState(state) {
  serviceActionState = state;
  if (active === "maintenance" && data) render();
}
function showDockerLogs(serviceId) {
  const rows = data?.maintenance?.service_manager?.services || [];
  const row = rows.find(item => item.service_id === serviceId);
  setServiceActionState({
    kind: row?.logs ? "success" : "warn",
    title: `Docker logs: ${serviceId}`,
    message: row?.logs ? "Showing the latest Raphael-managed container logs." : "No Raphael-managed Docker logs are available.",
    detail: row?.logs || row?.last_error || "The container may be external, stopped, or not Raphael-managed."
  });
}
async function refreshMaintenanceServices() {
  const [statusResponse, maintenanceResponse] = await Promise.all([
    fetch("/api/services/status"),
    fetch("/api/maintenance")
  ]);
  if (!statusResponse.ok || !maintenanceResponse.ok) {
    throw new Error(`Refresh failed: services ${statusResponse.status}, maintenance ${maintenanceResponse.status}`);
  }
  const serviceStatus = await statusResponse.json();
  const maintenance = await maintenanceResponse.json();
  maintenance.service_manager = serviceStatus;
  data.maintenance = maintenance;
  const groups = maintenance.bootstrap?.groups || {};
  const pill = document.getElementById("bootstrap-health-pill");
  if (pill) {
    pill.textContent = `Core: ${groups.core || "Unknown"} · AI: ${groups.ai || "Unknown"} · Creative: ${groups.creative || "Unknown"} · Voice: ${groups.voice || "Unknown"}`;
    pill.classList.toggle("bad", [groups.core, groups.ai, groups.creative].includes("Warning"));
  }
  if (active === "maintenance") render();
}
async function callServiceEndpoint(endpoint, serviceId, confirmationKey="") {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({service_id: serviceId, confirmation_key: confirmationKey})
  });
  let payload = {};
  try { payload = await response.json(); }
  catch (_) { payload = {error:`Service API returned non-JSON response (${response.status}).`}; }
  return {response, payload};
}
async function serviceAction(action, serviceId) {
  const endpoint = serviceEndpoint(action);
  if (!endpoint) {
    setServiceActionState({kind:"error", title:"Service action failed", message:`Unknown action: ${action}`});
    return;
  }
  setServiceActionState({kind:"working", title:"Action started", message:`Requesting ${action.replace("_", " ")} for ${serviceId}...`});
  try {
    let {response, payload} = await callServiceEndpoint(endpoint, serviceId);
    if (payload.confirmation_required) {
      setServiceActionState({
        kind:"pending",
        title:"Pending confirmation",
        message:payload.message || `Confirm ${action.replace("_", " ")} for ${serviceId}.`,
        command:payload.command || ""
      });
      const approved = window.confirm(`${payload.message || "Confirmation required."}\n\n${payload.command || ""}`);
      if (!approved) {
        setServiceActionState({kind:"warn", title:"Action cancelled", message:"No service action was executed."});
        return;
      }
      setServiceActionState({kind:"working", title:"Action started", message:`Running confirmed action for ${serviceId}...`});
      ({response, payload} = await callServiceEndpoint(endpoint, serviceId, payload.confirmation_key));
    }
    if (!response.ok || !payload.ok) {
      throw new Error(payload.error || payload.message || `Service action failed (${response.status}).`);
    }
    const service = payload.service || {};
    const pid = service.pid || payload.result?.results?.find?.(row=>row.pid)?.pid || "";
    setServiceActionState({
      kind:"success",
      title:"Action completed",
      message:payload.message || `${action} completed for ${serviceId}.`,
      pid,
      health:service.health || "",
      detail:service.detail || ""
    });
    await refreshMaintenanceServices();
  } catch (error) {
    setServiceActionState({
      kind:"error",
      title:"Service action failed",
      message:String(error?.message || error),
      detail:"Check the service row logs and last error below."
    });
    try { await refreshMaintenanceServices(); } catch (_) {}
  }
}
async function refreshServiceHealth() {
  setServiceActionState({kind:"working", title:"Health check started", message:"Refreshing service and system health..."});
  try {
    await refreshMaintenanceServices();
    setServiceActionState({kind:"success", title:"Health check completed", message:"Service status and the health pill were refreshed."});
  } catch (error) {
    setServiceActionState({kind:"error", title:"Health check failed", message:String(error?.message || error)});
  }
}
async function runDashboardChatSmokeTest() {
  dashboardChatTestState = {kind:"working", message:"Running isolated Dashboard Chat smoke tests..."};
  if (active === "maintenance") render();
  try {
    const response = await fetch("/api/dashboard-chat-tests/run", {method:"POST"});
    const payload = await response.json();
    if (!response.ok || !payload.ok) throw new Error(payload.error || `Smoke test failed (${response.status}).`);
    const tests = payload.tests || {};
    dashboardChatTestState = {
      kind: tests.failed ? "error" : "success",
      message: `Smoke test completed: ${tests.passed || 0} passed, ${tests.failed || 0} failed.`,
      detail: tests.report || ""
    };
    await refreshMaintenanceServices();
  } catch (error) {
    dashboardChatTestState = {kind:"error", message:String(error?.message || error)};
    if (active === "maintenance") render();
  }
}
async function viewDashboardChatTestReport() {
  try {
    const response = await fetch("/api/dashboard-chat-tests/report");
    const payload = await response.json();
    dashboardChatTestState = {
      kind: payload.failed ? "error" : "success",
      message: payload.exists ? `${payload.passed || 0} passed, ${payload.failed || 0} failed.` : "No Dashboard Chat test report exists yet.",
      detail: payload.content || payload.report || ""
    };
  } catch (error) {
    dashboardChatTestState = {kind:"error", message:String(error?.message || error)};
  }
  if (active === "maintenance") render();
}
async function refreshSelfHealing() {
  const response = await fetch("/api/self-healing");
  const payload = await response.json();
  if (!response.ok || !payload.ok) throw new Error(payload.error || `Self-Healing API returned ${response.status}.`);
  data.self_healing = payload.self_healing || payload;
  if (data.maintenance) data.maintenance.self_healing = data.self_healing;
  if (active === "selfhealing" || active === "maintenance") render();
  return data.self_healing;
}
async function selfHealingAction(action, options={}) {
  selfHealingActionState = {kind:"working", message:`Running self-healing action: ${action}...`};
  if (active === "selfhealing" || active === "maintenance") render();
  try {
    let response = await fetch(`/api/self-healing/${action}`, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify(options)
    });
    let payload = await response.json();
    if (payload.confirmation_required) {
      const approved = window.confirm(`${payload.message || "Confirmation required."}\n\n${payload.command || ""}`);
      if (!approved) {
        selfHealingActionState = {kind:"warn", message:"Self-healing action cancelled. No repair was run."};
        render();
        return;
      }
      response = await fetch(`/api/self-healing/${action}`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({...options, confirmation_key:payload.confirmation_key})
      });
      payload = await response.json();
    }
    if (!response.ok || !payload.ok) throw new Error(payload.error || payload.message || `Self-healing action failed (${response.status}).`);
    data.self_healing = payload.self_healing || payload.result?.self_healing || data.self_healing;
    if (data.maintenance) data.maintenance.self_healing = data.self_healing;
    selfHealingActionState = {kind:"success", message:payload.message || `${action} completed.`, detail:JSON.stringify(payload.result || payload, null, 2)};
    await refreshSelfHealing();
  } catch (error) {
    selfHealingActionState = {kind:"error", message:String(error?.message || error)};
    if (active === "selfhealing" || active === "maintenance") render();
  }
}
function selfHealingPlan(issueId) {
  selfHealingAction("plan", {issue_id:issueId});
}
function selfHealingApprove(repairId) {
  selfHealingAction("approve", {repair_id:repairId});
}
function selfHealingRun(repairId) {
  selfHealingAction("run", {repair_id:repairId});
}
function renderSelfHealing() {
  const sh = data.self_healing || data.maintenance?.self_healing || {};
  const issues = sh.active_issues || [];
  const history = sh.repair_history?.history || [];
  const notes = sh.notes || {};
  return `
    <article class="card full ${issues.some(row=>row.severity === "critical") ? "error-banner" : ""}">
      <h2>Self-Healing & Observability</h2>
      <span class="pill ${Number(sh.health_score || 0) >= 80 ? "ok" : Number(sh.health_score || 0) >= 50 ? "warn" : "bad"}">Health score ${esc(sh.health_score ?? "Unknown")}</span>
      <span class="pill">Active issues ${esc(issues.length)}</span>
      <span class="pill">Auto observe ${esc(sh.auto_observe)}</span>
      <span class="pill">Auto repair ${esc(sh.auto_repair)}</span>
      <span class="pill">Approval required ${esc(sh.requires_confirmation)}</span>
      <div class="mt-3">
        <button class="copy" onclick="selfHealingAction('observe')">Observe system</button>
        <button class="copy" onclick="selfHealingAction('detect')">Detect issues</button>
        <button class="copy" onclick="selfHealingAction('brief')">Reliability brief</button>
        <button class="copy" onclick="refreshSelfHealing()">Refresh</button>
      </div>
      ${selfHealingActionState ? `<p class="${selfHealingActionState.kind === "error" ? "bad" : selfHealingActionState.kind === "success" ? "ok" : "muted"}">${esc(selfHealingActionState.message || "")}</p>${selfHealingActionState.detail ? `<pre>${esc(selfHealingActionState.detail)}</pre>` : ""}` : ""}
      <p class="muted">Runtime: ${esc(sh.runtime || "")}</p>
    </article>
    <article class="card full">
      <h2>Active Issues</h2>
      ${table(issues, [
        ["Issue","issue_id"],
        ["Severity","severity",value=>`<span class="${statusClass(value)}">${esc(value)}</span>`],
        ["System","affected_system"],
        ["Symptoms","symptoms",value=>esc((value || []).join("; "))],
        ["Recommended Repair","recommended_fix"],
        ["Repairability","repairability"],
        ["Actions","issue_id",(value,row)=>`
          <button class="copy" onclick="selfHealingPlan('${esc(value)}')">Create repair plan</button>
          <button class="copy" onclick="copyCommand('python raphael.py diagnose-issue ${esc(value)}')">Copy diagnose</button>
          <details><summary class="muted">Evidence</summary><pre>${esc((row.evidence || []).join("\\n"))}</pre></details>`]
      ])}
    </article>
    <article class="card full">
      <h2>Repair History</h2>
      ${history.length ? table(history.slice(-20).reverse(), [
        ["Time","timestamp"],
        ["Repair","repair_id"],
        ["Issue","issue_id"],
        ["Action","action",value=>esc(JSON.stringify(value || {}))]
      ]) : `<div class="empty">No repairs have run yet.</div>`}
    </article>
    ${Object.values(notes).map(note=>card(note.label || "Self-Healing Note", note.exists ? `<div class="muted">${esc(note.updated)}</div><pre>${esc(note.content)}</pre>` : `<div class="empty">Missing note.</div>`, "card wide")).join("")}
  `;
}
function renderMaintenance() {
  const m = data.maintenance;
  if (!m) return `<article class="card full"><h2>Maintenance</h2><div class="empty">Maintenance data is unavailable. Run <code>python raphael.py system-check</code>.</div></article>`;
  const h = m.system_health || {};
  const b = m.bootstrap || {};
  const bg = b.groups || {};
  const sm = m.service_manager || {};
  const docker = sm.docker || {};
  const serviceRows = sm.services || [];
  const chatTests = m.dashboard_chat_tests || {};
  const selfHealing = m.self_healing || {};
  return `
    <article class="card full maintenance-hero ${m.overall === "healthy" ? "healthy" : "attention"}">
      <div>
        <h2>System Maintenance</h2>
        <p class="muted">Diagnostics and recovery helpers only. No project/source edits or external actions.</p>
      </div>
      <div class="stat">${esc(m.overall === "healthy" ? "Healthy" : "Needs Attention")}</div>
    </article>
    ${m.config_health.errors.length ? `<article class="card full error-banner"><strong>Configuration errors</strong>${m.config_health.errors.map(item=>`<span>${esc(item)}</span>`).join("")}</article>` : ""}
    ${serviceActionState ? `<article class="card full ${serviceActionState.kind === "error" ? "error-banner" : ""}">
      <h2>${esc(serviceActionState.title)}</h2>
      <p class="${serviceActionState.kind === "success" ? "ok" : serviceActionState.kind === "error" ? "bad" : "muted"}">${esc(serviceActionState.message || "")}</p>
      ${serviceActionState.command ? `<pre>${esc(serviceActionState.command)}</pre>` : ""}
      ${serviceActionState.pid ? `<span class="pill">PID ${esc(serviceActionState.pid)}</span>` : ""}
      ${serviceActionState.health ? `<span class="pill">Health ${esc(serviceActionState.health)}</span>` : ""}
      ${serviceActionState.detail ? `<pre>${esc(serviceActionState.detail)}</pre>` : ""}
    </article>` : ""}
    <article class="card full ${chatTests.failed ? "error-banner" : ""}">
      <h2>Dashboard Chat Tests</h2>
      <span class="pill ${chatTests.failed ? "bad" : "ok"}">Failed tests ${esc(chatTests.failed || 0)}</span>
      <span class="pill">Passed ${esc(chatTests.passed || 0)}</span>
      ${chatTests.updated ? `<span class="pill">Updated ${esc(chatTests.updated)}</span>` : ""}
      <div class="mt-3">
        <button class="copy" onclick="runDashboardChatSmokeTest()">Run smoke test</button>
        <button class="copy" onclick="viewDashboardChatTestReport()">View latest report</button>
      </div>
      <div class="muted mt-3">${esc(chatTests.report || "No report generated yet.")}</div>
      ${dashboardChatTestState ? `<p class="${dashboardChatTestState.kind === "error" ? "bad" : dashboardChatTestState.kind === "success" ? "ok" : "muted"}">${esc(dashboardChatTestState.message || "")}</p>${dashboardChatTestState.detail ? `<pre>${esc(dashboardChatTestState.detail)}</pre>` : ""}` : ""}
    </article>
    <article class="card full ${Number(selfHealing.health_score || 100) < 80 ? "error-banner" : ""}">
      <h2>Self-Healing Summary</h2>
      <span class="pill ${Number(selfHealing.health_score || 0) >= 80 ? "ok" : "bad"}">Health score ${esc(selfHealing.health_score ?? "Unknown")}</span>
      <span class="pill">Active issues ${esc((selfHealing.active_issues || []).length)}</span>
      <span class="pill">Repair history ${esc(selfHealing.repair_history_count || 0)}</span>
      <div class="mt-3">
        <button class="copy" onclick="active='selfhealing'; render();">Open Self-Healing</button>
        <button class="copy" onclick="selfHealingAction('observe')">Observe system</button>
        <button class="copy" onclick="selfHealingAction('detect')">Detect issues</button>
        <button class="copy" onclick="selfHealingAction('brief')">Reliability brief</button>
      </div>
      <p class="muted">Repairs remain approval-gated and allowlisted. No arbitrary shell, deletion, upload, spending, or unmanaged process killing.</p>
    </article>
    <article class="card full">
      <h2>Docker Services</h2>
      <span class="pill ${docker.healthy ? "ok" : "bad"}">Docker ${docker.available ? "Online" : "Unavailable"}</span>
      ${docker.version ? `<span class="pill">Version ${esc(docker.version)}</span>` : ""}
      ${docker.platform ? `<span class="pill">${esc(docker.platform)}</span>` : ""}
      <div class="mt-3">
        <button class="copy" onclick="serviceAction('start','qdrant')">Start Qdrant</button>
        <button class="copy" onclick="serviceAction('restart','qdrant')">Restart Qdrant</button>
        <button class="copy" onclick="serviceAction('open','qdrant')">Open Qdrant URL</button>
        <button class="copy" onclick="serviceAction('health','qdrant')">Docker Health</button>
        <button class="copy" onclick="showDockerLogs('qdrant')">Show Docker Logs</button>
      </div>
      <p class="${docker.error ? "bad" : "muted"}">${esc(docker.error || "Only allowlisted, localhost-bound, Raphael-labeled containers can be changed.")}</p>
      <div class="muted">Docker registry: ${esc(sm.docker_registry_path || "")}</div>
    </article>
    <article class="card full">
      <h2>Service Manager</h2>
      <div>
        <button class="copy" onclick="serviceAction('start_stack','required')">Start All Required</button>
        <button class="copy" onclick="serviceAction('start_stack','creative')">Start Creative Stack</button>
        <button class="copy" onclick="serviceAction('start_stack','voice')">Start Voice Stack</button>
        <button class="copy" onclick="serviceAction('start_stack','research')">Start Research Stack</button>
        <button class="copy" onclick="sendQuickChat('restart failed services')">Restart Failed Services</button>
        <button class="copy" onclick="refreshServiceHealth()">Run Health Check</button>
        <button class="copy" onclick="serviceAction('open','dashboard')">Open Dashboard</button>
        <button class="copy" onclick="serviceAction('open','comfyui')">Open ComfyUI</button>
      </div>
      ${sm.error ? `<div class="maintenance-error"><strong>Service Manager unavailable</strong><span>${esc(sm.error)}</span></div>` : ""}
      ${table(serviceRows, [
        ["Service","display_name"],
        ["Status","status",value=>`<span class="${statusClass(value)}">${esc(value)}</span>`],
        ["Health","health",value=>`<span class="${statusClass(value)}">${esc(value)}</span>`],
        ["PID","pid"],
        ["Category","category"],
        ["Actions","service_id",(value,row)=>`
          <button class="copy" onclick="serviceAction('start','${esc(value)}')">Start</button>
          <button class="copy" onclick="serviceAction('stop','${esc(value)}')">Stop</button>
          <button class="copy" onclick="serviceAction('restart','${esc(value)}')">Restart</button>
          <button class="copy" onclick="serviceAction('health','${esc(value)}')">Health</button>
          ${row.health_check_type === "url" ? `<button class="copy" onclick="serviceAction('open','${esc(value)}')">Open</button>` : ""}
          <details><summary class="muted">Logs / last error</summary>
            <div class="${row.last_error ? "bad" : "muted"}">${esc(row.last_error || "No error")}</div>
            <pre>${esc(row.logs || "No managed logs.")}</pre>
          </details>`]
      ])}
      <div class="muted mt-3">Registry: ${esc(sm.registry_path || "")}</div>
      <p class="muted">Only registry allowlisted commands run. Stop affects Raphael-managed PIDs only.</p>
    </article>
    <article class="card full">
      <h2>Bootstrap / Launcher</h2>
      <span class="pill">Core ${esc(bg.core || "Unknown")}</span>
      <span class="pill">AI ${esc(bg.ai || "Unknown")}</span>
      <span class="pill">Creative ${esc(bg.creative || "Unknown")}</span>
      <span class="pill">Voice ${esc(bg.voice || "Unknown")}</span>
      <div class="mt-3">
        <button class="copy" onclick="sendQuickChat('start Raphael services')">Start Raphael</button>
        <button class="copy" onclick="sendQuickChat('stop Raphael services')">Stop Raphael</button>
        <button class="copy" onclick="sendQuickChat('restart Raphael services')">Restart Raphael</button>
        <button class="copy" onclick="sendQuickChat('open dashboard')">Open Dashboard</button>
        <button class="copy" onclick="sendQuickChat('run bootstrap health')">Run Health Check</button>
        <button class="copy" onclick="sendQuickChat('install Raphael startup')">Install Startup</button>
        <button class="copy" onclick="sendQuickChat('remove Raphael startup')">Remove Startup</button>
      </div>
      <p class="muted mt-3">Dashboard ${esc(b.dashboard_url || "")} · ComfyUI ${esc(b.comfyui_url || "")}</p>
      <p class="muted">Stop, restart, install, and remove remain confirmation-gated through Command Bus.</p>
    </article>
    <article class="card full">
      <h2>Managed Service PIDs</h2>
      ${table(b.managed_pids || [], [["Service","service"],["PID","pid"],["Started","started"],["Command","command"],["Log","log"]])}
      <div class="muted mt-3">Registry: ${esc(b.pid_registry || "")}</div>
    </article>
    <article class="card wide">
      <h2>Bootstrap Services</h2>
      ${table(Object.entries(b.services || {}).map(([service,row])=>({service,ok:row.ok,detail:row.detail || ""})), [["Service","service"],["Status","ok",v=>maintenanceState(!!v)],["Detail","detail"]])}
    </article>
    <article class="card wide">
      <h2>POD / Voice Tools</h2>
      ${table(Object.entries(b.tools || {}).map(([tool,row])=>({tool,exists:row.exists,path:row.path})), [["Tool","tool"],["Status","exists",v=>v ? maintenanceState(true) : `<span class="maintenance-state warn">Missing / optional</span>`],["Path","path"]])}
    </article>
    <article class="card wide"><h2>Last Startup</h2>${b.startup?.exists ? `<pre>${esc(b.startup.content)}</pre>` : `<div class="empty">No startup log.</div>`}</article>
    <article class="card wide"><h2>Last Recovery</h2>${b.recovery?.exists ? `<pre>${esc(b.recovery.content)}</pre>` : `<div class="empty">No recovery log.</div>`}</article>
    <article class="card wide"><h2>Bootstrap Health</h2>${b.health?.exists ? `<pre>${esc(b.health.content)}</pre>` : `<div class="empty">Run bootstrap-health.</div>`}</article>
    <article class="card wide"><h2>Bootstrap Review</h2>${b.review?.exists ? `<pre>${esc(b.review.content)}</pre>` : `<div class="empty">Run bootstrap-review.</div>`}</article>
    <article class="card">
      <h2>System Health</h2>
      ${maintenanceState(m.overall === "healthy")}
      <p class="muted">Generated ${esc(m.generated)}</p>
    </article>
    <article class="card">
      <h2>Config Health</h2>
      ${maintenanceState(m.config_health.ok)}
      <div>${m.config_health.warnings.map(item=>`<p class="muted">${esc(item)}</p>`).join("") || `<p class="muted">No config warnings.</p>`}</div>
    </article>
    <article class="card">
      <h2>API Health</h2>
      ${maintenanceState(m.api_health.ok)}
      <p class="muted">${m.api_health.routes.length} routes · ${m.api_health.missing.length} missing</p>
    </article>
    <article class="card">
      <h2>Ollama</h2>
      ${maintenanceState(m.ollama_status.ok)}
      <div>${(m.ollama_status.models || []).map(model=>`<span class="pill">${esc(model)}</span>`).join("") || `<div class="empty">No Ollama models detected.</div>`}</div>
    </article>
    <article class="card">
      <h2>Qdrant</h2>
      ${maintenanceState(m.qdrant_status.ok)}
      <p class="muted">${esc(m.qdrant_status.detail)}</p>
    </article>
    <article class="card">
      <h2>Voice</h2>
      ${maintenanceState(!!m.voice_status.model_exists)}
      <p class="muted">Engine ${esc(m.voice_status.engine)} · control ${esc(m.voice_status.control_enabled)}</p>
    </article>
    <article class="card full">
      <h2>Dependencies</h2>
      ${table(m.dependencies.records, [
        ["Dependency","name"],
        ["Required","required", value=>value ? "yes" : "optional"],
        ["Status","available", (value,row)=>value ? maintenanceState(true) : row.required ? maintenanceState(false) : `<span class="maintenance-state warn">Optional missing</span>`]
      ])}
    </article>
    <article class="card full">
      <h2>Dashboard Routes</h2>
      ${m.api_health.routes.length ? table(m.api_health.routes, [["Route","path"],["Methods","methods"]]) : `<div class="empty">No dashboard routes detected.</div>`}
    </article>
    <article class="card wide">
      <h2>Recent Errors</h2>
      ${m.recent_errors.length ? m.recent_errors.map(row=>`<div class="maintenance-error"><strong>${esc(row.source)}</strong><span>${esc(row.message)}</span></div>`).join("") : `<div class="empty">No recent errors found.</div>`}
    </article>
    <article class="card wide">
      <h2>Recovery Commands</h2>
      ${m.commands.map(command=>`<button class="copy" onclick="copyCommand('${esc(command)}')">${esc(command)}</button>`).join("")}
      <h2 class="mt-3">Helper Scripts</h2>
      ${m.helpers.map(path=>`<button class="copy" onclick="copyCommand('${esc(path.replace(/\\/g, "\\\\"))}')">${esc(path)}</button>`).join("")}
    </article>
    <article class="card full">
      <h2>Safety Boundary</h2>
      <span class="pill">${esc(m.safety.backup_scope)}</span>
      <span class="pill">${esc(m.safety.repair_scope)}</span>
      <span class="pill">${esc(m.safety.cleanup_scope)}</span>
      <span class="pill">Project/source edits ${esc(m.safety.project_source_edits)}</span>
      <span class="pill">External actions ${esc(m.safety.external_actions)}</span>
    </article>
  `;
}
function render() {
  document.querySelectorAll("nav button").forEach(btn => btn.classList.toggle("active", btn.dataset.page === active));
  document.getElementById("title").textContent = pages.find(p => p[0] === active)?.[1] || "Dashboard";
  if (!data) {
    document.getElementById("content").innerHTML = `<article class="card full"><h2>Loading</h2><div class="empty">Loading Raphael dashboard data...</div></article>`;
    return;
  }
  const map = {home:renderHome, chat:renderChat, daily:renderDailyOperatingLoop, knowledge:renderKnowledge, relationships:renderKnowledgeRelationships, n8nstudio:renderN8nStudio, workflowrunner:renderWorkflowRunner, communications:renderCommunications, commandbus:renderCommandBus, notifications:renderNotifications, activity:renderActivityStream, briefs:renderExecutiveBriefs, identity:renderIdentity, world:renderWorldModel, simulations:renderSimulations, opportunities:renderOpportunities, allocation:renderAllocation, blueprints:renderBlueprints, commerce:renderCommerce, podstudio:renderPODStudio, assetlibrary:renderAssetLibrary, agency:renderAgency, creator:renderCreator, kpis:renderKPIs, finance:renderFinance, portfolio:renderPortfolio, initiatives:renderInitiatives, employees:renderEmployees, executionplans:renderExecutionPlans, execution:renderExecution, builder:renderBuilder, projects:renderProjects, goals:renderGoals, goalpropagation:renderGoalPropagation, deliberations:renderDeliberations, tasks:renderTasks, agents:renderAgents, councils:renderCouncils, workflows:renderWorkflows, memory:renderMemory, voice:renderVoice, vision:renderVision, search:renderSearch, health:renderHealth, selfhealing:renderSelfHealing, maintenance:renderMaintenance};
  window.__classicRenderMap = map;
  if (document.body.classList.contains("matrix-view") && active === "home" && window.RaphaelMatrix) {
    window.RaphaelMatrix.renderMatrixHome();
    return;
  }
  document.getElementById("content").innerHTML = map[active]();
  if (active === "chat") {
    initRaphaelOrb();
    initDashboardVoiceBridge();
    setDashboardVoiceState(dashboardVoiceState, dashboardVoiceMessage);
    const input = document.getElementById("chat-input");
    if (input) input.addEventListener("keydown", event => {
      if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) sendChat();
    });
  }
}
function initNav() {
  document.getElementById("nav").innerHTML = pages.map(([id,label]) => `<button data-page="${id}">${label}</button>`).join("");
  document.querySelectorAll("nav button").forEach(btn => btn.onclick = () => { active = btn.dataset.page; render(); });
}
async function load() {
  initNav();
  const res = await fetch("/api/overview");
  if (!res.ok) throw new Error(`Overview API returned ${res.status}`);
  data = await res.json();
  window.data = data;
  document.getElementById("generated").textContent = `Generated ${data.generated}`;
  const bell = document.getElementById("notification-bell");
  if (bell) {
    const count = data.counts.notifications_critical_high || 0;
    bell.textContent = `Notifications ${count}`;
    bell.classList.toggle("bad", count > 0);
  }
  const activityCounter = document.getElementById("activity-counter");
  if (activityCounter) {
    activityCounter.textContent = `Activity ${data.counts.activity_today || 0}`;
  }
  const bootstrapPill = document.getElementById("bootstrap-health-pill");
  if (bootstrapPill) {
    const groups = data.maintenance?.bootstrap?.groups || {};
    bootstrapPill.textContent = `Core: ${groups.core || "Unknown"} · AI: ${groups.ai || "Unknown"} · Creative: ${groups.creative || "Unknown"} · Voice: ${groups.voice || "Unknown"}`;
    bootstrapPill.classList.toggle("bad", [groups.core, groups.ai, groups.creative].includes("Warning"));
  }
  if (window.RaphaelMatrix) window.RaphaelMatrix.afterDataLoad();
  render();
}
load().catch(err => {
  document.body.classList.remove("matrix-view");
  document.body.classList.add("classic-view");
  document.getElementById("content").innerHTML = `<article class="card full error-banner"><h2>Dashboard Error</h2><p>Raphael could not load dashboard data. The CLI remains available.</p><pre>${esc(err)}</pre><button class="copy" onclick="location.reload()">Retry</button><button class="copy" onclick="copyCommand('python raphael.py system-check')">Copy system check</button></article>`;
});
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return INDEX_HTML


@app.get("/api/overview")
def api_overview() -> JSONResponse:
    return JSONResponse(overview())


@app.get("/api/health")
def api_health() -> JSONResponse:
    return JSONResponse(system_health())


@app.get("/api/maintenance")
def api_maintenance() -> JSONResponse:
    return JSONResponse(maintenance_data())


@app.get("/api/self-healing")
def api_self_healing() -> JSONResponse:
    return JSONResponse({"ok": True, "self_healing": self_healing_data()})


@app.post("/api/self-healing/{action}")
def api_self_healing_action(action: str, payload: dict[str, Any] = Body(default={})) -> JSONResponse:
    result, status = self_healing_bus_action(action, payload or {})
    return JSONResponse(result, status_code=status)


@app.get("/api/dashboard-chat-tests/report")
def api_dashboard_chat_test_report() -> JSONResponse:
    return JSONResponse(dashboard_chat_test_status_data())


@app.post("/api/dashboard-chat-tests/run")
def api_dashboard_chat_test_run() -> JSONResponse:
    result, status = run_dashboard_chat_smoke_test()
    return JSONResponse(result, status_code=status)


@app.get("/api/services/status")
def api_services_status() -> JSONResponse:
    return JSONResponse(service_manager_data())


@app.post("/api/services/start")
def api_services_start(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = service_bus_action("start", payload)
    return JSONResponse(result, status_code=status)


@app.post("/api/services/stop")
def api_services_stop(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = service_bus_action("stop", payload)
    return JSONResponse(result, status_code=status)


@app.post("/api/services/restart")
def api_services_restart(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = service_bus_action("restart", payload)
    return JSONResponse(result, status_code=status)


@app.post("/api/services/health")
def api_services_health(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = service_bus_action("health", payload)
    return JSONResponse(result, status_code=status)


@app.post("/api/services/start-stack")
def api_services_start_stack(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = service_bus_action("start_stack", payload)
    return JSONResponse(result, status_code=status)


@app.post("/api/services/open")
def api_services_open(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = service_bus_action("open", payload)
    return JSONResponse(result, status_code=status)


@app.get("/api/services")
def api_services_compat() -> JSONResponse:
    return JSONResponse(service_manager_data())


@app.post("/api/services/action")
def api_services_action_compat(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    action = str(payload.get("action", "")).replace("-", "_")
    result, status = service_bus_action(action, payload)
    return JSONResponse(result, status_code=status)


@app.get("/api/workflow-runner")
def api_workflow_runner() -> JSONResponse:
    return JSONResponse(workflow_runner_data())


@app.post("/api/workflow-runner/execute")
def api_workflow_runner_execute(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = workflow_bus_action("execute", payload)
    return JSONResponse(result, status_code=status)


@app.post("/api/workflow-runner/cancel")
def api_workflow_runner_cancel(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = workflow_bus_action("cancel", payload)
    return JSONResponse(result, status_code=status)


@app.post("/api/workflow-runner/monitor")
def api_workflow_runner_monitor(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = workflow_cli_read("workflow-monitor", str(payload.get("exec_id", "")))
    return JSONResponse(result, status_code=status)


@app.post("/api/workflow-runner/result")
def api_workflow_runner_result(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result, status = workflow_cli_read("workflow-result", str(payload.get("exec_id", "")))
    return JSONResponse(result, status_code=status)


@app.get("/api/knowledge")
def api_knowledge() -> JSONResponse:
    return JSONResponse(knowledge_data())


@app.get("/api/knowledge/relationships")
def api_knowledge_relationships() -> JSONResponse:
    return JSONResponse(knowledge_relationship_data())


@app.get("/api/communications/network")
def api_communications_network() -> JSONResponse:
    data = communication_data()
    return JSONResponse({"network": data["network"], "requests": data["requests"], "responses": data["responses"], "escalations": data["escalations"]})


@app.get("/api/communications/open")
def api_communications_open() -> JSONResponse:
    return JSONResponse(communication_data()["open_requests"])


@app.get("/api/communications/recommendations")
def api_communications_recommendations() -> JSONResponse:
    return JSONResponse(communication_data()["recommendations"])


@app.get("/api/communications/syntheses")
def api_communications_syntheses() -> JSONResponse:
    return JSONResponse(communication_data()["syntheses"])


@app.get("/api/notifications/sectors")
def api_notification_sectors() -> JSONResponse:
    return JSONResponse(notification_data().get("sector_counts", {}))


@app.get("/api/activity/summary")
def api_activity_summary() -> JSONResponse:
    return JSONResponse(activity_data().get("summary", {}))


@app.get("/api/activity/sectors")
def api_activity_sectors() -> JSONResponse:
    return JSONResponse(activity_data().get("sector_counts", {}))


@app.get("/api/councils/status")
def api_councils_status() -> JSONResponse:
    return JSONResponse(council_status_data())


@app.get("/api/councils/activity")
def api_councils_activity() -> JSONResponse:
    return JSONResponse(council_activity_data())


@app.get("/api/matrix/departments")
def api_matrix_departments() -> JSONResponse:
    return JSONResponse(matrix_department_data())


@app.get("/api/councils/chambers")
def api_councils_chambers() -> JSONResponse:
    return JSONResponse(council_chamber_data())


@app.get("/api/employees/network")
def api_employees_network() -> JSONResponse:
    return JSONResponse(employee_network_data())


@app.get("/api/raphael/presence")
def api_raphael_presence() -> JSONResponse:
    return JSONResponse(raphael_presence_data())


@app.post("/api/raphael/presence/action")
def api_raphael_presence_action(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    result = raphael_presence_action(payload)
    return JSONResponse(result, status_code=200 if result.get("accepted") else 400)


@app.post("/api/chat")
def api_chat(payload: dict[str, Any] = Body(...)) -> JSONResponse:
    phrase = str(payload.get("message", "")).strip()
    if not phrase:
        return JSONResponse(
            {
                "response": "Type a message for Raphael first.",
                "intent": "empty",
                "command": "",
                "status": "Empty",
                "confirmation_required": False,
                "awaiting_confirmation": False,
            }
        )
    return JSONResponse(dashboard_chat_response(
        phrase,
        test_mode=bool(payload.get("test_mode", False)),
        test_session_id=str(payload.get("test_session_id", "")),
        reset_test_session=bool(payload.get("reset_test_session", False)),
        test_scenario=str(payload.get("test_scenario", "")),
    ))
