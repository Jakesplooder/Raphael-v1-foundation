from typing import List
from .models import NotificationPolicy
from .gateway import MockDiscordGateway
from .event_handler import DiscordEventHandler
from .command_router import setup_router
from .approval_manager import ApprovalManager
from raphael_core.kernel.event_bus import global_event_bus
import asyncio

class DiscordBot:
    def __init__(self):
        self.gateway = MockDiscordGateway()
        
        policies = [
            NotificationPolicy(event_type="approval_requested", priority="high", destination_channel="executive-feed"),
            NotificationPolicy(event_type="experiment_completed", priority="medium", destination_channel="experiments"),
            NotificationPolicy(event_type="optimization_completed", priority="low", destination_channel="mission-control"),
        ]
        
        self.event_handler = DiscordEventHandler(self.gateway, policies)
        self.command_router = setup_router()
        self.approval_manager = ApprovalManager()

    def start(self):
        # Subscribe event handler to the event bus
        global_event_bus.subscribe("approval_requested", self.event_handler.handle_event)
        global_event_bus.subscribe("experiment_completed", self.event_handler.handle_event)
        global_event_bus.subscribe("optimization_completed", self.event_handler.handle_event)
