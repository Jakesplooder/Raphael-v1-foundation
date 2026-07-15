import logging
import uuid
from typing import List, Optional

from ..models.goal import Goal, Objective, Task, GoalStatus, TaskStatus, GoalPriority
from ..repositories.goal_repository import GoalRepository

logger = logging.getLogger("rrk.services.goal")

class GoalService:
    """Core CRUD and state management for Goals, Objectives, and Tasks."""
    
    def __init__(self, repository: GoalRepository):
        self.repository = repository
        
    def create_goal(self, title: str, description: str, priority: str = "medium", importance: str = "normal") -> Goal:
        goal_id = f"goal_{uuid.uuid4().hex[:8]}"
        g = Goal(
            id=goal_id,
            title=title,
            description=description,
            priority=GoalPriority(priority),
            importance=importance,
            status=GoalStatus.ACTIVE
        )
        self.repository.save_goal(g)
        return g
        
    def create_objective(self, goal_id: str, title: str) -> Objective:
        obj_id = f"obj_{uuid.uuid4().hex[:8]}"
        o = Objective(
            id=obj_id,
            goal_id=goal_id,
            title=title,
            status=GoalStatus.ACTIVE
        )
        self.repository.save_objective(o)
        return o
        
    def create_task(self, objective_id: str, title: str, description: str) -> Task:
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        t = Task(
            id=task_id,
            objective_id=objective_id,
            title=title,
            description=description,
            status=TaskStatus.CREATED
        )
        self.repository.save_task(t)
        return t
        
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        return self.repository.get_goal(goal_id)
        
    def get_objective(self, obj_id: str) -> Optional[Objective]:
        return self.repository.get_objective(obj_id)
        
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.repository.get_task(task_id)
        
    def assign_task(self, task_id: str, agent_id: str) -> Task:
        t = self.repository.get_task(task_id)
        if not t:
            raise ValueError(f"Task {task_id} not found")
        t.assigned_agent_id = agent_id
        t.status = TaskStatus.ASSIGNED
        self.repository.save_task(t)
        return t
        
    def update_task_status(self, task_id: str, status: TaskStatus) -> Optional[Task]:
        t = self.repository.get_task(task_id)
        if not t:
            return None
        t.status = status
        self.repository.save_task(t)
        return t
        
    def update_objective_status(self, obj_id: str, status: GoalStatus) -> Optional[Objective]:
        o = self.repository.get_objective(obj_id)
        if not o:
            return None
        o.status = status
        self.repository.save_objective(o)
        return o
        
    def update_goal_status(self, goal_id: str, status: GoalStatus) -> Optional[Goal]:
        g = self.repository.get_goal(goal_id)
        if not g:
            return None
        g.status = status
        self.repository.save_goal(g)
        return g
