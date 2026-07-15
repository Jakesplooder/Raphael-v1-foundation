import os

path = 'c:/RaphaelOS/voice_gateway.py'
text = open(path, 'r', encoding='utf-8').read()

text = text.replace('"http://localhost:11434/api/chat"', 'os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434") + "/api/chat"')
text = text.replace('"Ollama request failed. Confirm Ollama is running on localhost:11434."', 'f"Ollama request failed. Confirm Ollama is running on {os.environ.get(\'OLLAMA_URL\', \'http://host.docker.internal:11434\')}."')
text = text.replace('"http://localhost:11434/api/tags"', 'os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434") + "/api/tags"')

open(path, 'w', encoding='utf-8').write(text)

print("voice_gateway.py patched for Ollama URL.")
