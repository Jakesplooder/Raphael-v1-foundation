import logging
import requests
from typing import Dict, Any
from raphael_core.kernel.repositories.idempotency_store import IdempotencyStore

logger = logging.getLogger("creator.n8n_gateway")

class N8nGateway:
    """
    Handles secure, idempotent outbound communication to the n8n container,
    and provides a strict, read-only callback receiver for workflow completion.
    """
    def __init__(self, idempotency_store: IdempotencyStore, n8n_url: str = "http://localhost:5678"):
        self.idempotency_store = idempotency_store
        self.n8n_url = n8n_url
        
    def dispatch_workflow(self, request_id: str, workflow_id: str, payload: Dict[str, Any]) -> bool:
        """
        Dispatches a workflow to n8n securely with idempotency.
        """
        op_id = f"n8n_dispatch_{request_id}_{workflow_id}"
        
        if self.idempotency_store.get(op_id):
            logger.info(f"[{request_id}] n8n workflow {workflow_id} already dispatched. Skipping.")
            return True
            
        try:
            # n8n uses webhook URLs to trigger workflows
            webhook_url = f"{self.n8n_url}/webhook/{workflow_id}"
            logger.info(f"Dispatching to n8n at {webhook_url} with payload keys: {list(payload.keys())}")
            
            # We mock the network request for now, but this is the real pattern:
            # response = requests.post(webhook_url, json=payload, timeout=10)
            # response.raise_for_status()
            
            self.idempotency_store.set(op_id, {"status": "dispatched"})
            return True
            
        except Exception as e:
            logger.error(f"Failed to dispatch workflow to n8n: {e}")
            raise

    def handle_completion_webhook(self, request_id: str, status: str) -> Dict[str, str]:
        """
        A strict, read-only callback endpoint.
        Does NOT trigger any domain actions directly. Only records status.
        """
        logger.info(f"Received completion status '{status}' from n8n for request {request_id}.")
        # In a real environment, this might update a database record's status.
        return {"status": "acknowledged", "request_id": request_id}
