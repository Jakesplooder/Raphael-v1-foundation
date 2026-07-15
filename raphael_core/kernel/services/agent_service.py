import logging
import uuid
from typing import List, Optional
from ..models.agent import AgentDefinition, AgentInstance, AgentStatus, MemoryScope
from ..repositories.agent_repository import AgentRepository

logger = logging.getLogger("rrk.services.agent")

class AgentService:
    """Core CRUD and state management for Agents."""
    
    def __init__(self, repository: AgentRepository):
        self.repository = repository
        
    def create_definition(self, name: str, role: str, description: str, capabilities: List[str], permissions: List[str]) -> AgentDefinition:
        df = AgentDefinition(
            name=name,
            role=role,
            description=description,
            capabilities=capabilities,
            permissions=permissions
        )
        self.repository.save_definition(df)
        return df
        
    def spawn_agent(self, definition_name: str, memory_scope: MemoryScope = MemoryScope.NONE) -> AgentInstance:
        df = self.repository.get_definition(definition_name)
        if not df:
            raise ValueError(f"Agent definition '{definition_name}' not found.")
            
        instance_id = f"agent_{uuid.uuid4().hex[:8]}"
        inst = AgentInstance(
            id=instance_id,
            definition=df.name,
            status=AgentStatus.CREATED,
            memory_scope=memory_scope
        )
        self.repository.save_instance(inst)
        return inst
        
    def get_agent(self, instance_id: str) -> Optional[AgentInstance]:
        return self.repository.get_instance(instance_id)
        
    def get_definition(self, definition_name: str) -> Optional[AgentDefinition]:
        return self.repository.get_definition(definition_name)
        
    def update_status(self, instance_id: str, status: AgentStatus) -> None:
        inst = self.repository.get_instance(instance_id)
        if inst:
            inst.status = status
            self.repository.save_instance(inst)
