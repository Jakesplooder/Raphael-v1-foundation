from typing import List, Optional, Dict, Any
from ..repositories.project_repository import MarkdownProjectRepository
from ..models.project import Project, ProjectStatus

class ProjectService:
    def __init__(self, repository: MarkdownProjectRepository):
        self.repository = repository
        
    def create_project(self, name: str) -> Project:
        return self.repository.create_project(name)
        
    def list_projects(self) -> List[Project]:
        return self.repository.list_projects()
        
    def get_project(self, slug: str) -> Optional[Project]:
        return self.repository.get_project(slug)
        
    def delete_project(self, slug: str) -> bool:
        return self.repository.delete_project(slug)
        
    def process_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming generic requests, routing to the correct service method.
        """
        action = payload.get("action")
        if action == "create":
            name = payload.get("name")
            if not name:
                return {"error": "name is required"}
            project = self.create_project(name)
            return {"status": "success", "project": project.model_dump()}
        elif action == "list":
            projects = self.list_projects()
            return {"status": "success", "projects": [p.model_dump() for p in projects]}
        elif action == "get":
            slug = payload.get("slug")
            project = self.get_project(slug)
            if not project:
                return {"error": f"Project {slug} not found"}
            return {"status": "success", "project": project.model_dump()}
        return {"error": f"Unknown action: {action}"}
