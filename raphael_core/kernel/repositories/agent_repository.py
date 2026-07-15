import json
import logging
from pathlib import Path
from typing import List, Optional, Dict
from ..models.agent import AgentDefinition, AgentInstance

logger = logging.getLogger("rrk.repository.agent")

class AgentRepository:
    """Physical I/O for storing Agent Identities and Instances."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.definitions_path = self.vault_path / "Definitions"
        self.instances_path = self.vault_path / "Instances"
        
        self.definitions_path.mkdir(parents=True, exist_ok=True)
        self.instances_path.mkdir(parents=True, exist_ok=True)
        
        self.definitions: Dict[str, AgentDefinition] = {}
        self.instances: Dict[str, AgentInstance] = {}
        
        self._load_all()
        
    def _load_all(self):
        # Load Definitions
        for file in self.definitions_path.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    df = AgentDefinition(**data)
                    self.definitions[df.name] = df
            except Exception as e:
                logger.error(f"Failed to load agent definition {file}: {e}")
                
        # Load Instances
        for file in self.instances_path.glob("*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    inst = AgentInstance(**data)
                    self.instances[inst.id] = inst
            except Exception as e:
                logger.error(f"Failed to load agent instance {file}: {e}")

    def save_definition(self, definition: AgentDefinition) -> None:
        self.definitions[definition.name] = definition
        file_path = self.definitions_path / f"{definition.name.lower().replace(' ', '_')}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(definition.model_dump_json(indent=2))
            
    def get_definition(self, name: str) -> Optional[AgentDefinition]:
        return self.definitions.get(name)

    def save_instance(self, instance: AgentInstance) -> None:
        self.instances[instance.id] = instance
        file_path = self.instances_path / f"{instance.id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(instance.model_dump_json(indent=2))
            
    def get_instance(self, instance_id: str) -> Optional[AgentInstance]:
        return self.instances.get(instance_id)

    def list_instances(self) -> List[AgentInstance]:
        return list(self.instances.values())
