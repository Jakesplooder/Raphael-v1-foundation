from typing import List, Dict, Any
from ...kernel.event_bus import emit
from ...kernel.storage import KernelStorage

storage = KernelStorage()

class Employee:
    def __init__(self, name: str, role: str, skills: List[str]):
        self.name = name
        self.role = role
        self.skills = skills
        self.domain = "workforce"

    def assign_task(self, task: str):
        emit("TASK_ASSIGNED", "Employee", {"employee": self.name, "task": task})
        
    def save_profile(self):
        storage.save(self.domain, f"{self.name.lower().replace(' ', '_')}.json", {
            "name": self.name,
            "role": self.role,
            "skills": self.skills
        })
