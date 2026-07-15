from typing import List, Dict
from ..repositories.tasks import ITaskRepository

class TaskService:
    def __init__(self, repository: ITaskRepository):
        self.repository = repository

    def get_tasks(self, scope: str = "all") -> List[Dict[str, str]]:
        if scope == "agent":
            return self.repository.get_agent_tasks()
        elif scope == "council":
            return self.repository.get_council_tasks()
        elif scope == "all":
            return self.repository.get_agent_tasks() + self.repository.get_council_tasks()
        else:
            raise ValueError(f"Unknown scope: {scope}. Must be 'agent', 'council', or 'all'.")
