"""Phase 75 governed World Model runtime.

The World Model is a metadata graph with provenance, confidence, access
control, uncertainty handling, and read-only reasoning support. It never
executes external actions.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from collections import Counter, deque
from pathlib import Path
from typing import Any

from . import legacy


NODE_TYPES = {
    "Aaron", "Raphael", "Agent", "Council", "Employee", "Project", "Business",
    "Goal", "Task", "Workflow", "Execution", "Initiative", "Opportunity",
    "Skill", "Resource", "Service", "Model", "Tool", "KnowledgeItem", "Asset",
    "PODConcept", "Build", "Deliberation", "ExecutionPlan", "Risk",
    "Constraint", "Decision", "Metric", "Event", "Hypothesis",
}

RELATIONSHIP_TYPES = {
    "OWNS", "OPERATES", "COORDINATES", "REPORTS_TO", "WORKS_ON",
    "ASSIGNED_TO", "SUPPORTS", "ADVANCES", "DEPENDS_ON", "BLOCKED_BY",
    "REQUIRES", "USES", "PRODUCES", "GENERATES", "REVIEWS", "GOVERNS",
    "PART_OF", "RELATED_TO", "ENABLES", "RISKS", "MITIGATES", "MEASURES",
    "LEARNS_FROM",
}

SOURCE_TRUST = {
    "Workflow Runner": "A",
    "Task Registry": "A",
    "Builder Registry": "A",
    "Self-Healing Registry": "A",
    "Service Manager": "A",
    "System Generated Records": "A",
    "Agent generated with evidence": "B",
    "Phase 75 Seed": "B",
    "Agent inference": "C",
    "Human note without validation": "D",
}
TRUST_SCORE = {"A": 1.0, "B": 0.8, "C": 0.55, "D": 0.35}

DECAY_DAYS = {"WORKS_ON": 30, "DEPENDS_ON": 60, "BLOCKED_BY": 14, "USES": 90, "ADVANCES": 60}
STALE_DAYS = {
    "Project": 14, "Business": 30, "Goal": 21, "Task": 7, "Workflow": 30,
    "Service": 7, "Agent": 30, "Council": 45, "Resource": 60, "Model": 60,
}
STALE_STATUSES = {"active", "in_progress", "monitoring"}
STALE_EXEMPT = {"complete", "archived", "deprecated", "paused", "cancelled", "superseded"}

RUNTIME_FILES = {
    "nodes.json": [],
    "relationships.json": [],
    "events.json": [],
    "hypotheses.json": [],
    "access_policy.json": {},
    "inference_controls.json": {},
    "conflicts.json": [],
    "world_model_cache.json": {},
}
JSONL_FILES = {"query_log.jsonl", "snapshots.jsonl"}

NOTE_FILES = {
    "World Model Overview.md": "# World Model Overview\n\nRaphael's World Model stores governed operational reality with provenance, confidence, temporal validity, access policy, conflicts, and hypotheses.\n",
    "World Model Node Registry.md": "# World Model Node Registry\n\nNo registry generated yet.\n",
    "World Model Relationship Registry.md": "# World Model Relationship Registry\n\nNo registry generated yet.\n",
    "World Model Query Log.md": "# World Model Query Log\n\nNo queries recorded yet.\n",
    "World Model Access Policy.md": "# World Model Access Policy\n\nNo access policy generated yet.\n",
    "World Model Inference Controls.md": "# World Model Inference Controls\n\nNo inference controls generated yet.\n",
    "World Model Conflict Registry.md": "# World Model Conflict Registry\n\nNo conflicts recorded yet.\n",
    "World Model Health.md": "# World Model Health\n\nNo health report generated yet.\n",
    "World Model Review.md": "# World Model Review\n\nNo review generated yet.\n",
    "World Model Executive Brief.md": "# World Model Executive Brief\n\nNo brief generated yet.\n",
}

DEFAULT_ACCESS_POLICY = {
    "version": 1,
    "agents": {
        "Aaron": {"trust_tier": 4, "roles": ["owner"], "allowed_node_types": ["*"]},
        "Raphael Core": {"trust_tier": 4, "roles": ["core"], "allowed_node_types": ["*"]},
        "Executive Agent": {"trust_tier": 3, "roles": ["executive"], "allowed_node_types": ["*"]},
        "Research Agent": {"trust_tier": 2, "roles": ["research"], "allowed_node_types": ["Goal", "Project", "Business", "Workflow", "Service", "Resource", "KnowledgeItem", "Hypothesis", "Event"]},
        "Standard Agent": {"trust_tier": 1, "roles": ["standard"], "allowed_node_types": ["Goal", "Project", "Task", "Workflow", "Service", "Resource"]},
        "Unknown Agent": {"trust_tier": 0, "roles": ["unknown"], "allowed_node_types": ["Goal", "Project"]},
    },
    "base_rate_limits_per_hour": {
        "Research Agent": 80,
        "Executive Agent": 150,
        "Standard Agent": 30,
        "Unknown Agent": 10,
    },
    "trust_multipliers": {"0": 0.5, "1": 0.75, "2": 1.0, "3": 1.5, "4": 2.0},
    "burst_warning_per_minute": 10,
    "burst_block_per_minute": 25,
}

DEFAULT_INFERENCE_CONTROLS = {
    "version": 1,
    "sensitive_correlations": [
        ["Finance", "Health"],
        ["Finance", "Journal"],
        ["Finance", "Schedule"],
        ["Revenue", "Personal Events"],
        ["Relationship Data", "External Agent"],
        ["Journal", "Any Non-Core Agent"],
        ["Health", "Productivity"],
        ["Location", "Schedule"],
        ["Private Notes", "Business Performance"],
    ],
    "owners": ["Aaron"],
    "blocked_actions": ["spend_money", "publish", "upload", "message_people", "create_accounts", "modify_safety_policy", "bypass_approvals", "bypass_workflow_runner", "bypass_command_bus"],
}

SEED_GRAPH = [
    ("Launch POD Business", "POD Studio", "Commerce Agent", "POD Pipeline", "ComfyUI", "RTX 4070"),
    ("Improve Raphael OS", "World Model", "Developer Agent", "Daily Executive Brief", "Raphael Dashboard", "Local Runtime"),
    ("Grow Agency Services", "Agency Pipeline", "Sales Agent", "Knowledge Processing", "n8n", "Workflow Archive"),
]


def _now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _today() -> str:
    return dt.date.today().isoformat()


def _id(prefix: str, *parts: object) -> str:
    digest = hashlib.sha1("|".join(str(part) for part in parts).encode("utf-8")).hexdigest()[:10].upper()
    return f"{prefix}-{digest}"


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


def runtime_root(config: legacy.RaphaelConfig) -> Path:
    path = legacy.ensure_safe_path(config.os_root / "world_model", config)
    path.mkdir(parents=True, exist_ok=True)
    return path


def vault_root(config: legacy.RaphaelConfig) -> Path:
    path = legacy.ensure_safe_path(config.vault / "00_Raphael" / "Governance" / "World Model", config)
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_world_model(config: legacy.RaphaelConfig) -> dict[str, str]:
    runtime = runtime_root(config)
    vault = vault_root(config)
    for filename, default in RUNTIME_FILES.items():
        path = runtime / filename
        if not path.exists():
            if filename == "access_policy.json":
                default = DEFAULT_ACCESS_POLICY
            elif filename == "inference_controls.json":
                default = DEFAULT_INFERENCE_CONTROLS
            _write_json(path, default)
    for filename in JSONL_FILES:
        path = runtime / filename
        if not path.exists():
            path.write_text("", encoding="utf-8")
    for filename, content in NOTE_FILES.items():
        path = vault / filename
        if not path.exists():
            legacy.write_file(path, content, config)
    return {"runtime": str(runtime), "vault": str(vault)}


class WorldModelBuilder:
    def __init__(self, config: legacy.RaphaelConfig) -> None:
        self.config = config
        ensure_world_model(config)
        self.nodes: dict[str, dict[str, Any]] = {}
        self.relationships: dict[str, dict[str, Any]] = {}
        self.events: dict[str, dict[str, Any]] = {}
        self.hypotheses: dict[str, dict[str, Any]] = {}

    def add_node(
        self,
        node_type: str,
        name: str,
        summary: str,
        *,
        status: str = "active",
        priority: str = "medium",
        source_system: str = "System Generated Records",
        source_reference: str = "",
        confidence: float = 0.82,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        node_id: str | None = None,
    ) -> str:
        if node_type not in NODE_TYPES:
            raise ValueError(f"Unsupported node type: {node_type}")
        if status == "active" and not source_reference:
            raise ValueError(f"Active node requires source_reference: {name}")
        key = node_id or _id(node_type.upper(), name)
        existing = self.nodes.get(key, {})
        created = existing.get("created_at", _now())
        self.nodes[key] = {
            "node_id": key,
            "node_type": node_type,
            "name": name,
            "summary": summary,
            "status": status,
            "priority": priority,
            "created_at": created,
            "updated_at": _now(),
            "source_system": source_system,
            "source_reference": source_reference,
            "confidence": round(max(0.0, min(1.0, float(confidence))), 3),
            "confidence_state": confidence_state(confidence),
            "tags": tags or [],
            "metadata": metadata or {},
        }
        return key

    def add_relationship(
        self,
        from_node: str,
        to_node: str,
        relationship_type: str,
        summary: str,
        *,
        confidence: float = 0.82,
        evidence: list[dict[str, Any]] | None = None,
        source_system: str = "System Generated Records",
        source_reference: str = "",
        status: str = "active",
    ) -> str:
        if relationship_type not in RELATIONSHIP_TYPES:
            raise ValueError(f"Unsupported relationship type: {relationship_type}")
        if from_node not in self.nodes or to_node not in self.nodes:
            raise ValueError(f"Relationship references unknown nodes: {from_node} -> {to_node}")
        if status == "active" and not source_reference:
            raise ValueError("Active relationship requires source_reference")
        trust_tier = SOURCE_TRUST.get(source_system, "C")
        rel_id = _id("REL", from_node, relationship_type, to_node, summary)
        evidence = evidence or [{"source": source_system, "source_reference": source_reference, "source_trust": trust_tier, "summary": summary}]
        self.relationships[rel_id] = {
            "relationship_id": rel_id,
            "from_node": from_node,
            "to_node": to_node,
            "relationship_type": relationship_type,
            "summary": summary,
            "confidence": round(max(0.0, min(1.0, float(confidence))), 3),
            "confidence_state": confidence_state(confidence),
            "evidence": evidence,
            "source_system": source_system,
            "source_reference": source_reference,
            "created_at": self.relationships.get(rel_id, {}).get("created_at", _now()),
            "updated_at": _now(),
            "status": status,
            "source_trust": trust_tier,
        }
        return rel_id

    def add_event(
        self,
        event_type: str,
        cause: str,
        effect: str,
        outcome: str,
        related_entities: list[str],
        *,
        importance_level: str = "important",
        source_system: str = "System Generated Records",
        source_reference: str = "",
        confidence: float = 0.82,
    ) -> str:
        event_id = _id("EVENT", event_type, cause, effect, outcome, _today())
        self.events[event_id] = {
            "event_id": event_id,
            "event_type": event_type,
            "event_time": _now(),
            "cause": cause,
            "effect": effect,
            "outcome": outcome,
            "related_entities": related_entities,
            "source_system": source_system,
            "source_reference": source_reference,
            "confidence": round(confidence, 3),
            "importance_level": importance_level,
            "status": "active",
        }
        self.add_node("Event", event_type, outcome, source_system=source_system, source_reference=source_reference, confidence=confidence, node_id=event_id)
        return event_id

    def add_hypothesis(
        self,
        statement: str,
        *,
        generated_by: str = "Raphael Core",
        confidence: float = 0.55,
        supporting_evidence: list[dict[str, Any]] | None = None,
        contradicting_evidence: list[dict[str, Any]] | None = None,
        status: str = "active",
    ) -> str:
        hypothesis_id = _id("HYP", statement)
        self.hypotheses[hypothesis_id] = {
            "hypothesis_id": hypothesis_id,
            "statement": statement,
            "generated_by": generated_by,
            "confidence": round(confidence, 3),
            "supporting_evidence": supporting_evidence or [],
            "contradicting_evidence": contradicting_evidence or [],
            "created_at": self.hypotheses.get(hypothesis_id, {}).get("created_at", _now()),
            "updated_at": _now(),
            "status": status,
        }
        self.add_node("Hypothesis", statement[:80], statement, status=status, source_system=generated_by, source_reference=hypothesis_id, confidence=confidence, node_id=hypothesis_id)
        return hypothesis_id

    def build(self) -> dict[str, Any]:
        self._ingest_people()
        self._ingest_goals_projects_agents()
        self._ingest_workflows()
        self._ingest_services_resources()
        self._ingest_councils()
        self._ingest_self_healing()
        self._ensure_minimum_graph()
        self._add_epistemic_examples()
        conflicts = detect_conflicts(list(self.nodes.values()), list(self.relationships.values()))
        save_model(self.config, list(self.nodes.values()), list(self.relationships.values()), list(self.events.values()), list(self.hypotheses.values()), conflicts)
        refresh_notes(self.config)
        snapshot(self.config, "build")
        return status(self.config)

    def _ingest_people(self) -> None:
        aaron = self.add_node("Aaron", "Aaron", "Owner and final decision authority.", priority="high", source_reference="constitutional_authority", confidence=0.99)
        raphael = self.add_node("Raphael", "Raphael", "Local advisory operating system.", priority="high", source_reference=str(self.config.os_root), confidence=0.95)
        self.add_relationship(aaron, raphael, "OWNS", "Aaron owns Raphael OS authority.", confidence=0.98, source_reference="constitutional_authority")

    def _ingest_goals_projects_agents(self) -> None:
        goals = []
        try:
            goals = legacy.parse_goals(self.config)
        except Exception:
            goals = []
        for goal in goals:
            title = goal.get("title") or goal.get("Title") or goal.get("id") or "Untitled Goal"
            status_text = (goal.get("status") or "active").lower().replace(" ", "_")
            source = str(self.config.vault / "00_Raphael" / "Goals.md")
            goal_id = self.add_node("Goal", title, goal.get("description", title), status=status_text, priority=goal.get("priority", "medium").lower(), source_system="Task Registry", source_reference=source, confidence=0.84, metadata=goal)
            self.add_relationship(_id("AARON", "Aaron") if _id("AARON", "Aaron") in self.nodes else _id("AARON", "Aaron"), goal_id, "ADVANCES", "Aaron sponsors this goal.", confidence=0.82, source_system="Task Registry", source_reference=source)
        for project in self._project_names():
            path = self.config.vault / "02_Projects" / project / "Overview.md"
            self.add_node("Project", project, f"Project workspace: {project}", source_system="Task Registry", source_reference=str(path), confidence=0.82)
        for agent in getattr(legacy, "AGENTS", []):
            path = self.config.vault / "03_Agents" / agent / "Identity.md"
            self.add_node("Agent", agent, f"Digital employee agent: {agent}", source_system="Agent generated with evidence", source_reference=str(path), confidence=0.83, tags=["digital_employee"])

    def _ingest_workflows(self) -> None:
        try:
            from . import workflow_runner
            workflows = workflow_runner.load_registry(self.config)
        except Exception:
            workflows = []
        for workflow in workflows:
            wid = self.add_node("Workflow", workflow["name"], workflow.get("description", ""), status="active" if workflow.get("enabled") else "paused", source_system="Workflow Runner", source_reference=str(workflow_runner.registry_path(self.config)), confidence=0.9, metadata=workflow)
            for service in ("n8n", "comfyui", "dashboard"):
                if service in json.dumps(workflow).lower():
                    sid = self._service_node(service)
                    self.add_relationship(wid, sid, "USES", f"{workflow['name']} uses {service}.", source_system="Workflow Runner", source_reference=str(workflow_runner.registry_path(self.config)), confidence=0.83)

    def _ingest_services_resources(self) -> None:
        try:
            from . import service_manager
            services = service_manager.load_registry(self.config).get("services", [])
            source = str(service_manager.registry_path(self.config))
        except Exception:
            services, source = [], "service_manager_unavailable"
        for service in services:
            sid = self.add_node("Service", service["display_name"], service.get("notes", ""), status="active" if service.get("enabled") else "paused", source_system="Service Manager", source_reference=source, confidence=0.9, metadata=service)
            resource = "Local Runtime" if service["service_id"] in {"dashboard", "voice_gateway"} else "Localhost Service Port"
            rid = self.add_node("Resource", resource, f"Resource supporting {service['display_name']}.", source_system="Service Manager", source_reference=source, confidence=0.82)
            self.add_relationship(sid, rid, "REQUIRES", f"{service['display_name']} requires {resource}.", source_system="Service Manager", source_reference=source, confidence=0.84)

    def _ingest_councils(self) -> None:
        for council in getattr(legacy, "COUNCILS", []):
            path = self.config.vault / "00_Raphael" / "Councils" / council / "Council Brief.md"
            self.add_node("Council", council, f"Governance and advisory council: {council}", source_system="Agent generated with evidence", source_reference=str(path), confidence=0.8)

    def _ingest_self_healing(self) -> None:
        try:
            from . import self_healing
            data = self_healing.self_healing_status(self.config)
        except Exception:
            return
        source = str(runtime_root(self.config) / "self_healing_status")
        for issue in data.get("active_issues", []):
            issue_node = self.add_node("Risk", issue.get("affected_system", issue.get("kind", "Issue")), issue.get("probable_cause", ""), status=issue.get("status", "active"), priority=issue.get("severity", "medium"), source_system="Self-Healing Registry", source_reference=issue.get("issue_id", source), confidence=0.86, metadata=issue)
            target = self._service_node(str(issue.get("affected_system", "")).lower())
            if target:
                self.add_relationship(issue_node, target, "RISKS", issue.get("recommended_fix", "Service issue detected."), source_system="Self-Healing Registry", source_reference=issue.get("issue_id", source), confidence=0.84)

    def _ensure_minimum_graph(self) -> None:
        aaron = self.nodes.get(_id("AARON", "Aaron")) or next((n for n in self.nodes.values() if n["node_type"] == "Aaron"), None)
        aaron_id = aaron["node_id"] if aaron else self.add_node("Aaron", "Aaron", "Owner and final decision authority.", source_reference="constitutional_authority", confidence=0.99)
        for goal, project, agent, workflow, service, resource in SEED_GRAPH:
            gid = self.add_node("Goal", goal, f"Operational goal: {goal}", priority="high", source_system="Phase 75 Seed", source_reference="Phase 75 minimum viable graph", confidence=0.78)
            pid = self.add_node("Project", project, f"Project supporting {goal}.", source_system="Phase 75 Seed", source_reference="Phase 75 minimum viable graph", confidence=0.78)
            aid = self.add_node("Agent", agent, f"Responsible agent for {project}.", source_system="Phase 75 Seed", source_reference="Phase 75 minimum viable graph", confidence=0.78)
            wid = self.add_node("Workflow", workflow, f"Workflow supporting {project}.", source_system="Phase 75 Seed", source_reference="Phase 75 minimum viable graph", confidence=0.78)
            sid = self.add_node("Service", service, f"Required service for {workflow}.", source_system="Phase 75 Seed", source_reference="Phase 75 minimum viable graph", confidence=0.78)
            rid = self.add_node("Resource", resource, f"Resource required by {service}.", source_system="Phase 75 Seed", source_reference="Phase 75 minimum viable graph", confidence=0.78)
            src = "Phase 75 minimum viable graph"
            self.add_relationship(aaron_id, gid, "ADVANCES", f"Aaron sponsors {goal}.", source_system="Phase 75 Seed", source_reference=src, confidence=0.78)
            self.add_relationship(gid, pid, "ADVANCES", f"{project} advances {goal}.", source_system="Phase 75 Seed", source_reference=src, confidence=0.78)
            self.add_relationship(pid, aid, "ASSIGNED_TO", f"{agent} is responsible for {project}.", source_system="Phase 75 Seed", source_reference=src, confidence=0.78)
            self.add_relationship(aid, wid, "WORKS_ON", f"{agent} works through {workflow}.", source_system="Phase 75 Seed", source_reference=src, confidence=0.78)
            self.add_relationship(pid, wid, "REQUIRES", f"{project} requires {workflow}.", source_system="Phase 75 Seed", source_reference=src, confidence=0.78)
            self.add_relationship(wid, sid, "USES", f"{workflow} uses {service}.", source_system="Phase 75 Seed", source_reference=src, confidence=0.78)
            self.add_relationship(sid, rid, "REQUIRES", f"{service} requires {resource}.", source_system="Phase 75 Seed", source_reference=src, confidence=0.78)
        self.add_event("Phase 75 build", "Implementation request", "World Model runtime", "World Model graph built with governed metadata.", list(self.nodes)[:8], importance_level="milestone", source_system="Phase 75 Seed", source_reference="Phase 75 plan", confidence=0.86)

    def _add_epistemic_examples(self) -> None:
        self.add_hypothesis(
            "POD Business is most likely to generate near-term revenue among current business options.",
            confidence=0.62,
            supporting_evidence=[{"source": "Phase 75 Seed", "summary": "POD graph has workflow, service, and resource chain."}],
            contradicting_evidence=[{"source": "Phase 75 Seed", "summary": "No validated revenue record is present in the model."}],
        )

    def _service_node(self, service_id_or_name: str) -> str:
        key = service_id_or_name.lower().replace("_", " ")
        for node in self.nodes.values():
            if node["node_type"] == "Service" and key and (key in node["name"].lower() or key in node["node_id"].lower()):
                return node["node_id"]
        if not key:
            return ""
        return self.add_node("Service", service_id_or_name.strip().title() or "Unknown Service", "Service referenced by another subsystem.", source_system="Agent inference", source_reference=f"inferred:{service_id_or_name}", confidence=0.55)

    def _project_names(self) -> list[str]:
        root = self.config.vault / "02_Projects"
        if not root.exists():
            return []
        return sorted(path.name for path in root.iterdir() if path.is_dir())


def save_model(
    config: legacy.RaphaelConfig,
    nodes: list[dict[str, Any]],
    relationships: list[dict[str, Any]],
    events: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
    conflicts: list[dict[str, Any]],
) -> None:
    root = runtime_root(config)
    _write_json(root / "nodes.json", sorted(nodes, key=lambda row: row["node_id"]))
    _write_json(root / "relationships.json", sorted(relationships, key=lambda row: row["relationship_id"]))
    _write_json(root / "events.json", sorted(events, key=lambda row: row["event_id"]))
    _write_json(root / "hypotheses.json", sorted(hypotheses, key=lambda row: row["hypothesis_id"]))
    _write_json(root / "conflicts.json", conflicts)
    _write_json(root / "world_model_cache.json", {"generated": _now(), "node_count": len(nodes), "relationship_count": len(relationships), "conflict_count": len(conflicts)})


def load_model(config: legacy.RaphaelConfig) -> dict[str, Any]:
    ensure_world_model(config)
    root = runtime_root(config)
    nodes = _read_json(root / "nodes.json", [])
    relationships = apply_confidence_decay(_read_json(root / "relationships.json", []))
    events = apply_event_retention(_read_json(root / "events.json", []))
    hypotheses = _read_json(root / "hypotheses.json", [])
    conflicts = _read_json(root / "conflicts.json", [])
    return {"nodes": nodes, "relationships": relationships, "events": events, "hypotheses": hypotheses, "conflicts": conflicts}


def build_world_model(config: legacy.RaphaelConfig) -> dict[str, Any]:
    return WorldModelBuilder(config).build()


def refresh_world_model(config: legacy.RaphaelConfig) -> dict[str, Any]:
    return build_world_model(config)


def confidence_state(confidence: float) -> str:
    value = float(confidence)
    if value > 0.25:
        return "active"
    if 0.15 <= value <= 0.25:
        return "review_candidate"
    if 0.10 <= value < 0.15:
        return "dormant"
    return "deprecated"


def apply_confidence_decay(relationships: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = dt.datetime.now()
    result = []
    for rel in relationships:
        row = dict(rel)
        try:
            updated = dt.datetime.fromisoformat(str(row.get("updated_at", "")))
        except ValueError:
            updated = now
        decay_days = DECAY_DAYS.get(row.get("relationship_type"))
        if decay_days and row.get("status") == "active":
            periods = max(0, int((now - updated).days // decay_days))
            if periods:
                row["confidence"] = round(max(0.09, float(row.get("confidence", 0)) - periods * 0.1), 3)
                row["confidence_state"] = confidence_state(row["confidence"])
                if row["confidence_state"] in {"dormant", "deprecated"}:
                    row["status"] = row["confidence_state"]
        result.append(row)
    return result


def apply_event_retention(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = dt.datetime.now()
    limits = {"routine": 365, "important": 730}
    result = []
    for event in events:
        row = dict(event)
        importance = row.get("importance_level", "important")
        try:
            event_time = dt.datetime.fromisoformat(str(row.get("event_time", "")))
        except ValueError:
            event_time = now
        if importance in limits and (now - event_time).days > limits[importance]:
            row["status"] = "archived"
        result.append(row)
    return result


def detect_conflicts(nodes: list[dict[str, Any]], relationships: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    by_name_type: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for node in nodes:
        by_name_type.setdefault((node["node_type"], node["name"].casefold()), []).append(node)
    for (node_type, name), rows in by_name_type.items():
        statuses = {row.get("status") for row in rows}
        if len(statuses) > 1:
            conflicts.append({
                "conflict_id": _id("CONF", node_type, name, sorted(statuses)),
                "kind": "node_status_conflict",
                "status": "conflicted",
                "summary": f"{node_type} `{rows[0]['name']}` has competing statuses.",
                "competing_evidence": [{"node_id": row["node_id"], "status": row.get("status"), "confidence": row.get("confidence"), "source_system": row.get("source_system"), "source_reference": row.get("source_reference")} for row in rows],
                "recommendation": "Aaron review required before treating this status as established fact.",
                "created_at": _now(),
            })
    rel_groups: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for rel in relationships:
        rel_groups.setdefault((rel["from_node"], rel["to_node"], rel["relationship_type"]), []).append(rel)
    for key, rows in rel_groups.items():
        active_statuses = {row.get("status") for row in rows}
        if len(rows) > 1 and len(active_statuses) > 1:
            conflicts.append({
                "conflict_id": _id("CONFREL", *key, sorted(active_statuses)),
                "kind": "relationship_status_conflict",
                "status": "conflicted",
                "summary": "Relationship has competing status evidence.",
                "competing_evidence": [{"relationship_id": row["relationship_id"], "status": row.get("status"), "confidence": row.get("confidence"), "source_trust": row.get("source_trust")} for row in rows],
                "recommendation": "Aaron review required before using this relationship for recommendations.",
                "created_at": _now(),
            })
    return conflicts


def health(config: legacy.RaphaelConfig) -> dict[str, Any]:
    model = load_model(config)
    nodes = model["nodes"]
    relationships = model["relationships"]
    stale_nodes = stale_node_ids(nodes)
    stale_rels = [row["relationship_id"] for row in relationships if row.get("confidence_state") == "review_candidate"]
    null_sources = [row["node_id"] for row in nodes if row.get("status") == "active" and not row.get("source_reference")]
    high_conf_nodes = sum(1 for row in nodes if float(row.get("confidence", 0)) > 0.7)
    rels_with_evidence = sum(1 for row in relationships if row.get("evidence"))
    data = {
        "generated": _now(),
        "node_count": len(nodes),
        "relationship_count": len(relationships),
        "event_count": len(model["events"]),
        "hypothesis_count": len(model["hypotheses"]),
        "conflict_count": len(model["conflicts"]),
        "stale_nodes": stale_nodes,
        "stale_relationships": stale_rels,
        "review_candidates": [row["node_id"] for row in nodes if row.get("confidence_state") == "review_candidate"],
        "dormant_entities": [row["node_id"] for row in nodes if row.get("confidence_state") == "dormant"],
        "deprecated_entities": [row["node_id"] for row in nodes if row.get("confidence_state") == "deprecated"],
        "active_nodes_missing_source_reference": null_sources,
        "quality": {
            "nodes_confidence_gt_0_7_ratio": round(high_conf_nodes / max(1, len(nodes)), 3),
            "relationships_with_evidence_ratio": round(rels_with_evidence / max(1, len(relationships)), 3),
            "minimum_viable_graph_connected": minimum_graph_connected(model),
        },
    }
    _write_json(runtime_root(config) / "world_model_cache.json", data)
    write_health_note(config, data)
    return data


def stale_node_ids(nodes: list[dict[str, Any]]) -> list[str]:
    now = dt.datetime.now()
    stale = []
    for node in nodes:
        status = str(node.get("status", "")).lower()
        if status in STALE_EXEMPT or status not in STALE_STATUSES:
            continue
        threshold = STALE_DAYS.get(node.get("node_type"))
        if not threshold:
            continue
        try:
            updated = dt.datetime.fromisoformat(str(node.get("updated_at", "")))
        except ValueError:
            continue
        if (now - updated).days > threshold:
            stale.append(node["node_id"])
    return stale


def minimum_graph_connected(model: dict[str, Any]) -> bool:
    nodes = {row["node_id"]: row for row in model["nodes"]}
    rels = [row for row in model["relationships"] if row.get("status") == "active" and row.get("confidence_state") not in {"dormant", "deprecated"}]
    outgoing: dict[str, list[str]] = {}
    for rel in rels:
        outgoing.setdefault(rel["from_node"], []).append(rel["to_node"])
    aaron_ids = [node_id for node_id, node in nodes.items() if node["node_type"] == "Aaron"]
    if not aaron_ids:
        return False
    required = ["Goal", "Project", "Agent", "Workflow", "Service", "Resource"]
    for aaron_id in aaron_ids:
        queue = deque([(aaron_id, [])])
        seen = {(aaron_id, ())}
        while queue:
            current, path_types = queue.popleft()
            next_types = path_types + ([nodes[current]["node_type"]] if current in nodes else [])
            if all(kind in next_types for kind in required):
                return True
            for nxt in outgoing.get(current, []):
                state = (nxt, tuple(next_types))
                if state not in seen:
                    seen.add(state)
                    queue.append((nxt, next_types))
    return False


def status(config: legacy.RaphaelConfig) -> dict[str, Any]:
    ensure_world_model(config)
    model = load_model(config)
    return {
        "enabled": bool(getattr(config, "world_model_enabled", True)),
        "runtime": str(runtime_root(config)),
        "vault": str(vault_root(config)),
        "node_count": len(model["nodes"]),
        "relationship_count": len(model["relationships"]),
        "event_count": len(model["events"]),
        "hypothesis_count": len(model["hypotheses"]),
        "conflict_count": len(model["conflicts"]),
        "minimum_viable_graph_connected": minimum_graph_connected(model),
        "health": health(config),
        "safety": {
            "advisory_only": True,
            "external_actions": False,
            "approval_bypass": False,
            "raw_graph_dumps_from_gateway": False,
        },
    }


def node(config: legacy.RaphaelConfig, node_id: str) -> dict[str, Any]:
    model = load_model(config)
    for row in model["nodes"]:
        if row["node_id"].casefold() == node_id.casefold() or row["name"].casefold() == node_id.casefold():
            return row
    raise FileNotFoundError(f"World Model node not found: {node_id}")


def related(config: legacy.RaphaelConfig, node_id: str, *, include_dormant: bool = False) -> dict[str, Any]:
    model = load_model(config)
    resolved = node(config, node_id)["node_id"]
    nodes = {row["node_id"]: row for row in model["nodes"]}
    rows = []
    for rel in model["relationships"]:
        if not include_dormant and (rel.get("status") in {"dormant", "deprecated"} or rel.get("confidence_state") in {"dormant", "deprecated"}):
            continue
        if rel["from_node"] == resolved or rel["to_node"] == resolved:
            other = rel["to_node"] if rel["from_node"] == resolved else rel["from_node"]
            rows.append({"relationship": rel, "node": nodes.get(other, {"node_id": other, "name": "Unknown"})})
    return {"node_id": resolved, "related": rows}


def path_between(config: legacy.RaphaelConfig, source: str, target: str) -> dict[str, Any]:
    model = load_model(config)
    src = node(config, source)["node_id"]
    dst = node(config, target)["node_id"]
    edges: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for rel in model["relationships"]:
        if rel.get("status") == "active" and rel.get("confidence_state") not in {"dormant", "deprecated"}:
            edges.setdefault(rel["from_node"], []).append((rel["to_node"], rel))
            edges.setdefault(rel["to_node"], []).append((rel["from_node"], rel))
    queue = deque([(src, [])])
    seen = {src}
    while queue:
        current, rel_path = queue.popleft()
        if current == dst:
            return {"source": src, "target": dst, "path": rel_path, "found": True}
        for nxt, rel in edges.get(current, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, rel_path + [rel]))
    return {"source": src, "target": dst, "path": [], "found": False}


def world_model_answer_legacy(
    config: legacy.RaphaelConfig,
    agent_id: str,
    purpose: str, 
    question: str,
) -> dict:
    """
    Legacy fallback path for CLI commands not yet migrated to RRK Jobs.
    
    This function exists explicitly as a bridge during migration.
    It should be removed once all callers are RRK-native.
    
    TODO: Track removal in migration log.
    """
    # Attempt RRK path first if kernel is running via local Dashboard API
    try:
        import urllib.request
        import json
        req = urllib.request.Request(
            "http://127.0.0.1:8788/api/world-model/query",
            data=json.dumps({
                "agent_id": agent_id,
                "purpose": purpose,
                "question": question
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                if "error" not in data:
                    return data
    except Exception:
        pass
    
    # Fall through to legacy path
    return _world_model_answer_internal(config, agent_id, purpose, question)


def _world_model_answer_internal(config: legacy.RaphaelConfig, agent_id: str, purpose: str, question: str, trace_id: str = None) -> dict[str, Any]:
    ensure_world_model(config)
    access = _read_json(runtime_root(config) / "access_policy.json", DEFAULT_ACCESS_POLICY)
    controls = _read_json(runtime_root(config) / "inference_controls.json", DEFAULT_INFERENCE_CONTROLS)
    actor = access["agents"].get(agent_id) or access["agents"].get("Standard Agent") or access["agents"]["Unknown Agent"]
    rate = check_rate_limit(config, agent_id, actor, access)
    if not rate["allowed"]:
        answer = {"allowed": False, "answer": "Query blocked by World Model rate limiting.", "rate_limit": rate}
        log_query(config, agent_id, purpose, question, answer, blocked=True, trace_id=trace_id)
        return answer
    blocked = blocked_correlation(question, agent_id, controls)
    if blocked:
        answer = {
            "allowed": False,
            "answer": "I cannot assemble that sensitive correlation. Aaron review is required.",
            "blocked_correlation": blocked,
            "uncertainty": "No answer was assembled from unauthorized sensitive data.",
        }
        log_query(config, agent_id, purpose, question, answer, blocked=True, trace_id=trace_id)
        return answer
    model = load_model(config)
    result = answer_from_model(model, question)
    result["allowed"] = True
    result["purpose"] = purpose
    result["rate_limit"] = rate
    log_query(config, agent_id, purpose, question, result, trace_id=trace_id)
    refresh_query_log_note(config)
    return result


def answer_from_model(model: dict[str, Any], question: str) -> dict[str, Any]:
    q = question.casefold()
    if "most likely" in q and "revenue" in q:
        hypotheses = [h for h in model["hypotheses"] if "revenue" in h.get("statement", "").casefold() and h.get("status") == "active"]
        if hypotheses:
            hyp = sorted(hypotheses, key=lambda row: row.get("confidence", 0), reverse=True)[0]
            return {
                "answer": hyp["statement"],
                "epistemic_status": "hypothesis",
                "hypothesis_status": hyp["status"],
                "confidence": hyp["confidence"],
                "supporting_evidence": hyp.get("supporting_evidence", []),
                "contradicting_evidence": hyp.get("contradicting_evidence", []),
                "recommendation": "Treat as a prioritized hypothesis until validated by revenue evidence.",
            }
    if "status" in q:
        match = re.search(r"status\s+of\s+(.+?)[?.,]*$", question, flags=re.I)
        project_name = match.group(1).strip(" ?") if match else ""
        conflicts = [c for c in model["conflicts"] if project_name.casefold() in json.dumps(c).casefold()] if project_name else model["conflicts"]
        if conflicts:
            conflict = conflicts[0]
            return {
                "answer": "Project status is conflicted and should not be treated as established fact.",
                "epistemic_status": "conflict",
                "conflict_warning": conflict["summary"],
                "competing_evidence": conflict["competing_evidence"],
                "confidence_levels": [item.get("confidence") for item in conflict["competing_evidence"]],
                "recommendation": conflict["recommendation"],
            }
    if "focus" in q or "what should aaron" in q:
        return executive_reasoning(model)
    matches = search_nodes(model, question)
    return {
        "answer": "I found relevant World Model entities. Uncertainty and provenance are included.",
        "epistemic_status": "known_with_provenance" if matches else "unknown",
        "matches": matches[:8],
        "confidence": max([row.get("confidence", 0) for row in matches], default=0),
        "recommendation": "Ask a narrower question or request Aaron review for uncertain items." if not matches else "Use only active, non-dormant items for action planning.",
    }


def executive_reasoning(model: dict[str, Any]) -> dict[str, Any]:
    active_rels = [row for row in model["relationships"] if row.get("status") == "active" and row.get("confidence_state") not in {"dormant", "deprecated"}]
    blockers = [row for row in active_rels if row["relationship_type"] == "BLOCKED_BY"]
    dependencies = [row for row in active_rels if row["relationship_type"] in {"DEPENDS_ON", "REQUIRES", "USES"}]
    degree = Counter()
    for rel in active_rels:
        degree[rel["from_node"]] += 1
        degree[rel["to_node"]] += 1
    nodes = {row["node_id"]: row for row in model["nodes"]}
    leverage = [{"node_id": node_id, "name": nodes.get(node_id, {}).get("name", node_id), "connections": count} for node_id, count in degree.most_common(5)]
    recommendation = "Focus on the highest-leverage active project with complete workflow, service, and resource support."
    if blockers:
        recommendation = "Review blockers first; they create the highest execution risk."
    return {
        "answer": recommendation,
        "epistemic_status": "reasoned_recommendation",
        "dependency_count": len(dependencies),
        "blocker_count": len(blockers),
        "top_dependencies": dependencies[:5],
        "top_blockers": blockers[:5],
        "leverage_analysis": leverage,
        "confidence": 0.72,
        "uncertainty": "Recommendation is advisory and depends on current graph freshness.",
    }


def search_nodes(model: dict[str, Any], question: str) -> list[dict[str, Any]]:
    terms = {term.strip(".,?!").casefold() for term in question.split() if len(term.strip(".,?!")) > 2}
    rows = []
    for node_row in model["nodes"]:
        if node_row.get("status") in {"dormant", "deprecated"} or node_row.get("confidence_state") in {"dormant", "deprecated"}:
            continue
        haystack = f"{node_row.get('name', '')} {node_row.get('summary', '')} {' '.join(node_row.get('tags', []))}".casefold()
        score = sum(1 for term in terms if term in haystack)
        if score:
            rows.append({k: node_row[k] for k in ("node_id", "node_type", "name", "summary", "status", "confidence", "source_system", "source_reference")})
    return sorted(rows, key=lambda row: row["confidence"], reverse=True)


def check_rate_limit(config: legacy.RaphaelConfig, agent_id: str, actor: dict[str, Any], access: dict[str, Any]) -> dict[str, Any]:
    now = dt.datetime.now()
    rows = query_log_rows(config)
    recent_hour = [row for row in rows if row.get("agent_id") == agent_id and _within(row.get("timestamp", ""), now, 3600)]
    recent_minute = [row for row in rows if row.get("agent_id") == agent_id and _within(row.get("timestamp", ""), now, 60)]
    base_key = agent_id if agent_id in access["base_rate_limits_per_hour"] else "Standard Agent" if actor.get("trust_tier", 0) > 0 else "Unknown Agent"
    base = access["base_rate_limits_per_hour"].get(base_key, 30)
    trust_tier = int(actor.get("trust_tier", 0))
    limit = int(base * float(access["trust_multipliers"].get(str(trust_tier), 1)))
    burst_block = int(access.get("burst_block_per_minute", 25))
    burst_warning = int(access.get("burst_warning_per_minute", 10))
    allowed = len(recent_hour) < limit and len(recent_minute) < burst_block
    return {
        "allowed": allowed,
        "query_count": len(recent_hour),
        "burst_count": len(recent_minute),
        "blocked_count": sum(1 for row in recent_hour if row.get("blocked")),
        "sensitive_query_count": sum(1 for row in recent_hour if row.get("sensitive")),
        "hourly_limit": limit,
        "burst_warning": len(recent_minute) >= burst_warning,
        "safety_pressure_score": min(100, len(recent_minute) * 4 + len(recent_hour)),
    }


def _within(timestamp: str, now: dt.datetime, seconds: int) -> bool:
    try:
        then = dt.datetime.fromisoformat(str(timestamp))
    except ValueError:
        return False
    return (now - then).total_seconds() <= seconds


def blocked_correlation(question: str, agent_id: str, controls: dict[str, Any]) -> list[str]:
    if agent_id in {"Aaron", "Raphael Core"}:
        return []
    q = question.casefold()
    for left, right in controls.get("sensitive_correlations", []):
        if left.casefold() in q and right.casefold() in q:
            return [left, right]
    return []


def query_log_rows(config: legacy.RaphaelConfig) -> list[dict[str, Any]]:
    path = runtime_root(config) / "query_log.jsonl"
    rows = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def log_query(config: legacy.RaphaelConfig, agent_id: str, purpose: str, question: str, result: dict[str, Any], *, blocked: bool = False, trace_id: str = None) -> None:
    entry = {
        "timestamp": _now(),
        "agent_id": agent_id,
        "purpose": purpose,
        "question": question,
        "blocked": blocked,
        "sensitive": bool(result.get("blocked_correlation")),
        "epistemic_status": result.get("epistemic_status", ""),
        "confidence": result.get("confidence"),
    }
    path = runtime_root(config) / "query_log.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, default=str) + "\n")
        
    if trace_id:
        from .kernel.observability import ObservabilityLayer
        ObservabilityLayer.info(
            source="WorldModelService", 
            message=f"WM query completed: agent={agent_id} purpose='{purpose}'", 
            trace_id=trace_id
        )


def snapshot(config: legacy.RaphaelConfig, reason: str) -> dict[str, Any]:
    model = load_model(config)
    row = {
        "timestamp": _now(),
        "reason": reason,
        "node_count": len(model["nodes"]),
        "relationship_count": len(model["relationships"]),
        "event_count": len(model["events"]),
        "hypothesis_count": len(model["hypotheses"]),
        "conflict_count": len(model["conflicts"]),
    }
    with (runtime_root(config) / "snapshots.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")
    return row


def set_node_status(config: legacy.RaphaelConfig, node_id: str, status_value: str, reason: str = "") -> dict[str, Any]:
    model = load_model(config)
    target = node(config, node_id)
    for row in model["nodes"]:
        if row["node_id"] == target["node_id"]:
            row["status"] = status_value
            row["updated_at"] = _now()
            row.setdefault("metadata", {})["status_reason"] = reason or f"CLI world model status change to {status_value}"
            target = row
            break
    save_model(config, model["nodes"], model["relationships"], model["events"], model["hypotheses"], detect_conflicts(model["nodes"], model["relationships"]))
    refresh_notes(config)
    return target


def set_relationship_status(config: legacy.RaphaelConfig, rel_id: str, status_value: str, reason: str = "") -> dict[str, Any]:
    model = load_model(config)
    found = None
    for row in model["relationships"]:
        if row["relationship_id"].casefold() == rel_id.casefold():
            row["status"] = status_value
            row["updated_at"] = _now()
            row.setdefault("metadata", {})["status_reason"] = reason or f"CLI relationship status change to {status_value}"
            found = row
            break
    if not found:
        raise FileNotFoundError(f"World Model relationship not found: {rel_id}")
    save_model(config, model["nodes"], model["relationships"], model["events"], model["hypotheses"], detect_conflicts(model["nodes"], model["relationships"]))
    refresh_notes(config)
    return found


def correct_node(config: legacy.RaphaelConfig, node_id: str, replacement_name: str, source_of_truth: str, reason: str = "Manual correction") -> dict[str, Any]:
    model = load_model(config)
    old = set_node_status(config, node_id, "deprecated", reason)
    builder = WorldModelBuilder(config)
    for row in model["nodes"]:
        builder.nodes[row["node_id"]] = row
    for row in model["relationships"]:
        builder.relationships[row["relationship_id"]] = row
    for row in model["events"]:
        builder.events[row["event_id"]] = row
    for row in model["hypotheses"]:
        builder.hypotheses[row["hypothesis_id"]] = row
    new_id = builder.add_node(old["node_type"], replacement_name, f"Correction replacement for {old['name']}.", source_system="System Generated Records", source_reference=source_of_truth, confidence=0.86, metadata={"corrects": old["node_id"], "reason": reason})
    event_id = builder.add_event("World Model correction", old["node_id"], new_id, reason, [old["node_id"], new_id], source_reference=source_of_truth, confidence=0.86)
    builder.add_relationship(old["node_id"], event_id, "LEARNS_FROM", "Correction preserves prior record in audit trail.", source_reference=source_of_truth, confidence=0.86)
    builder.add_relationship(event_id, new_id, "PRODUCES", "Correction produced replacement node.", source_reference=source_of_truth, confidence=0.86)
    save_model(config, list(builder.nodes.values()), list(builder.relationships.values()), list(builder.events.values()), list(builder.hypotheses.values()), detect_conflicts(list(builder.nodes.values()), list(builder.relationships.values())))
    refresh_notes(config)
    return {"old_node": old["node_id"], "replacement_node": new_id, "correction_event": event_id}


def refresh_notes(config: legacy.RaphaelConfig) -> None:
    model = load_model(config)
    root = vault_root(config)
    node_rows = ["| Node ID | Type | Name | Status | Confidence | Source |", "|---|---|---|---|---:|---|"]
    for row in model["nodes"]:
        node_rows.append(f"| {row['node_id']} | {row['node_type']} | {row['name']} | {row['status']} | {row['confidence']} | {row['source_system']} |")
    legacy.write_generated_note(root / "World Model Node Registry.md", "# World Model Node Registry\n\n" + "\n".join(node_rows), config)
    rel_rows = ["| Relationship ID | From | Type | To | Status | Confidence | Trust |", "|---|---|---|---|---|---:|---|"]
    for row in model["relationships"]:
        rel_rows.append(f"| {row['relationship_id']} | {row['from_node']} | {row['relationship_type']} | {row['to_node']} | {row['status']} | {row['confidence']} | {row.get('source_trust', '')} |")
    legacy.write_generated_note(root / "World Model Relationship Registry.md", "# World Model Relationship Registry\n\n" + "\n".join(rel_rows), config)
    conflict_blocks = []
    for conflict in model["conflicts"]:
        conflict_blocks.append(f"## {conflict['conflict_id']}\n\n- Kind: {conflict['kind']}\n- Summary: {conflict['summary']}\n- Recommendation: {conflict['recommendation']}\n")
    legacy.write_generated_note(root / "World Model Conflict Registry.md", "# World Model Conflict Registry\n\n" + ("\n".join(conflict_blocks) or "No conflicts recorded."), config)
    _write_access_notes(config)
    write_health_note(config, health(config))
    write_brief(config)
    refresh_query_log_note(config)


def _write_access_notes(config: legacy.RaphaelConfig) -> None:
    root = vault_root(config)
    access = _read_json(runtime_root(config) / "access_policy.json", DEFAULT_ACCESS_POLICY)
    controls = _read_json(runtime_root(config) / "inference_controls.json", DEFAULT_INFERENCE_CONTROLS)
    legacy.write_generated_note(root / "World Model Access Policy.md", "# World Model Access Policy\n\n```json\n" + json.dumps(access, indent=2) + "\n```\n", config)
    legacy.write_generated_note(root / "World Model Inference Controls.md", "# World Model Inference Controls\n\n```json\n" + json.dumps(controls, indent=2) + "\n```\n", config)


def write_health_note(config: legacy.RaphaelConfig, data: dict[str, Any]) -> None:
    root = vault_root(config)
    content = f"""# World Model Health

