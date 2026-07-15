import json
import os
from pydantic import BaseModel
from typing import Dict

class MigrationStatus(BaseModel):
    domain: str
    status: str
    legacy_dependency: bool
    storage_migrated: bool
    event_bus_connected: bool

class MigrationRegistry:
    """
    Tracks the RRK Kernel Migration progress.
    Used by audit.py to determine true completion state.
    """
    def __init__(self, registry_file: str = "raphael_core/kernel/migration_state.json"):
        self.registry_file = registry_file
        self.state: Dict[str, MigrationStatus] = {}
        self.load()
        
    def load(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, "r") as f:
                data = json.load(f)
                self.state = {k: MigrationStatus(**v) for k, v in data.items()}
                
    def save(self):
        with open(self.registry_file, "w") as f:
            json.dump({k: v.model_dump() for k, v in self.state.items()}, f, indent=2)
            
    def update(self, domain: str, status: str, legacy_dependency: bool,
               storage_migrated: bool, event_bus_connected: bool):
        self.state[domain] = MigrationStatus(
            domain=domain,
            status=status,
            legacy_dependency=legacy_dependency,
            storage_migrated=storage_migrated,
            event_bus_connected=event_bus_connected
        )
        self.save()

    def get_summary(self) -> dict:
        total = len(self.state)
        native = sum(1 for v in self.state.values() if v.status == "native" and not v.legacy_dependency)
        completion = round((native / total) * 100, 1) if total > 0 else 0.0
        
        return {
            "total_domains": total,
            "native_domains": native,
            "legacy_domains": total - native,
            "completion_percentage": completion,
            "domains": {k: v.model_dump() for k, v in self.state.items()}
        }
