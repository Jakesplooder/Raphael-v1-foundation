import uuid
from .kernel.storage import KernelStorage
from .kernel.event_bus import emit

storage = KernelStorage()

class IdentityManager:
    def __init__(self):
        self.domain = "identity"

    def create_identity(self, name: str, role: str):
        uid = str(uuid.uuid4())
        record = {"id": uid, "name": name, "role": role}
        storage.save(self.domain, f"{uid}.json", record)
        emit("IDENTITY_CREATED", "IdentityManager", record)
        return uid
