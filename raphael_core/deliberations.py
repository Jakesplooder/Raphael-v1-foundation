from typing import List, Dict
from .kernel.storage import KernelStorage
from .kernel.event_bus import emit

storage = KernelStorage()

class DeliberationEngine:
    def __init__(self):
        self.domain = "deliberations"

    def start_deliberation(self, topic: str, participants: List[str]):
        d_id = f"DELIB-{hash(topic)}"
        record = {
            "topic": topic,
            "participants": participants,
            "status": "active"
        }
        storage.save(self.domain, f"{d_id}.json", record)
        emit("DELIBERATION_STARTED", "DeliberationEngine", {"deliberation_id": d_id, "topic": topic})
        return d_id
