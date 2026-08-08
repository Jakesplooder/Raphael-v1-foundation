from abc import ABC, abstractmethod

class DiscordGateway(ABC):
    @abstractmethod
    def send(self, channel: str, message: str):
        pass

class MockDiscordGateway(DiscordGateway):
    def __init__(self):
        self.message_log = []

    def send(self, channel: str, message: str):
        print(f"\n[Discord:{channel}]")
        print(message)
        print("-" * 40)
        self.message_log.append({"channel": channel, "message": message})
