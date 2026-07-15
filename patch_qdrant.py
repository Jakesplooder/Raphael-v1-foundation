import re
path = 'c:/Users/cyber/Downloads/RalphaelOS/api_gateway/legacy_adapter.py'
text = open(path, 'r', encoding='utf-8').read()
text = re.sub(r'"qdrant_url": ".*?"', '"qdrant_url": "http://qdrant:6333"', text)
# Also change any direct requests.get("http://localhost:6333") to qdrant:6333 just in case
text = text.replace("http://localhost:6333", "http://qdrant:6333")
open(path, 'w', encoding='utf-8').write(text)
print("Patched qdrant url.")
