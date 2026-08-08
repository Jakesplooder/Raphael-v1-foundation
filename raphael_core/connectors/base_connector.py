from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseConnector(ABC):
    """
    Base class for all Raphael Execution Connectors.
    Implements a strict lifecycle: validate -> prepare -> execute -> verify -> cleanup
    """

    @abstractmethod
    def metadata(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def capabilities(self) -> List[Dict[str, Any]]:
        pass

    async def validate(self, action: str, params: Dict[str, Any]) -> bool:
        return True

    def prepare(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return params

    @abstractmethod
    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def verify(self, action: str, result: Dict[str, Any]) -> bool:
        return True

    def cleanup(self, action: str, result: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    async def health(self) -> bool:
        pass
