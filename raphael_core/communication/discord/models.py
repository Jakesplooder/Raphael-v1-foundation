from dataclasses import dataclass, field
from typing import List

@dataclass
class DiscordUser:
    discord_id: str
    role: str
    permissions: List[str] = field(default_factory=list)

    def has_permission(self, permission: str) -> bool:
        return permission in self.permissions or "admin" in self.permissions


@dataclass
class DiscordChannel:
    name: str
    channel_id: str
    purpose: str
    minimum_priority: str = "low"


@dataclass
class NotificationPolicy:
    event_type: str
    priority: str
    destination_channel: str
    enabled: bool = True
