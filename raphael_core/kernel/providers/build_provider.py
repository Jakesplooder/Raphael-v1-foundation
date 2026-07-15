import subprocess
import os
import shutil
from typing import Dict, Any, Optional, List
from pathlib import Path

from ..models.builder import BuildExecution, BuildWorkspace
from .workflow.automation_provider import AutomationProvider

class BuildProvider(AutomationProvider):
    """Base class for Build Providers."""
    @property
    def provider_name(self) -> str:
        return "base_builder"

    async def execute_step(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Implements the AutomationProvider interface to work with WorkflowScheduler."""
        func = getattr(self, action, None)
        if callable(func):
            return func(**parameters)
        raise NotImplementedError(f"Action '{action}' is not supported by {self.provider_name}.")

class LocalBuildProvider(BuildProvider):
    """
    Executes builds locally. Expanded to support self-healing coding loops, Git checkpointing,
    and granular file modifications.
    """
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    @property
    def provider_name(self) -> str:
        return "local_builder"

    def _get_path(self, request_id: str) -> Path:
        return self.workspace_root / request_id

    def create_workspace(self, request_id: str) -> Dict[str, Any]:
        path = self._get_path(request_id)
        path.mkdir(parents=True, exist_ok=True)
        return {"status": "success", "workspace_path": str(path)}

    def scaffold(self, request_id: str, framework: str) -> Dict[str, Any]:
        path = self._get_path(request_id)
        if framework == "react":
            self.run_command(request_id, "npx create-react-app .")
        elif framework == "vite":
            self.run_command(request_id, "npx create-vite . --template react-ts")
        elif framework == "fastapi":
            self.run_command(request_id, "mkdir src && touch src/main.py requirements.txt")
        return {"status": "success"}

    def write_file(self, request_id: str, file_path: str, content: str) -> Dict[str, Any]:
        target = self._get_path(request_id) / file_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"status": "success", "file": file_path}

    def write_files(self, request_id: str, files: Dict[str, str]) -> Dict[str, Any]:
        for file_path, content in files.items():
            self.write_file(request_id, file_path, content)
        return {"status": "success", "files_written": len(files)}

    def read_workspace(self, request_id: str) -> Dict[str, Any]:
        # Returns a flat representation of files (in reality, CodeGraphService handles deep scanning)
        path = self._get_path(request_id)
        files = [str(f.relative_to(path)) for f in path.rglob("*") if f.is_file() and ".git" not in str(f) and "node_modules" not in str(f)]
        return {"status": "success", "files": files}

    def run_command(self, request_id: str, command: str) -> Dict[str, Any]:
        path = self._get_path(request_id)
        try:
            result = subprocess.run(
                command, cwd=path, shell=True, capture_output=True, text=True, check=True
            )
            return {"status": "success", "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "exit_code": e.returncode, "stdout": e.stdout, "stderr": e.stderr}

    def build(self, request_id: str, build_command: str = "npm run build") -> Dict[str, Any]:
        return self.run_command(request_id, build_command)

    def test(self, request_id: str, test_command: str = "npm test") -> Dict[str, Any]:
        return self.run_command(request_id, test_command)

    def lint(self, request_id: str, lint_command: str = "npm run lint") -> Dict[str, Any]:
        return self.run_command(request_id, lint_command)

    def format(self, request_id: str, format_command: str = "npm run format") -> Dict[str, Any]:
        return self.run_command(request_id, format_command)

    def git_init(self, request_id: str) -> Dict[str, Any]:
        return self.run_command(request_id, "git init")

    def git_commit(self, request_id: str, message: str) -> Dict[str, Any]:
        self.run_command(request_id, "git add .")
        return self.run_command(request_id, f"git commit -m '{message}'")

    def archive(self, request_id: str) -> Dict[str, Any]:
        path = self._get_path(request_id)
        archive_path = path.parent / f"{request_id}.zip"
        shutil.make_archive(str(path.parent / request_id), 'zip', str(path))
        return {"status": "success", "archive_path": str(archive_path)}

    def destroy_workspace(self, request_id: str) -> Dict[str, Any]:
        path = self._get_path(request_id)
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
        return {"status": "success"}
