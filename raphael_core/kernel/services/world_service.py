import hashlib
import logging
import time
from typing import Dict, Any, List, Optional
import datetime as dt

from ..models.world import (
    WorldNode, WorldRelationship, WorldEvent, WorldHypothesis,
    NodeStatus, ConfidenceState
)
from ..repositories.world_repository import WorldRepository

logger = logging.getLogger("rrk.services.world")

class WorldService:
    """Core domain logic for the World Model."""
    
    def __init__(self, repository: WorldRepository):
        self.repository = repository
        
    def _generate_id(self, prefix: str, *parts: Any) -> str:
        digest = hashlib.sha1("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:10].upper()
        return f"{prefix}-{digest}"

    def get_node(self, node_id: str) -> Optional[WorldNode]:
        return self.repository.get_node(node_id)
        
    def add_node(self, node_type: str, name: str, summary: str, source_system: str, source_ref: str, confidence: float = 0.82, metadata: dict = None) -> WorldNode:
        node_id = self._generate_id(node_type.upper(), name)
        existing = self.repository.get_node(node_id)
        
        n = WorldNode(
            node_id=node_id,
            node_type=node_type,
            name=name,
            summary=summary,
            source_system=source_system,
            source_reference=source_ref,
            confidence=confidence,
            confidence_state=self._compute_confidence_state(confidence),
            metadata=metadata or {},
            created_at=existing.created_at if existing else time.time()
        )
        self.repository.upsert_node(n)
        return n

    def add_relationship(self, from_node: str, to_node: str, rel_type: str, summary: str, source_system: str, source_ref: str, confidence: float = 0.82) -> WorldRelationship:
        rel_id = self._generate_id("REL", from_node, rel_type, to_node, summary)
        
        evidence = [{"source": source_system, "source_reference": source_ref, "summary": summary}]
        r = WorldRelationship(
            relationship_id=rel_id,
            from_node=from_node,
            to_node=to_node,
            relationship_type=rel_type,
            summary=summary,
            source_system=source_system,
            source_reference=source_ref,
            confidence=confidence,
            confidence_state=self._compute_confidence_state(confidence),
            evidence=evidence
        )
        self.repository.upsert_relationship(r)
        return r

    def add_event(self, event_type: str, cause: str, effect: str, outcome: str, related: List[str], source_system: str, source_ref: str) -> WorldEvent:
        event_id = self._generate_id("EVENT", event_type, cause, effect, outcome)
        e = WorldEvent(
            event_id=event_id,
            event_type=event_type,
            cause=cause,
            effect=effect,
            outcome=outcome,
            related_entities=related,
            source_system=source_system,
            source_reference=source_ref
        )
        self.repository.upsert_event(e)
        return e

    def add_hypothesis(self, statement: str, generated_by: str, confidence: float = 0.55) -> WorldHypothesis:
        h_id = self._generate_id("HYP", statement)
        h = WorldHypothesis(
            hypothesis_id=h_id,
            statement=statement,
            generated_by=generated_by,
            confidence=confidence
        )
        self.repository.upsert_hypothesis(h)
        return h
        
    def _compute_confidence_state(self, confidence: float) -> ConfidenceState:
        if confidence > 0.25:
            return ConfidenceState.ACTIVE
        elif 0.15 <= confidence <= 0.25:
            return ConfidenceState.REVIEW_CANDIDATE
        elif 0.10 <= confidence < 0.15:
            return ConfidenceState.DORMANT
        return ConfidenceState.DEPRECATED

    def query_model(self, agent_id: str, purpose: str, question: str) -> Dict[str, Any]:
        """Inference Gating (Access Policy & Blocks)."""
        access = self.repository.get_access_policy()
        controls = self.repository.get_inference_controls()
        
        actor = access.get("agents", {}).get(agent_id) or access.get("agents", {}).get("Standard Agent", {"trust_tier": 1})
        
        # Simple rule: if question contains blocked sensitive correlations
        q_lower = question.lower()
        blocked_found = None
        for correlation in controls.get("sensitive_correlations", []):
            if all(term.lower() in q_lower for term in correlation):
                blocked_found = correlation
                break
                
        if blocked_found and actor.get("trust_tier", 0) < 3:
            return {
                "allowed": False,
                "answer": f"I cannot assemble that sensitive correlation: {blocked_found}. Executive review is required.",
                "blocked_correlation": blocked_found
            }
            
        return {
            "allowed": True,
            "answer": f"Simulated World Model response for: {question}",
            "purpose": purpose
        }
