from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class IRepository(ABC):
    """
    Base abstraction for all data repositories.
    Subsystems must depend ONLY on these interfaces, never directly parsing storage 
    (like Markdown, Postgres, SQLite, Neo4j, etc.).
    """
    pass

# --- Phase D1 Repositories ---

class IProjectRepository(IRepository):
    @abstractmethod
    def list_projects(self) -> List[Dict[str, Any]]: ...
    
    @abstractmethod
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]: ...
    
    @abstractmethod
    def save_project(self, project_id: str, data: Dict[str, Any]) -> bool: ...

class IGoalRepository(IRepository):
    @abstractmethod
    def list_goals(self) -> List[Dict[str, Any]]: ...
    
    @abstractmethod
    def get_goal(self, goal_id: str) -> Optional[Dict[str, Any]]: ...

class ITaskRepository(IRepository):
    @abstractmethod
    def list_tasks(self) -> List[Dict[str, Any]]: ...
    
    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]: ...

# --- Phase D2 Repositories ---

class IExecutiveRepository(IRepository):
    @abstractmethod
    def get_deliberations(self) -> List[Dict[str, Any]]: ...
    
    @abstractmethod
    def get_execution_plans(self) -> List[Dict[str, Any]]: ...

class IAgencyRepository(IRepository):
    @abstractmethod
    def list_agents(self) -> List[Dict[str, Any]]: ...

# --- Phase D3 / D4 Repositories ---

class ICommerceRepository(IRepository):
    @abstractmethod
    def get_revenue_streams(self) -> List[Dict[str, Any]]: ...

class IBlueprintRepository(IRepository):
    @abstractmethod
    def list_blueprints(self) -> List[Dict[str, Any]]: ...

class IAllocationRepository(IRepository):
    @abstractmethod
    def get_allocations(self) -> List[Dict[str, Any]]: ...

# --- Phase D5 Repositories ---

class IMemoryRepository(IRepository):
    @abstractmethod
    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]: ...

class IKnowledgeRepository(IRepository):
    @abstractmethod
    def search_knowledge(self, query: str) -> List[Dict[str, Any]]: ...

class IPatternRepository(IRepository):
    @abstractmethod
    def list_patterns(self) -> List[Dict[str, Any]]: ...
