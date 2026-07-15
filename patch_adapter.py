import re

path = 'c:/Users/cyber/Downloads/RalphaelOS/api_gateway/legacy_adapter.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix paths
text = re.sub(r'def vault_path\(\) -> Path:.*?return Path\(load_settings\(\)\.get\("vault_path", ".*?"\)\)', 'def vault_path() -> Path:\n    return Path("/app/vault")', text, flags=re.DOTALL)
text = re.sub(r'def runtime_path\(\) -> Path:.*?return Path\(load_settings\(\)\.get\("runtime_path", ".*?"\)\)', 'def runtime_path() -> Path:\n    return Path("/app/runtime")', text, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Patched legacy_adapter.py")
