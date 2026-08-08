from typing import Dict, Any, List

# Rule 1: We must use world_model.related for known graph traversals
from raphael_core import world_model
from raphael_core.kernel.interfaces import Event, EventType
from raphael_core.kernel.event_bus import emit

def get_career_twin(config: Any, person_node_id: str) -> Dict[str, Any]:
    """
    Constructs the Career Twin state projection for a given person.
    Strictly uses graph traversal (world_model.related) as per ADR-012.
    """
    raw_related = world_model.related(config, person_node_id)
    
    twin_state = {
        "person_id": person_node_id,
        "skills": []
    }
    
    # Check if raw_related has the structure expected
    if "related" in raw_related:
        for item in raw_related["related"]:
            rel = item.get("relationship", {})
            node = item.get("node", {})
            
            if rel.get("relationship_type") == "RELATED_TO" or rel.get("relationship_type") == "HAS_SKILL":
                if node.get("node_type") == "Skill":
                    twin_state["skills"].append({
                        "name": node.get("name"),
                        "confidence": rel.get("confidence", node.get("confidence", 0.0)),
                        "source": rel.get("source_system", "Unknown"),
                        "evidence": rel.get("evidence", [])
                    })
    return twin_state

def record_skill_acquisition(person_node_id: str, skill_name: str, confidence: float, source: str) -> None:
    """
    Records a new skill for a person.
    Must NOT mutate World Model directly. Emits a CAREER_SKILL_VERIFIED event.
    """
    event = Event(
        source="career_twin",
        type=EventType.CAREER_SKILL_VERIFIED,
        payload={
            "person_id": person_node_id,
            "skill_name": skill_name,
            "confidence": confidence,
            "source": source
        }
    )
    # emit is from global_event_bus
    emit(event.type, "career_twin", event.payload)

