import logging
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

logger = logging.getLogger("rrk.agents.memory")

class AgentMemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: f"AMEM-{uuid.uuid4().hex[:8].upper()}")
    category: str # "decision", "preference", "strategy", "failure"
    agent_type: str
    content: str
    context: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    timestamp: float = Field(default_factory=datetime.now().timestamp)

class AgentMemoryService:
    """
    Agent-specific memory vault.
    Stores decisions, preferences, past plans, successful strategies, and failures.
    """
    def __init__(self):
        self.memory: List[AgentMemoryEntry] = []
        
    def save_memory(self, agent_type: str, category: str, content: str, context: Dict[str, Any] = None, confidence: float = 1.0):
        entry = AgentMemoryEntry(
            agent_type=agent_type,
            category=category,
            content=content,
            context=context or {},
            confidence=confidence
        )
        self.memory.append(entry)
        logger.info(f"[AgentMemory] Saved {category} for {agent_type}: {content[:50]}...")
        
    def retrieve_memories(self, agent_type: str, category: str = None) -> List[AgentMemoryEntry]:
        results = [m for m in self.memory if m.agent_type == agent_type]
        if category:
            results = [m for m in results if m.category == category]
        return results
