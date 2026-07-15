import abc
import re
from pathlib import Path
from typing import List, Dict

class IGoalRepository(abc.ABC):
    @abc.abstractmethod
    def get_all_goals(self) -> List[Dict[str, str]]:
        pass

class MarkdownGoalRepository(IGoalRepository):
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def _read_text(self, path: Path) -> str:
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def _subsection_value(self, text: str, header: str) -> str:
        pattern = rf"^### {re.escape(header)}[ \t]*\r?\n+(.*?)(?=^### |\Z)"
        match = re.search(pattern, text, flags=re.M | re.S)
        return match.group(1).strip() if match else ""

    def _meaningful_table_rows(self, text: str) -> List[str]:
        # Rough extraction of markdown table rows
        rows = []
        in_table = False
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("|"):
                in_table = True
                if not set(line.replace("|", "").strip()) <= {"-", ":"}:
                    rows.append(line)
            elif in_table:
                # empty line or non-table line breaks the table
                pass
        return rows

    def _table_cells(self, row: str) -> List[str]:
        return [cell.strip() for cell in row.strip().strip("|").split("|")]

    def parse_subheadings(self, text: str) -> List[Dict[str, str]]:
        items = []
        for match in re.finditer(r"^## (GOAL-[A-Z0-9-]+)\s+(.+?)(?=^## GOAL-|\Z)", text, flags=re.M | re.S):
            body = match.group(2)
            items.append({
                "id": match.group(1),
                "title": self._subsection_value(body, "Title"),
                "status": self._subsection_value(body, "Status"),
                "priority": self._subsection_value(body, "Priority"),
                "milestone": self._subsection_value(body, "Next Milestone"),
            })
        return items

    def parse_table(self, text: str) -> List[Dict[str, str]]:
        goals = []
        for row in self._meaningful_table_rows(text):
            cells = self._table_cells(row)
            if len(cells) >= 9 and cells[0].startswith("GOAL-"):
                goals.append({
                    "id": cells[0],
                    "title": cells[1],
                    "description": cells[2],
                    "status": cells[3],
                    "priority": cells[4],
                    "projects": cells[5],
                    "agents": cells[6],
                    "created": cells[7],
                    "milestone": cells[8],
                })
        return goals

    def normalize(self, table_goals: List[Dict[str, str]], heading_goals: List[Dict[str, str]]) -> List[Dict[str, str]]:
        # Merge them using ID as primary key. Table goals have more fields.
        merged = {}
        for g in heading_goals:
            merged[g["id"]] = g.copy()
        for g in table_goals:
            if g["id"] not in merged:
                merged[g["id"]] = g.copy()
            else:
                # Update existing with table fields
                merged[g["id"]].update(g)
        return list(merged.values())

    def get_all_goals(self) -> List[Dict[str, str]]:
        goals_file = self.data_dir / "vault" / "00_Raphael" / "Goals.md"
        text = self._read_text(goals_file)
        
        heading_goals = self.parse_subheadings(text)
        table_goals = self.parse_table(text)
        
        return self.normalize(table_goals, heading_goals)
