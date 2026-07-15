import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import os

from ..models.world import WorldNode, WorldRelationship, WorldEvent, WorldHypothesis

logger = logging.getLogger("rrk.repositories.world")

class WorldRepository:
    """Abstract JSON repository for the World Model Graph."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Files
        self.nodes_file = self.base_path / "nodes.json"
        self.rels_file = self.base_path / "relationships.json"
        self.events_file = self.base_path / "events.json"
        self.hypo_file = self.base_path / "hypotheses.json"
        self.conflicts_file = self.base_path / "conflicts.json"
        self.access_file = self.base_path / "access_policy.json"
        self.inference_file = self.base_path / "inference_controls.json"
        
        # Initialize files if they don't exist
        for f in [self.nodes_file, self.rels_file, self.events_file, self.hypo_file, self.conflicts_file]:
            if not f.exists():
                self._write_json(f, [])
                
        if not self.access_file.exists():
            self._write_json(self.access_file, {"version": 1, "agents": {}, "base_rate_limits_per_hour": {}})
            
        if not self.inference_file.exists():
            self._write_json(self.inference_file, {"version": 1, "sensitive_correlations": [], "owners": []})
            
    def _read_json(self, path: Path, default: Any = None) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default if default is not None else []

    def _write_json(self, path: Path, data: Any) -> None:
        temp_path = path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        temp_path.replace(path)

    # --- Nodes ---
    def get_nodes(self) -> List[WorldNode]:
        data = self._read_json(self.nodes_file)
        return [WorldNode(**row) for row in data]

    def save_nodes(self, nodes: List[WorldNode]) -> None:
        self._write_json(self.nodes_file, [n.model_dump() for n in nodes])

    def get_node(self, node_id: str) -> Optional[WorldNode]:
        for n in self.get_nodes():
            if n.node_id == node_id:
                return n
        return None

    def upsert_node(self, node: WorldNode) -> None:
        nodes = self.get_nodes()
        idx = next((i for i, n in enumerate(nodes) if n.node_id == node.node_id), -1)
        if idx >= 0:
            nodes[idx] = node
        else:
            nodes.append(node)
        self.save_nodes(nodes)

    # --- Relationships ---
    def get_relationships(self) -> List[WorldRelationship]:
        data = self._read_json(self.rels_file)
        return [WorldRelationship(**row) for row in data]
        
    def save_relationships(self, rels: List[WorldRelationship]) -> None:
        self._write_json(self.rels_file, [r.model_dump() for r in rels])

    def upsert_relationship(self, rel: WorldRelationship) -> None:
        rels = self.get_relationships()
        idx = next((i for i, r in enumerate(rels) if r.relationship_id == rel.relationship_id), -1)
        if idx >= 0:
            rels[idx] = rel
        else:
            rels.append(rel)
        self.save_relationships(rels)

    # --- Events ---
    def get_events(self) -> List[WorldEvent]:
        data = self._read_json(self.events_file)
        return [WorldEvent(**row) for row in data]
        
    def save_events(self, events: List[WorldEvent]) -> None:
        self._write_json(self.events_file, [e.model_dump() for e in events])

    def upsert_event(self, event: WorldEvent) -> None:
        events = self.get_events()
        events.append(event)
        self.save_events(events)

    # --- Hypotheses ---
    def get_hypotheses(self) -> List[WorldHypothesis]:
        data = self._read_json(self.hypo_file)
        return [WorldHypothesis(**row) for row in data]
        
    def save_hypotheses(self, hypos: List[WorldHypothesis]) -> None:
        self._write_json(self.hypo_file, [h.model_dump() for h in hypos])
        
    def upsert_hypothesis(self, hypo: WorldHypothesis) -> None:
        hypos = self.get_hypotheses()
        idx = next((i for i, h in enumerate(hypos) if h.hypothesis_id == hypo.hypothesis_id), -1)
        if idx >= 0:
            hypos[idx] = hypo
        else:
            hypos.append(hypo)
        self.save_hypotheses(hypos)
        
    # --- Config ---
    def get_access_policy(self) -> Dict[str, Any]:
        return self._read_json(self.access_file, {})
        
    def get_inference_controls(self) -> Dict[str, Any]:
        return self._read_json(self.inference_file, {})