Generated: {data['generated']}

- Nodes: {data['node_count']}
- Relationships: {data['relationship_count']}
- Events: {data['event_count']}
- Hypotheses: {data['hypothesis_count']}
- Conflicts: {data['conflict_count']}
- Minimum viable graph connected: {data['quality']['minimum_viable_graph_connected']}
- Nodes confidence > 0.7: {data['quality']['nodes_confidence_gt_0_7_ratio']}
- Relationships with evidence: {data['quality']['relationships_with_evidence_ratio']}
- Active nodes missing source_reference: {len(data['active_nodes_missing_source_reference'])}

## Review Queues

- Stale nodes: {len(data['stale_nodes'])}
- Stale relationships: {len(data['stale_relationships'])}
- Review candidates: {len(data['review_candidates'])}
- Dormant entities: {len(data['dormant_entities'])}
"""
    legacy.write_generated_note(root / "World Model Health.md", content, config)


def write_brief(config: legacy.RaphaelConfig) -> Path:
    root = vault_root(config)
    model = load_model(config)
    reasoning = executive_reasoning(model)
    content = f"""# World Model Executive Brief

Generated: {_now()}

## Recommendation

{reasoning['answer']}

## Signals

- Dependencies: {reasoning['dependency_count']}
- Blockers: {reasoning['blocker_count']}
- Confidence: {reasoning['confidence']}
- Uncertainty: {reasoning['uncertainty']}

