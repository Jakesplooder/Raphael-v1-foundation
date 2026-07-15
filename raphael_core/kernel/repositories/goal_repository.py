import json
import logging
from pathlib import Path
from typing import List, Optional, Dict

from ..models.goal import Goal, Objective, Task

logger = logging.getLogger("rrk.repository.goal")

class GoalRepository:
    """Stores goals, objectives, and tasks in a markdown hierarchy."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.vault_path.mkdir(parents=True, exist_ok=True)
        
        # In-memory indices
        self.goals: Dict[str, Goal] = {}
        self.objectives: Dict[str, Objective] = {}
        self.tasks: Dict[str, Task] = {}
        
        self._load_all()
        
    def _read_md(self, path: Path) -> dict:
        """Reads JSON data from a .md file (assuming raw JSON content for now)."""
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.loads(f.read())
            
    def _write_md(self, path: Path, data: dict) -> None:
        """Writes JSON data into a .md file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(data, indent=2))
            
    def _load_all(self):
        for goal_dir in self.vault_path.iterdir():
            if not goal_dir.is_dir():
                continue
                
            goal_file = goal_dir / "goal.md"
            if goal_file.exists():
                try:
                    data = self._read_md(goal_file)
                    g = Goal(**data)
                    self.goals[g.id] = g
                except Exception as e:
                    logger.error(f"Failed to load goal {goal_file}: {e}")
                    
            obj_dir = goal_dir / "objectives"
            if obj_dir.exists():
                for obj_file in obj_dir.glob("*.md"):
                    try:
                        data = self._read_md(obj_file)
                        o = Objective(**data)
                        self.objectives[o.id] = o
                    except Exception as e:
                        logger.error(f"Failed to load objective {obj_file}: {e}")
                        
            task_dir = goal_dir / "tasks"
            if task_dir.exists():
                for task_file in task_dir.glob("*.md"):
                    try:
                        data = self._read_md(task_file)
                        t = Task(**data)
                        self.tasks[t.id] = t
                    except Exception as e:
                        logger.error(f"Failed to load task {task_file}: {e}")
                        
    def save_goal(self, goal: Goal) -> None:
        self.goals[goal.id] = goal
        path = self.vault_path / goal.id / "goal.md"
        self._write_md(path, goal.model_dump())
        
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        return self.goals.get(goal_id)
        
    def save_objective(self, obj: Objective) -> None:
        self.objectives[obj.id] = obj
        path = self.vault_path / obj.goal_id / "objectives" / f"{obj.id}.md"
        self._write_md(path, obj.model_dump())
        
    def get_objective(self, obj_id: str) -> Optional[Objective]:
        return self.objectives.get(obj_id)
        
    def save_task(self, task: Task) -> None:
        self.tasks[task.id] = task
        # Find the goal ID for the task via its objective
        obj = self.get_objective(task.objective_id)
        if obj:
            path = self.vault_path / obj.goal_id / "tasks" / f"{task.id}.md"
            self._write_md(path, task.model_dump())
        else:
            logger.error(f"Cannot save task {task.id}: Objective {task.objective_id} not found.")
            
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
