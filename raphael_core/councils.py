from .kernel.storage import KernelStorage
from .kernel.event_bus import emit

storage = KernelStorage()

class CouncilsManager:
    def __init__(self):
        self.domain = "councils"

    def convene_council(self, council_type: str, issue: dict):
        record = {"type": council_type, "issue": issue, "status": "convened"}
        storage.save(self.domain, f"latest_{council_type}.json", record)
        emit("COUNCIL_CONVENED", "CouncilsManager", {"council_type": council_type})
