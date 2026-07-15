import os

# Patch legacy_adapter.py
path1 = 'c:/Users/cyber/Downloads/RalphaelOS/api_gateway/legacy_adapter.py'
text1 = open(path1, 'r', encoding='utf-8').read()
text1 = text1.replace('"http://localhost:11434/api/tags"', 'os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434") + "/api/tags"')
open(path1, 'w', encoding='utf-8').write(text1)

# Patch legacy.py
path2 = 'c:/Users/cyber/Downloads/RalphaelOS/raphael_core/legacy.py'
text2 = open(path2, 'r', encoding='utf-8').read()
text2 = text2.replace('"http://" + os.environ.get("OLLAMA_URL", "http://localhost:11434") + ""', 'os.environ.get("OLLAMA_URL", "http://host.docker.internal:11434")')
text2 = text2.replace('"http://localhost:11434"', '"http://host.docker.internal:11434"')
open(path2, 'w', encoding='utf-8').write(text2)

print("Ollama URLs patched successfully!")
