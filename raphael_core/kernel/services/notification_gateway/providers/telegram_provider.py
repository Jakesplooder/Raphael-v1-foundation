import os
import urllib.request
import urllib.parse
import json

class TelegramProvider:
    def __init__(self):
        self.bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "8666035008:AAFX8gPHzoWmU99D7Q-R71bAnCY8UErUhFI")
        self.chat_id = os.environ.get("TELEGRAM_CHAT_ID", "6536514456")

    def send(self, message: str):
        print(f"[TELEGRAM] -> CEO Mobile")
        print(message)
        print("-" * 40)
        
        if self.bot_token and self.chat_id != "1":
            try:
                url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
                data = json.dumps({"chat_id": self.chat_id, "text": message}).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'RaphaelOS'})
                with urllib.request.urlopen(req) as response:
                    pass
            except Exception as e:
                print(f"Failed to send Telegram message: {e}")
