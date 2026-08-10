import logging
from typing import Dict, Any, List
from pathlib import Path

from ..interfaces import ServiceModule, Event, EventType, ModuleHealth
from ..repositories.commerce_repository import CommerceRepository
from ..services.commerce_service import CommerceService
from ..models.commerce import ProductType

logger = logging.getLogger("rrk.managers.commerce")

class CommerceManager(ServiceModule):
    """
    Manages the Commerce subsystem.
    Delegates actual workflow execution to WorkflowPlanManager.
    """
    
    def __init__(self, event_bus, config):
        self.event_bus = event_bus
        self.config = config
        
        os_root = getattr(self.config, "os_root", Path("C:/RaphaelOS"))
        runtime_path = os_root / "CommerceStudio"
        
        self.repository = CommerceRepository(runtime_path)
        self.service = CommerceService(self.repository)
        self._is_initialized = False

    @property
    def name(self) -> str:
        return "CommerceManager"

    @property
    def depends_on(self) -> List[str]:
        return ["EventBus", "WorkflowPlanManager"]

    async def initialize(self) -> None:
        self.event_bus.subscribe(EventType.COMMERCE_PRODUCT_REQUESTED, self._handle_product_requested)
        self._is_initialized = True
        logger.info("CommerceManager initialized.")

    async def _handle_product_requested(self, event: Event):
        # When an agent requests a product, we create it in the repository
        # and then tell WorkflowPlanManager to kick off the Workflow Template
        payload = event.payload
        product = self.service.create_product(
            product_type=ProductType(payload.get("product_type", "pod")),
            name=payload.get("name", "Untitled Product"),
            concept=payload.get("concept", "")
        )
        
        # Publish an intent to start the workflow plan
        self.event_bus.publish(Event(
            source=self.name,
            type=EventType.WORKFLOW_PLAN_REQUESTED,
            payload={
                "name": f"Launch {product.name}",
                "template": self.service.get_commerce_launch_template(product.product_type),
                "context": {"product_id": product.product_id}
            }
        ))
        
        # Dump telemetry to commerce_history
        import os, json
        os.makedirs(f"commerce_history/{product.product_id}", exist_ok=True)
        with open(f"commerce_history/{product.product_id}/request.json", "w") as f:
            json.dump({
                "product_type": product.product_type,
                "name": product.name,
                "concept": product.concept
            }, f, indent=2)

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass
        
    async def shutdown(self) -> None:
        self._is_initialized = False

    def status(self) -> str:
        return "running" if self._is_initialized else "stopped"

    async def heartbeat(self) -> bool | Dict[str, Any]:
        return True

    def health(self) -> ModuleHealth:
        return ModuleHealth.OK

    async def metrics(self) -> dict:
        return {}

    async def handle_request(self, method: str, endpoint: str, payload: Dict[str, Any]) -> Any:
        if method == "POST" and endpoint == "/api/commerce/request":
            # Manual trigger endpoint
            self.event_bus.publish(Event(
                source=self.name,
                type=EventType.COMMERCE_PRODUCT_REQUESTED,
                payload=payload
            ))
            return {"status": "accepted"}
        elif method == "GET" and endpoint == "/api/commerce/products":
            return {"products": [p.model_dump() for p in self.repository.get_products()]}
            
        return {"error": "Unknown endpoint"}
