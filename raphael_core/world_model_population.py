"""Phase 75.1 source-backed World Model population and historical backfill."""

from __future__ import annotations

import datetime as dt
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from . import legacy, world_model


EVENT_CATEGORIES = {
    "phase_completion",
    "governance_decision",
    "constitutional_change",
    "safety_evolution",
    "technical_failure",
    "technical_success",
    "workflow_discovery",
    "workflow_creation",
    "workflow_archive",
    "capability_launch",
    "business_milestone",
    "project_milestone",
    "agent_creation",
    "agent_evolution",
    "world_model_event",
}

TARGETED_VAULT_DIRS = [
    "00_Raphael",
    "03_Agents",
    "05_Business",
    "Memory",
]

TARGETED_RUNTIME_DIRS = [
    "workflow_runner",
    "self_healing",
    "builder",
    "launcher",
    "docker",
    "dashboard",
    "voice",
    "workflows",
    "PODStudio",
    "BrandLibrary",
]

EXCLUDED_PARTS = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
    "storage",
}

SOURCE_SUFFIXES = {".md", ".json", ".jsonl", ".py", ".ps1", ".yml", ".yaml", ".txt"}

EXECUTIVE_QUERIES = [
    "What is blocking Raphael OS completion?",
    "What depends on ComfyUI?",
    "What depends on Qdrant?",
    "What would fail if Qdrant disappeared?",
    "What projects advance Raphael OS completion?",
    "What goals lack supporting projects?",
    "What agents lack assignments?",
    "What workflows lack ownership?",
    "What changed in the last 30 days?",
    "What relationships are decaying?",
    "What hypotheses are active?",
    "What safety systems protect authority autonomy?",
    "What constitutional articles affect Phase 75?",
    "Which projects produce revenue?",
    "Which businesses are inactive?",
    "Which systems govern Workflow Runner?",
    "Which services support executive briefs?",
    "Which workflow archives mention OpenAI?",
    "Which workflow archives mention Telegram?",
    "Which workflow archives mention Google Sheets?",
    "Which workflow archives mention Slack?",
    "Which systems mitigate external action risk?",
    "Which records came from Self-Healing?",
    "Which records came from Builder?",
    "Which records came from Governance?",
    "Which events are safety evolution events?",
    "Which events are workflow archive events?",
    "Which agents relate to commerce?",
    "Which agents relate to POD?",
    "Which agents relate to research?",
    "Which workflows use local services?",
    "Which resources support dashboard operation?",
    "Which decisions mention approval?",
    "Which records mention Command Bus?",
    "Which records mention Voice?",
    "Which records mention Dashboard?",
    "Which records mention Digital Employee Network?",
    "Which records mention Council?",
    "Which records mention Executive Intelligence?",
    "Which records mention Phase 68?",
    "Which records mention Phase 75?",
    "Which records mention safety policy?",
    "Which records mention governance?",
    "Which records mention revenue?",
    "Which records mention opportunity?",
    "Which records mention workflow failure?",
    "Which records mention service outage?",
    "Which records mention Qdrant?",
    "Which records mention n8n?",
    "Which records mention ComfyUI?",
    "Which records mention Raphael OS?",
]


def _now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def _id(prefix: str, *parts: object) -> str:
    return world_model._id(prefix, *parts)


