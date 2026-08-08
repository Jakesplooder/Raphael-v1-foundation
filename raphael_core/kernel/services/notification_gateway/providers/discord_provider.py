import os
import urllib.request
import json

class DiscordProvider:
    def __init__(self):
        self.webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "https://discord.com/api/webhooks/1527256018126377040/JFfv6S1RkSQYOnVnrAq4iII2HdbMAlkt-cWEpKjumVexJBAgKpL5y8_wvhYw6ike9rLt")

    def send(self, message: str, channel: str):
        print(f"[DISCORD] -> {channel}")
        print(message)
        print("-" * 40)
        
        if self.webhook_url:
            try:
                data = json.dumps({"content": message}).encode('utf-8')
                req = urllib.request.Request(self.webhook_url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'RaphaelOS'})
                with urllib.request.urlopen(req) as response:
                    pass
            except Exception as e:
                print(f"Failed to send Discord webhook: {e}")
