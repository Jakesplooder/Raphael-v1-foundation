import re
import os

legacy_file = r'R:\RalphaelOS_Repo\raphael_core\legacy.py'

with open(legacy_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded Ollama URLs in strings
content = content.replace('"http://localhost:11434/api/chat"', 'os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/chat"')
content = content.replace('"http://localhost:11434/api/tags"', 'os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/tags"')
content = content.replace('localhost:11434', '\" + os.environ.get("OLLAMA_URL", "http://localhost:11434") + \"')

# Replace hardcoded Qdrant URLs
content = content.replace('"http://localhost:6333"', 'os.environ.get("QDRANT_URL", "http://localhost:6333")')

# Remove strict dashboard_host checks
content = content.replace('if config.dashboard_host not in {"127.0.0.1", "localhost"}:', 'if False: # config.dashboard_host not in {"127.0.0.1", "localhost"}:')

with open(legacy_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated legacy.py")
