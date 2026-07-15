import re
from pathlib import Path
from typing import List, Dict

class ITaskRepository:
    def get_agent_tasks(self) -> List[Dict[str, str]]:
        raise NotImplementedError

    def get_council_tasks(self) -> List[Dict[str, str]]:
        raise NotImplementedError

class MarkdownTaskRepository(ITaskRepository):
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        
    def _read_text(self, path: Path) -> str:
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""
        
    def _section_value(self, text: str, heading: str) -> str:
        pattern = rf"^## {re.escape(heading)}[ \t]*\r?\n+(.*?)(?=^## |\Z)"
        match = re.search(pattern, text, flags=re.M | re.S)
        return match.group(1).strip() if match else ""

    def _subsection_value(self, text: str, heading: str) -> str:
        pattern = rf"^### {re.escape(heading)}[ \t]*\r?\n+(.*?)(?=^### |\Z)"
        match = re.search(pattern, text, flags=re.M | re.S)
        return match.group(1).strip() if match else ""

    def _parse_agent_markdown_file(self, path: Path) -> Dict[str, str]:
        text = self._read_text(path)
        return {
            "id": self._section_value(text, "Task ID") or path.stem,
            "task": self._section_value(text, "Task") or path.stem,
            "agent": self._section_value(text, "Assigned Agent") or path.parents[1].name,
            "status": self._section_value(text, "Status") or "Unknown",
            "priority": self._section_value(text, "Priority") or "Medium",
            "project": self._section_value(text, "Related Project") or "Unassigned",
            "path": str(path),
        }

    def _parse_council_markdown_file(self, path: Path, council_name: str) -> List[Dict[str, str]]:
        text = self._read_text(path)
        items = []
        for match in re.finditer(r"^## (COUNCIL-[A-Z0-9]+)\s+(.+?)(?=^## COUNCIL-|\Z)", text, flags=re.M | re.S):
            body = match.group(2)
            items.append({
                "id": match.group(1),
                "council": council_name,
                "task": self._subsection_value(body, "Task"),
                "agent": self._subsection_value(body, "Assigned Agent"),
                "status": self._subsection_value(body, "Status") or "Open",
                "priority": self._subsection_value(body, "Priority") or "Normal",
            })
        return items

    def get_agent_tasks(self) -> List[Dict[str, str]]:
        root = self.vault_path / "03_Agents"
        items: List[Dict[str, str]] = []
        if not root.exists():
            return items
        for path in sorted(root.glob("*/Tasks/*.md")):
            items.append(self._parse_agent_markdown_file(path))
        return items

    def get_council_tasks(self) -> List[Dict[str, str]]:
        items: List[Dict[str, str]] = []
        root = self.vault_path / "03_Agents" / "Councils"
        if not root.exists():
            return items
            
        councils = [
            "Executive Council",
            "Product Council",
            "Engineering Council",
            "Operations Council",
            "Research Council",
            "Career Council",
            "Business Council",
            "Commerce Council",
            "Agency Council",
            "Creator Council",
            "Financial Council",
            "Portfolio Council",
            "Governance Council"
        ]
        
        for council in councils:
            path = root / council / "Council Tasks.md"
            if path.exists():
                items.extend(self._parse_council_markdown_file(path, council))
        return items
