import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any
from ..models.project import Project, ProjectStatus, ProjectHealth, ProjectContext
from ...config import RaphaelConfig
from ...legacy import slugify, infer_project_type, append_unique_line, PROJECT_FILES, update_project_registry

class MarkdownProjectRepository:
    def __init__(self, config: RaphaelConfig):
        self.config = config
        self.projects_dir = self.config.vault / "02_Projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_project_path(self, slug: str) -> Path:
        return self.projects_dir / slug

    def list_projects(self) -> List[Project]:
        projects = []
        if not self.projects_dir.exists():
            return projects
            
        for item in self.projects_dir.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                projects.append(self.get_project(item.name))
        return projects

    def get_project(self, slug: str) -> Optional[Project]:
        path = self._get_project_path(slug)
        if not path.exists() or not path.is_dir():
            return None
            
        # Parse basic metadata from directory
        files = [f.name for f in path.iterdir() if f.is_file() and f.suffix == ".md"]
        
        # In a full implementation we would parse Frontmatter or the Registry for status/health
        return Project(
            name=slug.replace("-", " ").title(),
            slug=slug,
            path=str(path),
            status=ProjectStatus.ACTIVE,
            type=infer_project_type(slug.replace("-", " ")),
            files=files
        )

    def create_project(self, name: str) -> Project:
        slug = slugify(name)
        path = self._get_project_path(slug)
        
        if path.exists():
            return self.get_project(slug)
            
        # Legacy template initialization
        path.mkdir(parents=True, exist_ok=True)
        (path / "Archive").mkdir(parents=True, exist_ok=True)
        
        for filename, template in PROJECT_FILES.items():
            file_path = path / filename
            file_path.write_text(template.format(name=slug), encoding="utf-8")
            
        update_project_registry(self.config, slug)
        
        return self.get_project(slug)
        
    def delete_project(self, slug: str) -> bool:
        path = self._get_project_path(slug)
        if path.exists():
            shutil.rmtree(path)
            return True
        return False
