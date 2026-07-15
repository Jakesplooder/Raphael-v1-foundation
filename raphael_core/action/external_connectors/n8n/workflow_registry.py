class WorkflowRegistry:
    """
    Stub for mapping Raphael abstract intents to n8n Workflow IDs.
    """
    def __init__(self):
        self.workflows = {
            "CREATE_SHOPIFY_STORE": "workflow_001",
            "SETUP_CRM": "workflow_002"
        }

    def get_workflow(self, intent: str) -> str:
        return self.workflows.get(intent)
