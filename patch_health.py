import os
import re

path = 'c:/Users/cyber/Downloads/RalphaelOS/api_gateway/legacy_adapter.py'
text = open(path, 'r', encoding='utf-8').read()

http_json_new = """import urllib.request
import json
def http_json(url: str, timeout: float = 0.5) -> tuple[bool, Any]:
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return True, json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return False, str(exc)"""

text = re.sub(r'def http_json.*?return True, \{\}', http_json_new, text, flags=re.DOTALL)
open(path, 'w', encoding='utf-8').write(text)

print("Restored http_json with 0.5s timeout.")
