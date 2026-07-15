from typing import Dict, Any
from ..workflow.automation_provider import AutomationProvider

class EtsyProvider(AutomationProvider):
    @property
    def provider_name(self) -> str:
        return "etsy"
        
    async def execute_step(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("EtsyProvider interface created but execution is not yet implemented.")

class ShopifyProvider(AutomationProvider):
    @property
    def provider_name(self) -> str:
        return "shopify"
        
    async def execute_step(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("ShopifyProvider interface created but execution is not yet implemented.")

class PrintifyProvider(AutomationProvider):
    @property
    def provider_name(self) -> str:
        return "printify"
        
    async def execute_step(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("PrintifyProvider interface created but execution is not yet implemented.")

class SEOProvider(AutomationProvider):
    @property
    def provider_name(self) -> str:
        return "seo"
        
    async def execute_step(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("SEOProvider interface created but execution is not yet implemented.")
