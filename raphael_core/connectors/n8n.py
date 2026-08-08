from raphael_core.connectors.base_connector import BaseConnector
from typing import Dict, Any, List

class N8nConnector(BaseConnector):
    def metadata(self) -> Dict[str, Any]:
        return {"name": "N8nConnector"}
    def capabilities(self) -> List[Dict[str, Any]]:
        return []
    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return {}
    async def health(self) -> bool:
        return True
