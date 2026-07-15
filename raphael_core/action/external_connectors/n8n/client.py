class N8NClient:
    """
    Stub for the future n8n automation client.
    Will handle webhook invocations and REST API interactions.
    """
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

    def trigger_workflow(self, workflow_id: str, payload: dict):
        # Implementation reserved for D24
        pass
