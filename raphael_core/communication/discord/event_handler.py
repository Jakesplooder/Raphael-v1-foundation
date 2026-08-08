from typing import List, Dict
from raphael_core.kernel.interfaces import Event
from .gateway import DiscordGateway
from .models import NotificationPolicy
from .embed_builder import EmbedBuilder

class DiscordEventHandler:
    def __init__(self, gateway: DiscordGateway, policies: List[NotificationPolicy]):
        self.gateway = gateway
        self.policies = {p.event_type: p for p in policies if p.enabled}

    async def handle_event(self, event: Event):
        policy = self.policies.get(event.type)
        if not policy:
            return

        # Format message based on event type
        if event.type == "approval_requested":
            message = EmbedBuilder.build_decision_pending(event.payload)
        elif event.type == "experiment_completed":
            message = EmbedBuilder.build_experiment_completed(event.payload)
        elif event.type == "optimization_completed":
            message = EmbedBuilder.build_optimization_completed(event.payload)
        else:
            message = EmbedBuilder.build_generic(event.type, event.payload)

        self.gateway.send(policy.destination_channel, message)