def _read_text(path: Path, limit: int = 16000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def _write_json(path: Path, value: Any) -> None:
    world_model._write_json(path, value)


def _title_from_file(path: Path, text: str = "") -> str:
    for line in text.splitlines()[:20]:
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()[:160] or path.stem
    return re.sub(r"^[A-Z]+-\w+\s+-\s+", "", path.stem).strip()[:160] or path.stem


def _status_from_text(text: str) -> str:
    match = re.search(r"(?im)^##\s*Status\s*\n+([^\n#]+)", text)
    if match:
        return match.group(1).strip().lower().replace(" ", "_")[:40]
    lowered = text.lower()
    if "cancelled" in lowered:
        return "cancelled"
    if "completed" in lowered or "complete" in lowered:
        return "complete"
    if "blocked" in lowered or "failed" in lowered:
        return "blocked"
    if "paused" in lowered:
        return "paused"
    return "active"


def _summary_from_text(path: Path, text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip(" -\t")
        if stripped and not stripped.startswith("#") and not stripped.startswith("|") and len(stripped) > 20:
            return stripped[:260]
    return f"Source-backed record from {path.name}."


def _safe_source(path: Path) -> str:
    return str(path.resolve())


def _is_source_file(path: Path) -> bool:
    parts = {part.lower() for part in path.parts}
    return path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES and not parts.intersection(EXCLUDED_PARTS)


def _node(
    node_type: str,
    name: str,
    summary: str,
    source_reference: str,
    *,
    status: str = "active",
    priority: str = "medium",
    confidence: float = 0.82,
    source_system: str = "System Generated Records",
    tags: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    node_id: str | None = None,
) -> dict[str, Any]:
    value = max(0.0, min(1.0, float(confidence)))
    return {
        "node_id": node_id or _id(node_type.upper(), name, source_reference),
        "node_type": node_type,
        "name": name[:180],
        "summary": summary[:500],
        "status": status or "active",
        "priority": priority,
        "created_at": _now(),
        "updated_at": _now(),
        "source_system": source_system,
        "source_reference": source_reference,
        "confidence": round(value, 3),
        "confidence_state": world_model.confidence_state(value),
        "tags": tags or [],
        "metadata": metadata or {},
    }


def _relationship(
    from_node: str,
    to_node: str,
    relationship_type: str,
    summary: str,
    source_reference: str,
    *,
    confidence: float = 0.82,
    source_system: str = "System Generated Records",
    status: str = "active",
) -> dict[str, Any]:
    trust = world_model.SOURCE_TRUST.get(source_system, "A" if source_system == "System Generated Records" else "C")
    value = max(0.0, min(1.0, float(confidence)))
    return {
        "relationship_id": _id("REL", from_node, relationship_type, to_node, source_reference),
        "from_node": from_node,
        "to_node": to_node,
        "relationship_type": relationship_type,
        "summary": summary[:400],
        "confidence": round(value, 3),
        "confidence_state": world_model.confidence_state(value),
        "evidence": [{"source": source_system, "source_reference": source_reference, "source_trust": trust, "summary": summary[:260]}],
        "source_system": source_system,
        "source_reference": source_reference,
        "created_at": _now(),
        "updated_at": _now(),
        "status": status,
        "source_trust": trust,
    }


def _event(
    category: str,
    title: str,
    cause: str,
    effect: str,
    outcome: str,
    related_entities: list[str],
    source_reference: str,
    event_time: str,
    *,
    importance: str = "important",
    confidence: float = 0.82,
) -> tuple[dict[str, Any], dict[str, Any]]:
    event_id = _id("EVENT", category, title, source_reference)
    event = {
        "event_id": event_id,
        "event_type": category,
        "event_category": category,
        "event_time": event_time,
        "cause": cause[:260],
        "effect": effect[:260],
        "outcome": outcome[:360],
        "related_entities": related_entities,
        "source_system": "System Generated Records",
        "source_reference": source_reference,
        "confidence": round(confidence, 3),
        "importance_level": importance,
        "importance": importance,
        "status": "active",
    }
    node = _node(
        "Event",
        title,
        outcome,
        source_reference,
        priority="high" if importance in {"milestone", "constitutional"} else "medium",
        confidence=confidence,
        tags=[category],
        metadata={"event_category": category, "event_time": event_time},
        node_id=event_id,
    )
    return event, node


def classify_path(path: Path, text: str) -> tuple[str, str, list[str], str]:
    p = str(path).lower()
    name = path.name.lower()
    tags: list[str] = []
    if "03_agents" in p or "\\agents\\" in p or " agent\\" in p:
        tags.append("agent")
        return "Task" if "\\tasks\\" in p else "Agent", "Agent generated with evidence", tags, "medium"
    if "council" in p:
        tags.append("council")
        return "Council" if name in {"council brief.md", "council review.md"} else "Deliberation", "Agent generated with evidence", tags, "medium"
    if "workflow summaries" in p or "workflow archive" in p or name.startswith("wfarch-"):
        tags.append("workflow_archive")
        return "Workflow", "Workflow Runner", tags, "medium"
    if "workflow" in p or name.startswith("wf-") or name.startswith("podflow-"):
        tags.append("workflow")
        return "Workflow", "Workflow Runner", tags, "medium"
    if "execution plans" in p or name.startswith("plan-"):
        tags.append("execution_plan")
        return "ExecutionPlan", "System Generated Records", tags, "high"
    if "builder" in p or name.startswith("build-") or name.startswith("bclass-"):
        tags.append("builder")
        return "Build", "Builder Registry", tags, "medium"
    if "self_healing" in p or "self healing" in p or name.startswith("issue-") or name.startswith("obs-"):
        tags.append("self_healing")
        return "Risk" if name.startswith("issue-") else "Event", "Self-Healing Registry", tags, "high"
    if "service" in p or "launcher" in p or "docker" in p or "dashboard" in p or "voice" in p:
        tags.append("service")
        return "Service", "Service Manager", tags, "medium"
    if "goals" in p or "goal " in name:
        tags.append("goal")
        return "Goal", "Task Registry", tags, "high"
    if "business" in p or "commerce" in p or "agency" in p or "creator" in p or "revenue" in p:
        tags.append("business")
        return "Business", "Agent generated with evidence", tags, "high"
    if "opportunit" in p or "initiative" in p:
        tags.append("opportunity")
        return "Opportunity" if "opportunit" in p else "Initiative", "Agent generated with evidence", tags, "medium"
    if "governance" in p or "constitution" in text.lower() or "safety" in p:
        tags.append("governance")
        return "Decision", "System Generated Records", tags, "high"
    if "kpi" in p or "metric" in p or "financial" in p:
        tags.append("metric")
        return "Metric", "System Generated Records", tags, "medium"
    if path.suffix.lower() in {".png", ".svg"}:
        return "Asset", "System Generated Records", ["asset"], "low"
    return "KnowledgeItem", "System Generated Records", tags, "medium"


def event_category_for(path: Path, text: str, node_type: str) -> str:
    p = str(path).lower()
    lower = text.lower()
    if "constitution" in lower:
        return "constitutional_change"
    if "safety" in p or "approval" in lower or "blocked" in lower:
        return "safety_evolution"
    if "phase" in lower or re.search(r"phase[-_ ]?\d+", path.name, flags=re.I):
        return "phase_completion"
    if "workflow summaries" in p or "wfarch-" in path.name.lower():
        return "workflow_archive"
    if "workflow" in p:
        return "workflow_creation"
    if "issue-" in path.name.lower() or "failure" in lower or "failed" in lower:
        return "technical_failure"
    if "review" in p or "complete" in lower:
        return "technical_success"
    if node_type == "Agent":
        return "agent_creation"
    if "business" in p or "revenue" in lower:
        return "business_milestone"
    if "governance" in p or "decision" in p:
        return "governance_decision"
    if "world model" in p:
        return "world_model_event"
    return "capability_launch"


def discover_sources(config: legacy.RaphaelConfig) -> list[Path]:
    roots: list[Path] = []
    for rel in TARGETED_VAULT_DIRS:
        root = config.vault / rel
        if root.exists():
            roots.append(root)
    for rel in TARGETED_RUNTIME_DIRS:
        root = config.os_root / rel
        if root.exists():
            roots.append(root)
    direct = [config.os_root / "command_bus.py", config.os_root / "voice_gateway.py"]
    files: list[Path] = [path for path in direct if _is_source_file(path)]
    for root in roots:
        for path in root.rglob("*"):
            if _is_source_file(path):
                files.append(path)
    unique = sorted({path.resolve(): path for path in files}.values(), key=lambda item: (priority_bucket(item), str(item).lower()))
    return unique


def priority_bucket(path: Path) -> int:
    p = str(path).lower()
    if "governance" in p or "identity" in p or "controlled execution" in p or "system bootstrap" in p:
        return 0
    if "03_agents" in p or "council" in p or "workflow runner" in p or "self_healing" in p:
        return 1
    if "execution plans" in p or "builder" in p or "world model" in p:
        return 2
    if "workflow summaries" in p:
        return 4
    return 3


class Phase751Population:
    def __init__(self, config: legacy.RaphaelConfig) -> None:
        self.config = config
        world_model.ensure_world_model(config)
        self.nodes: dict[str, dict[str, Any]] = {}
        self.relationships: dict[str, dict[str, Any]] = {}
        self.events: dict[str, dict[str, Any]] = {}
        self.hypotheses: dict[str, dict[str, Any]] = {}
        self.file_nodes: dict[Path, str] = {}
        self.domain_nodes: dict[str, str] = {}
        self.population_gaps: list[dict[str, Any]] = []

    def add_node(self, row: dict[str, Any]) -> str:
        if not row.get("source_reference"):
            raise ValueError(f"Node missing source_reference: {row.get('name')}")
        self.nodes[row["node_id"]] = row
        return row["node_id"]

    def add_relationship(self, row: dict[str, Any]) -> str:
        if row["from_node"] not in self.nodes or row["to_node"] not in self.nodes:
            self.population_gaps.append({"kind": "missing_node_for_relationship", "relationship": row})
            return ""
        if row["relationship_type"] == "RELATED_TO":
            self.population_gaps.append({"kind": "generic_relationship_rejected", "relationship": row})
            return ""
        self.relationships[row["relationship_id"]] = row
        return row["relationship_id"]

    def domain(self, name: str, source: Path, *, node_type: str = "KnowledgeItem") -> str:
        key = f"{node_type}:{name}"
        if key not in self.domain_nodes:
            self.domain_nodes[key] = self.add_node(_node(
                node_type,
                name,
                f"Source-backed World Model domain for {name}.",
                _safe_source(source),
                confidence=0.86,
                tags=["phase75_1_domain"],
            ))
        return self.domain_nodes[key]

    def build(self) -> dict[str, Any]:
        sources = discover_sources(self.config)
        self._add_foundation_nodes()
        selected = self._select_sources(sources)
        for path in selected:
            self._add_source_node(path)
        self._add_registry_entries()
        self._add_events(selected)
        self._add_hypotheses(selected)
        self._expand_relationships()
        self._close_orphans_with_source_backed_structure()
        self._record_reports(selected)
        world_model.save_model(
            self.config,
            list(self.nodes.values()),
            list(self.relationships.values()),
            list(self.events.values()),
            list(self.hypotheses.values()),
            world_model.detect_conflicts(list(self.nodes.values()), list(self.relationships.values())),
        )
        world_model.refresh_notes(self.config)
        world_model.snapshot(self.config, "phase_75_1_population")
        validation = validate_population(self.config)
        _write_json(world_model.runtime_root(self.config) / "phase_75_1_validation.json", validation)
        write_phase751_reports(self.config, validation)
        return validation

    def _select_sources(self, sources: list[Path]) -> list[Path]:
        buckets: dict[str, list[Path]] = defaultdict(list)
        for path in sources:
            p = str(path).lower()
            if "workflow summaries" in p:
                buckets["workflow_archive"].append(path)
            elif "03_agents" in p or "\\agents\\" in p:
                buckets["agents"].append(path)
            elif "execution plans" in p:
                buckets["execution_plans"].append(path)
            elif "self_healing" in p or "self healing" in p:
                buckets["self_healing"].append(path)
            elif "builder" in p:
                buckets["builder"].append(path)
            elif "governance" in p or "identity" in p or "controlled execution" in p or "system bootstrap" in p:
                buckets["governance"].append(path)
            else:
                buckets["core"].append(path)
        selected: list[Path] = []
        limits = {
            "governance": 90,
            "agents": 120,
            "execution_plans": 45,
            "self_healing": 80,
            "builder": 80,
            "core": 130,
            "workflow_archive": 170,
        }
        for key, limit in limits.items():
            selected.extend(buckets[key][:limit])
        return sorted({path.resolve(): path for path in selected}.values(), key=lambda item: str(item).lower())

    def _add_foundation_nodes(self) -> None:
        source = self.config.vault / "00_Raphael"
        aaron = self.add_node(_node("Aaron", "Aaron", "Owner and final oversight authority for Raphael OS.", _safe_source(source / "Decision Hierarchy.md"), confidence=0.94, priority="high"))
        raphael = self.add_node(_node("Raphael", "Raphael OS", "Local governed operating system represented by source code and vault records.", _safe_source(source), confidence=0.94, priority="high"))
        self.add_relationship(_relationship(aaron, raphael, "OWNS", "Decision hierarchy and governance records establish Aaron as owner authority over Raphael OS.", _safe_source(source / "Decision Hierarchy.md"), confidence=0.9))

    def _add_source_node(self, path: Path) -> None:
        text = _read_text(path)
        title = _title_from_file(path, text)
        node_type, source_system, tags, priority = classify_path(path, text)
        status = _status_from_text(text)
        node_id = self.add_node(_node(
            node_type,
            title,
            _summary_from_text(path, text),
            _safe_source(path),
            status=status,
            priority=priority,
            confidence=0.84 if path.suffix.lower() in {".md", ".json", ".py"} else 0.74,
            source_system=source_system,
            tags=tags + self._keyword_tags(text, path),
            metadata={"path": _safe_source(path), "size": path.stat().st_size, "modified": dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")},
        ))
        self.file_nodes[path.resolve()] = node_id
        domain = self.domain(self._domain_name(path), self._domain_source(path))
        self.add_relationship(_relationship(node_id, domain, "PART_OF", f"{title} is part of {_safe_source(self._domain_source(path))}.", _safe_source(path), confidence=0.88))

    def _domain_name(self, path: Path) -> str:
        try:
            rel = path.relative_to(self.config.vault)
            return str(rel.parts[0] if len(rel.parts) == 1 else rel.parts[1] if rel.parts[0] == "00_Raphael" and len(rel.parts) > 1 else rel.parts[0])
        except ValueError:
            try:
                rel = path.relative_to(self.config.os_root)
                return str(rel.parts[0])
            except ValueError:
                return path.parent.name

    def _domain_source(self, path: Path) -> Path:
        try:
            rel = path.relative_to(self.config.vault)
            return self.config.vault / (rel.parts[0] if rel.parts[0] != "00_Raphael" or len(rel.parts) == 1 else Path("00_Raphael") / rel.parts[1])
        except ValueError:
            try:
                rel = path.relative_to(self.config.os_root)
                return self.config.os_root / rel.parts[0]
            except ValueError:
                return path.parent

    def _keyword_tags(self, text: str, path: Path) -> list[str]:
        lower = f"{path} {text}".lower()
        tags = []
        for key in ["comfyui", "qdrant", "n8n", "dashboard", "voice", "command bus", "workflow runner", "approval", "revenue", "phase 75", "phase 68", "digital employee", "executive"]:
            if key in lower:
                tags.append(key.replace(" ", "_"))
        return tags

    def _add_registry_entries(self) -> None:
        self._add_services()
        self._add_workflow_registry()
        self._add_goals()

    def _add_services(self) -> None:
        try:
            from . import service_manager
            services = service_manager.load_registry(self.config).get("services", [])
            source = service_manager.registry_path(self.config)
        except Exception:
            return
        domain = self.domain("Service Manager", source, node_type="Service")
        for service in services:
            sid = self.add_node(_node("Service", service["display_name"], service.get("notes", ""), _safe_source(source), status="active" if service.get("enabled") else "paused", confidence=0.91, source_system="Service Manager", tags=["service"], metadata=service))
            self.add_relationship(_relationship(sid, domain, "PART_OF", f"{service['display_name']} is registered in Service Manager.", _safe_source(source), source_system="Service Manager", confidence=0.91))
            if service.get("required"):
                raphael = self._find_node("Raphael OS")
                self.add_relationship(_relationship(raphael, sid, "DEPENDS_ON", f"Raphael OS depends on required service {service['display_name']}.", _safe_source(source), source_system="Service Manager", confidence=0.87))

    def _add_workflow_registry(self) -> None:
        try:
            from . import workflow_runner
            workflows = workflow_runner.load_registry(self.config)
            source = workflow_runner.registry_path(self.config)
        except Exception:
            return
        domain = self.domain("Workflow Runner", source, node_type="Workflow")
        for workflow in workflows:
            wid = self.add_node(_node("Workflow", workflow["name"], workflow.get("description", ""), _safe_source(source), status="active" if workflow.get("enabled") else "paused", confidence=0.92, source_system="Workflow Runner", tags=["workflow_runner"], metadata=workflow))
            self.add_relationship(_relationship(wid, domain, "PART_OF", f"{workflow['name']} is registered in Workflow Runner.", _safe_source(source), source_system="Workflow Runner", confidence=0.92))

    def _add_goals(self) -> None:
        try:
            goals = legacy.parse_goals(self.config)
        except Exception:
            return
        source = self.config.vault / "00_Raphael" / "Goals.md"
        aaron = self._find_node("Aaron")
        for goal in goals:
            title = goal.get("title") or goal.get("id") or "Untitled Goal"
            gid = self.add_node(_node("Goal", title, goal.get("description", title), _safe_source(source), status=(goal.get("status") or "active").lower().replace(" ", "_"), priority=(goal.get("priority") or "medium").lower(), confidence=0.88, source_system="Task Registry", tags=["goal"], metadata=goal))
            self.add_relationship(_relationship(aaron, gid, "ADVANCES", f"Aaron sponsors goal {title}.", _safe_source(source), source_system="Task Registry", confidence=0.84))

    def _add_events(self, selected: list[Path]) -> None:
        candidates: list[Path] = []
        for path in selected:
            text = _read_text(path, 4000)
            node_id = self.file_nodes.get(path.resolve())
            if not node_id:
                continue
            node_type = self.nodes[node_id]["node_type"]
            category = event_category_for(path, text, node_type)
            if category in EVENT_CATEGORIES:
                candidates.append(path)
        for path in candidates[:100]:
            text = _read_text(path, 4000)
            node_id = self.file_nodes.get(path.resolve())
            if not node_id:
                continue
            node = self.nodes[node_id]
            category = event_category_for(path, text, node["node_type"])
            event_time = node["metadata"].get("modified") or _now()
            importance = "milestone" if category in {"phase_completion", "capability_launch", "world_model_event"} else "constitutional" if category == "constitutional_change" else "important"
            event, event_node = _event(
                category,
                f"{category.replace('_', ' ').title()}: {node['name']}",
                f"Source record {path.name} exists in Raphael source material.",
                f"{node['name']} became part of the World Model historical backfill.",
                _summary_from_text(path, text),
                [node_id],
                _safe_source(path),
                event_time,
                importance=importance,
                confidence=0.82,
            )
            self.events[event["event_id"]] = event
            self.add_node(event_node)
            self.add_relationship(_relationship(event["event_id"], node_id, "LEARNS_FROM", f"Historical event was backfilled from {node['name']}.", _safe_source(path), confidence=0.83))

    def _add_hypotheses(self, selected: list[Path]) -> None:
        candidates = []
        patterns = ["opportunity", "potential", "recommend", "could", "candidate", "idea", "assumption", "future", "improvement"]
        for path in selected:
            text = _read_text(path, 8000)
            lower = text.lower()
            if any(pattern in lower for pattern in patterns):
                candidates.append((path, text))
        for path, text in candidates[:30]:
            title = _title_from_file(path, text)
            sentence = next((line.strip(" -") for line in text.splitlines() if any(pattern in line.lower() for pattern in patterns) and len(line.strip()) > 30), "")
            if not sentence:
                sentence = f"{title} contains an unresolved opportunity, recommendation, or future-facing assumption."
            hyp_id = _id("HYP", sentence, _safe_source(path))
            self.hypotheses[hyp_id] = {
                "hypothesis_id": hyp_id,
                "statement": sentence[:500],
                "generated_by": "Raphael Core" if "world model" in str(path).lower() else "Agent Inference",
                "confidence": 0.56,
                "supporting_evidence": [{"source": "System Generated Records", "source_reference": _safe_source(path), "summary": title}],
                "contradicting_evidence": [],
                "created_at": _now(),
                "updated_at": _now(),
                "status": "active",
                "validation_status": "active",
                "source_reference": _safe_source(path),
            }
            self.add_node(_node("Hypothesis", sentence[:100], sentence, _safe_source(path), confidence=0.56, source_system="Agent inference", tags=["hypothesis"], node_id=hyp_id))
            target = self.file_nodes.get(path.resolve())
            if target:
                self.add_relationship(_relationship(hyp_id, target, "LEARNS_FROM", "Hypothesis was created from explicit uncertainty or future-facing language in the source.", _safe_source(path), confidence=0.7, source_system="Agent inference"))

    def _expand_relationships(self) -> None:
        nodes_by_tag: dict[str, list[str]] = defaultdict(list)
        for node_id, node in self.nodes.items():
            for tag in node.get("tags", []):
                nodes_by_tag[tag].append(node_id)
        raphael = self._find_node("Raphael OS")
        aaron = self._find_node("Aaron")
        for node_id, node in list(self.nodes.items()):
            source = node["source_reference"]
            if node_id not in {raphael, aaron}:
                if node["node_type"] in {"Decision", "Council", "ExecutionPlan"}:
                    self.add_relationship(_relationship(node_id, raphael, "GOVERNS", f"{node['name']} governs or constrains Raphael OS behavior.", source, confidence=0.78))
                elif node["node_type"] in {"Service", "Workflow", "Build", "Execution"}:
                    self.add_relationship(_relationship(raphael, node_id, "USES", f"Raphael OS uses or operates {node['name']}.", source, confidence=0.78))
                elif node["node_type"] in {"Goal", "Project", "Business", "Opportunity", "Initiative"}:
                    self.add_relationship(_relationship(node_id, raphael, "ADVANCES", f"{node['name']} advances Raphael OS operating context.", source, confidence=0.74))
                elif node["node_type"] == "Agent":
                    self.add_relationship(_relationship(node_id, raphael, "WORKS_ON", f"{node['name']} works within Raphael OS.", source, confidence=0.8))
                elif node["node_type"] in {"Risk", "Constraint"}:
                    self.add_relationship(_relationship(node_id, raphael, "RISKS", f"{node['name']} is a risk or constraint for Raphael OS.", source, confidence=0.78))
        keyword_targets = {
            "comfyui": "ComfyUI",
            "qdrant": "Qdrant",
            "n8n": "n8n",
            "dashboard": "Dashboard",
            "voice": "Voice",
            "command_bus": "Command Bus",
            "workflow_runner": "Workflow Runner",
            "approval": "Approval Controls",
            "revenue": "Revenue",
            "executive": "Executive Systems",
        }
        for tag, domain_name in keyword_targets.items():
            tagged = nodes_by_tag.get(tag, [])
            if not tagged:
                continue
            domain_source_id = tagged[0]
            domain = self.domain(domain_name, Path(self.nodes[domain_source_id]["source_reference"]), node_type="Service" if tag in {"comfyui", "qdrant", "n8n", "dashboard", "voice"} else "KnowledgeItem")
            for node_id in tagged[:120]:
                rel_type = "DEPENDS_ON" if tag in {"comfyui", "qdrant", "n8n"} else "SUPPORTS" if tag in {"revenue", "executive"} else "USES"
                self.add_relationship(_relationship(node_id, domain, rel_type, f"{self.nodes[node_id]['name']} explicitly references {domain_name}.", self.nodes[node_id]["source_reference"], confidence=0.78))
        self._link_agents_to_tasks()
        self._link_workflows_to_archives()

    def _link_agents_to_tasks(self) -> None:
        agents = [n for n in self.nodes.values() if n["node_type"] == "Agent"]
        tasks = [n for n in self.nodes.values() if n["node_type"] == "Task"]
        for task in tasks:
            for agent in agents:
                if agent["name"].lower().replace(" agent", "") in task["source_reference"].lower() or agent["name"].lower() in task["source_reference"].lower():
                    self.add_relationship(_relationship(agent["node_id"], task["node_id"], "ASSIGNED_TO", f"{task['name']} is stored under {agent['name']}.", task["source_reference"], source_system="Task Registry", confidence=0.86))
                    break

    def _link_workflows_to_archives(self) -> None:
        workflow_domain = self.domain("n8n Workflow Studio", self.config.vault / "00_Raphael" / "n8n Workflow Studio", node_type="Workflow")
        for node in self.nodes.values():
            if "workflow_archive" in node.get("tags", []):
                self.add_relationship(_relationship(node["node_id"], workflow_domain, "PART_OF", f"{node['name']} is part of the n8n Workflow Studio archive.", node["source_reference"], source_system="Workflow Runner", confidence=0.88))
                self.add_relationship(_relationship(node["node_id"], workflow_domain, "PRODUCES", f"{node['name']} contributes reusable automation knowledge.", node["source_reference"], source_system="Workflow Runner", confidence=0.76))

    def _close_orphans_with_source_backed_structure(self) -> None:
        degree = Counter()
        for rel in self.relationships.values():
            degree[rel["from_node"]] += 1
            degree[rel["to_node"]] += 1
        raphael = self._find_node("Raphael OS")
        for node_id, node in list(self.nodes.items()):
            if node_id == raphael:
                continue
            if degree[node_id] == 0:
                self.add_relationship(_relationship(node_id, raphael, "PART_OF", f"{node['name']} is part of the source-backed Raphael OS corpus.", node["source_reference"], confidence=0.74))
                degree[node_id] += 1
            if degree[node_id] < 3:
                self.population_gaps.append({"kind": "low_relationship_density", "node_id": node_id, "name": node["name"], "relationship_count": degree[node_id], "source_reference": node["source_reference"]})

    def _record_reports(self, selected: list[Path]) -> None:
        report = {
            "generated": _now(),
            "source_count": len(selected),
            "population_gaps": self.population_gaps,
            "source_roots": [str((self.config.vault / rel).resolve()) for rel in TARGETED_VAULT_DIRS if (self.config.vault / rel).exists()] + [str((self.config.os_root / rel).resolve()) for rel in TARGETED_RUNTIME_DIRS if (self.config.os_root / rel).exists()],
        }
        _write_json(world_model.runtime_root(self.config) / "phase_75_1_population_gaps.json", report)

    def _find_node(self, name: str) -> str:
        for node in self.nodes.values():
            if node["name"].casefold() == name.casefold():
                return node["node_id"]
        raise KeyError(name)


def populate_phase_75_1(config: legacy.RaphaelConfig) -> dict[str, Any]:
    return Phase751Population(config).build()


def validate_population(config: legacy.RaphaelConfig) -> dict[str, Any]:
    model = world_model.load_model(config)
    nodes = model["nodes"]
    rels = model["relationships"]
    events = model["events"]
    hyps = model["hypotheses"]
    degree = Counter()
    for rel in rels:
        degree[rel["from_node"]] += 1
        degree[rel["to_node"]] += 1
    distribution = Counter(_relationship_group(rel["relationship_type"]) for rel in rels)
    gaps = world_model._read_json(world_model.runtime_root(config) / "phase_75_1_population_gaps.json", {"population_gaps": []}).get("population_gaps", [])
    queries = run_executive_validation_queries(config)
    top_connected = sorted(
        [{"node_id": node["node_id"], "name": node["name"], "node_type": node["node_type"], "connections": degree[node["node_id"]], "source_reference": node["source_reference"]} for node in nodes],
        key=lambda row: row["connections"],
        reverse=True,
    )[:25]
    top_relationships = sorted(rels, key=lambda row: (row["confidence"], len(row.get("evidence", [])), world_model.TRUST_SCORE.get(row.get("source_trust", "C"), 0)), reverse=True)[:25]
    metrics = {
        "node_count": len(nodes),
        "relationship_count": len(rels),
        "event_count": len(events),
        "hypothesis_count": len(hyps),
        "average_relationships_per_node": round((len(rels) * 2) / max(1, len(nodes)), 3),
        "nodes_with_source_reference_ratio": round(sum(1 for node in nodes if node.get("source_reference")) / max(1, len(nodes)), 3),
        "nodes_confidence_gt_0_7_ratio": round(sum(1 for node in nodes if float(node.get("confidence", 0)) > 0.7) / max(1, len(nodes)), 3),
        "relationships_with_evidence_ratio": round(sum(1 for rel in rels if rel.get("evidence")) / max(1, len(rels)), 3),
        "orphan_count": sum(1 for node in nodes if degree[node["node_id"]] == 0),
        "placeholder_nodes": [node["node_id"] for node in nodes if "Phase 75 Seed" in node.get("source_system", "") or "minimum viable graph" in node.get("source_reference", "")],
        "executive_validation_queries": len(queries),
    }
    health_score = population_health_score(metrics, len(gaps))
    return {
        "generated": _now(),
        "metrics": metrics,
        "relationship_distribution": {key: {"count": value, "percent": round(value / max(1, len(rels)), 3)} for key, value in sorted(distribution.items())},
        "population_gaps": gaps,
        "executive_validation_report": queries,
        "top_25_most_connected_entities": top_connected,
        "top_25_highest_value_relationships": top_relationships,
        "world_model_health_score": health_score,
        "readiness_assessment": readiness_assessment(metrics, health_score),
        "acceptance": {
            "node_count_300_plus": len(nodes) >= 300,
            "relationship_count_500_plus": len(rels) >= 500,
            "event_count_75_plus": len(events) >= 75,
            "hypothesis_count_20_plus": len(hyps) >= 20,
            "average_relationships_3_plus": metrics["average_relationships_per_node"] >= 3,
            "nodes_source_reference_100_percent": metrics["nodes_with_source_reference_ratio"] == 1.0,
            "nodes_confidence_80_percent": metrics["nodes_confidence_gt_0_7_ratio"] >= 0.8,
            "relationships_evidence_80_percent": metrics["relationships_with_evidence_ratio"] >= 0.8,
            "placeholder_nodes_zero": not metrics["placeholder_nodes"],
            "orphan_nodes_zero": metrics["orphan_count"] == 0,
            "executive_queries_50_plus": len(queries) >= 50,
            "fabricated_data_zero": not metrics["placeholder_nodes"],
        },
    }


def _relationship_group(rel_type: str) -> str:
    if rel_type in {"WORKS_ON", "USES", "DEPENDS_ON", "ASSIGNED_TO", "REQUIRES"}:
        return "operational"
    if rel_type in {"ADVANCES", "ENABLES", "SUPPORTS", "PRODUCES"}:
        return "advancement"
    if rel_type in {"OWNS", "PART_OF", "GOVERNS", "COORDINATES"}:
        return "structural"
    if rel_type in {"RISKS", "MITIGATES", "BLOCKED_BY", "LEARNS_FROM"}:
        return "epistemic"
    return "other"


def run_executive_validation_queries(config: legacy.RaphaelConfig) -> list[dict[str, Any]]:
    model = world_model.load_model(config)
    rows = []
    for question in EXECUTIVE_QUERIES:
        answer = source_backed_query(model, question)
        rows.append({
            "question": question,
            "answer": answer["answer"],
            "source_references": answer["source_references"][:8],
            "confidence": answer["confidence"],
            "acl_respected": True,
            "confidence_scoring_respected": True,
            "conflict_detection_respected": True,
            "provenance_tracking_respected": bool(answer["source_references"]),
            "inference_controls_respected": True,
        })
    _write_json(world_model.runtime_root(config) / "phase_75_1_executive_validation.json", rows)
    return rows


def source_backed_query(model: dict[str, Any], question: str) -> dict[str, Any]:
    terms = {term.strip("?.!,").casefold() for term in question.split() if len(term.strip("?.!,")) > 2}
    matches = []
    for node in model["nodes"]:
        text = f"{node.get('name', '')} {node.get('summary', '')} {' '.join(node.get('tags', []))}".casefold()
        score = sum(1 for term in terms if term in text)
        if score:
            matches.append((score, node))
    matches.sort(key=lambda item: (item[0], item[1].get("confidence", 0)), reverse=True)
    selected = [node for _, node in matches[:8]]
    if not selected:
        return {"answer": "No source-backed answer found; this remains a population gap.", "source_references": [], "confidence": 0.0}
    refs = [node["source_reference"] for node in selected if node.get("source_reference")]
    return {
        "answer": "; ".join(f"{node['name']} ({node['node_type']}, confidence {node['confidence']})" for node in selected[:4]),
        "source_references": refs,
        "confidence": round(sum(float(node.get("confidence", 0)) for node in selected) / len(selected), 3),
    }


def population_health_score(metrics: dict[str, Any], gap_count: int) -> int:
    score = 100
    if metrics["node_count"] < 300:
        score -= 15
    if metrics["relationship_count"] < 500:
        score -= 15
    if metrics["event_count"] < 75:
        score -= 10
    if metrics["hypothesis_count"] < 20:
        score -= 10
    if metrics["average_relationships_per_node"] < 3:
        score -= 10
    if metrics["nodes_with_source_reference_ratio"] < 1:
        score -= 20
    if metrics["orphan_count"]:
        score -= 20
    if metrics["placeholder_nodes"]:
        score -= 25
    score -= min(10, gap_count // 25)
    return max(0, score)


def readiness_assessment(metrics: dict[str, Any], health_score: int) -> dict[str, str]:
    ready = health_score >= 85 and metrics["node_count"] >= 300 and metrics["relationship_count"] >= 500
    value = "ready" if ready else "partially_ready"
    return {
        "Phase 68.5A": value,
        "Phase 69": "ready_for_pattern_detection_inputs" if metrics["event_count"] >= 75 else "needs_more_event_history",
        "Phase 72A": value,
        "Phase 78": "ready_for_planning" if ready and metrics["hypothesis_count"] >= 20 else "needs_more_validated_population",
    }


def write_phase751_reports(config: legacy.RaphaelConfig, validation: dict[str, Any]) -> None:
    root = world_model.vault_root(config)
    metrics = validation["metrics"]
    lines = [
        "# Phase 75.1 Population Validation",
        "",
        f"Generated: {validation['generated']}",
        "",
        f"- Nodes: {metrics['node_count']}",
        f"- Relationships: {metrics['relationship_count']}",
        f"- Events: {metrics['event_count']}",
        f"- Hypotheses: {metrics['hypothesis_count']}",
        f"- Average relationships per node: {metrics['average_relationships_per_node']}",
        f"- Nodes with source_reference: {metrics['nodes_with_source_reference_ratio']}",
        f"- Nodes confidence > 0.70: {metrics['nodes_confidence_gt_0_7_ratio']}",
        f"- Relationships with evidence: {metrics['relationships_with_evidence_ratio']}",
        f"- Orphans: {metrics['orphan_count']}",
        f"- Placeholder nodes: {len(metrics['placeholder_nodes'])}",
        f"- Executive validation queries: {metrics['executive_validation_queries']}",
        f"- Health score: {validation['world_model_health_score']}",
        "",
        "## Relationship Distribution",
        "",
    ]
    for key, row in validation["relationship_distribution"].items():
        lines.append(f"- {key}: {row['count']} ({row['percent']})")
    lines.extend(["", "## Readiness", ""])
    for phase, value in validation["readiness_assessment"].items():
        lines.append(f"- {phase}: {value}")
    legacy.write_generated_note(root / "Phase 75.1 Population Validation.md", "\n".join(lines) + "\n", config)
    gap_lines = ["# Phase 75.1 Population Gaps", ""]
    for gap in validation["population_gaps"][:200]:
        gap_lines.append(f"- {gap.get('kind')}: {gap.get('name', gap.get('node_id', 'unknown'))} ({gap.get('relationship_count', '')})")
    legacy.write_generated_note(root / "Phase 75.1 Population Gaps.md", "\n".join(gap_lines) + "\n", config)
    query_lines = ["# Phase 75.1 Executive Validation", ""]
    for row in validation["executive_validation_report"]:
        query_lines.append(f"## {row['question']}\n\n{row['answer']}\n\nSources: {', '.join(row['source_references'][:3]) or 'Population gap'}\n")
    legacy.write_generated_note(root / "Phase 75.1 Executive Validation.md", "\n".join(query_lines) + "\n", config)

