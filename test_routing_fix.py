import sys
from pathlib import Path
import json

sys.path.insert(0, r"C:\Users\cyber\Downloads\RalphaelOS")

from api_gateway.legacy_adapter import dashboard_route_agent_ask

class MockVoiceGateway:
    def normalize(self, phrase, wake_word):
        return phrase.lower().strip()
    
    class RouteResult:
        def __init__(self, intent, command, confirmation_required, response):
            self.intent = intent
            self.command = command
            self.confirmation_required = confirmation_required
            self.response = response
            
        def __repr__(self):
            return f"RouteResult(command={self.command})"

voice_config = {"wake_word": "raphael"}
gateway = MockVoiceGateway()

phrases = [
    "Ask operations agent to add 3 servers",
    "Add 3 servers to operations agent",
    "Operations agent add 3 servers"
]

print("Testing Dashboard Route Agent Ask:")
for phrase in phrases:
    result = dashboard_route_agent_ask(phrase, voice_config, gateway)
    print(f"Phrase: '{phrase}'")
    print(f"Result: {result}")
    print("-" * 40)
