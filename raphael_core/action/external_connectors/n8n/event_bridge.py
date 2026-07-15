class EventBridge:
    """
    Stub for listening to Raphael's EventBus and triggering external n8n workflows,
    or receiving n8n webhooks and injecting them back into Raphael's reality memory.
    """
    def __init__(self, event_bus):
        self.event_bus = event_bus

    def start_listening(self):
        # Subscribe to REALITY_TRANSFER_APPROVED, etc.
        pass
