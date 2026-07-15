from .kernel.storage import KernelStorage
from .kernel.event_bus import emit

storage = KernelStorage()

class InitiativeQueue:
    def __init__(self):
        self.domain = "initiatives"

    def enqueue(self, initiative: dict):
        queue = storage.load(self.domain, "queue.json") or []
        queue.append(initiative)
        storage.save(self.domain, "queue.json", queue)
        emit("INITIATIVE_QUEUED", "InitiativeQueue", initiative)
