from raphael_core.connectors.base_connector import BaseConnector
from typing import Dict, Any, List

class FilesystemConnector(BaseConnector):
    def metadata(self) -> Dict[str, Any]:
        return {"name": "FilesystemConnector"}
    def capabilities(self) -> List[Dict[str, Any]]:
        return []
    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {}
    async def health(self) -> bool:
        return True