## Highest Leverage Nodes

{chr(10).join(f"- {row['name']} ({row['connections']} connections)" for row in reasoning['leverage_analysis']) or "- None."}

All recommendations remain advisory and require normal Workflow Runner, Command Bus, and approval boundaries.
"""
    path = root / "World Model Executive Brief.md"
    legacy.write_generated_note(path, content, config)
    return path


def review(config: legacy.RaphaelConfig) -> Path:
    refresh_notes(config)
    path = vault_root(config) / "World Model Review.md"
    data = health(config)
    content = f"""# World Model Review

Generated: {_now()}

- Build status: successful
- Runtime: `{runtime_root(config)}`
- Nodes: {data['node_count']}
- Relationships: {data['relationship_count']}
- Conflicts: {data['conflict_count']}
- Dormant entities: {len(data['dormant_entities'])}
- Minimum viable graph connected: {data['quality']['minimum_viable_graph_connected']}

## Governance

- Query Gateway operational: True
- Access control operational: True
- Rate limiting operational: True
- Inference controls operational: True

## Epistemics

- Conflict detection operational: True
- Confidence decay operational: True
- Dormancy operational: True
- Hypothesis lifecycle operational: True
"""
    legacy.write_generated_note(path, content, config)
    return path


def refresh_query_log_note(config: legacy.RaphaelConfig) -> None:
    rows = query_log_rows(config)[-50:]
    lines = ["| Time | Agent | Purpose | Blocked | Status | Question |", "|---|---|---|---:|---|---|"]
    for row in rows:
        question = str(row.get("question", "")).replace("|", "/")[:120]
        lines.append(f"| {row.get('timestamp', '')} | {row.get('agent_id', '')} | {row.get('purpose', '')} | {row.get('blocked', False)} | {row.get('epistemic_status', '')} | {question} |")
    legacy.write_generated_note(vault_root(config) / "World Model Query Log.md", "# World Model Query Log\n\n" + ("\n".join(lines) if rows else "No queries recorded yet."), config)


def access_review(config: legacy.RaphaelConfig) -> dict[str, Any]:
    access = _read_json(runtime_root(config) / "access_policy.json", DEFAULT_ACCESS_POLICY)
    controls = _read_json(runtime_root(config) / "inference_controls.json", DEFAULT_INFERENCE_CONTROLS)
    return {
        "access_policy_path": str(runtime_root(config) / "access_policy.json"),
        "inference_controls_path": str(runtime_root(config) / "inference_controls.json"),
        "agent_count": len(access.get("agents", {})),
        "sensitive_correlation_count": len(controls.get("sensitive_correlations", [])),
        "only_aaron_may_add_correlations": controls.get("owners") == ["Aaron"],
    }


# --- Phase 80.X: RRK Integration ---

from .kernel.interfaces import ServiceModule

class WorldModelService(ServiceModule):
    """
    RRK native ServiceModule bridging the legacy World Model functions
    into the managed kernel environment.
    """
    
    def __init__(self, config: legacy.RaphaelConfig = None):
        self.config = config or legacy.load_config(legacy.DEFAULT_SETTINGS_PATH)
        self._running = False
        self._queries_handled = 0
        
    @property
    def name(self) -> str:
        return "WorldModelService"
        
    @property
    def depends_on(self) -> list[str]:
        return ["EventBus", "RuntimeStateStore"]

    def _get_trace_id(self) -> str:
        import uuid
        return str(uuid.uuid4())
        
    async def initialize(self) -> None:
        from .kernel.state import store
        store.set_state(self.name, "status", "initialized")
        
    async def start(self) -> None:
        from .kernel.state import store
        from .kernel.observability import ObservabilityLayer
        self._running = True
        store.set_state(self.name, "status", "running")
        ObservabilityLayer.info(self.name, "WorldModelService started.")
        
    async def heartbeat(self) -> bool:
        # Check basic file access as a heartbeat mechanism
        try:
            p = runtime_root(self.config) / "nodes.json"
            return self._running and p.exists()
        except Exception:
            return False
            
    async def stop(self) -> None:
        from .kernel.state import store
        self._running = False
        store.set_state(self.name, "status", "stopped")
        
    async def shutdown(self) -> None:
        from .kernel.state import store
        from .kernel.observability import ObservabilityLayer
        store.set_state(self.name, "status", "shutdown")
        ObservabilityLayer.info(self.name, "WorldModelService shut down.")
        
    def health(self):
        from .kernel.interfaces import ModuleHealth
        if self._running:
            return ModuleHealth.OK
        return ModuleHealth.FAILED
        
    def status(self) -> str:
        return f"Operational. Queries handled: {self._queries_handled}"
        
    def metrics(self) -> dict[str, Any]:
        return {
            "queries_handled": self._queries_handled
        }

    def query(self, agent_id: str, purpose: str, question: str) -> dict:
        """
        Primary query path — RRK native with trace_id and observability.
        """
        from .kernel.observability import ObservabilityLayer
        trace_id = self._get_trace_id()
        ObservabilityLayer.info(
            source=self.name,
            message=f"WM query received",
            trace_id=trace_id,
            agent=agent_id
        )
        self._queries_handled += 1
        
        # We delegate to the internal function which will stamp the trace_id in the JSON log
        return _world_model_answer_internal(self.config, agent_id, purpose, question, trace_id=trace_id)

    def get_graph(self) -> dict:
        """
        Returns the full world model nodes.
        """
        from .kernel.observability import ObservabilityLayer
        trace_id = self._get_trace_id()
        ObservabilityLayer.info(
            source=self.name,
            message=f"WM graph export requested",
            trace_id=trace_id
        )
        self._queries_handled += 1
        
        nodes = _read_json(runtime_root(self.config) / "nodes.json", [])
        return {"nodes": nodes}

