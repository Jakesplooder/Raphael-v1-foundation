import logging
from typing import List, Dict, Any, Optional

from ..models.build_intelligence import EngineeringMemoryEntry

logger = logging.getLogger("rrk.services.builder.engineering_memory")

class BuilderKnowledgeBase:
    """
    Knowledge Base for the Builder (Milestone 5).
    Stores and retrieves architectural decisions, successful patches, reusable modules, 
    framework conventions, common fixes, and preferred project layouts.
    Turns every successful build into future training data for Raphael.
    """
    
    def __init__(self):
        self.entries: List[EngineeringMemoryEntry] = []
        
    def save_lesson(self, category: str, content: str, tags: List[str] = None, context: Dict[str, Any] = None):
        """
        Saves a new piece of engineering experience.
        Categories: 'architectural_decision', 'successful_patch', 'reusable_module', 
        'framework_convention', 'common_fix', 'project_layout'.
        """
        entry = EngineeringMemoryEntry(
            category=category,
            content=content,
            tags=tags or [],
            context=context or {}
        )
        self.entries.append(entry)
        logger.info(f"[BuilderKnowledgeBase] Saved {category} memory: {content[:100]}...")
        # TODO: Persist to Qdrant memory repository
        
    def retrieve_relevant(self, query: str, limit: int = 5) -> List[EngineeringMemoryEntry]:
        """
        Retrieves engineering memories relevant to the current problem or architecture.
        Mocks a semantic search.
        """
        # MOCK IMPLEMENTATION
        results = [e for e in self.entries if any(t in query for t in e.tags)]
        return results[:limit]
