import re

source_path = 'C:/RaphaelOS/dashboard/app.py'
target_path = 'c:/Users/cyber/Downloads/RalphaelOS/api_gateway/legacy_adapter.py'

with open(source_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix paths
text = re.sub(r'def vault_path\(\) -> Path:.*?return Path\(load_settings\(\)\.get\("vault_path", ".*?"\)\)', 'def vault_path() -> Path:\n    return Path("/app/vault")', text, flags=re.DOTALL)
text = re.sub(r'def runtime_path\(\) -> Path:.*?return Path\(load_settings\(\)\.get\("runtime_path", ".*?"\)\)', 'def runtime_path() -> Path:\n    return Path("/app/runtime")', text, flags=re.DOTALL)

# Strip FastAPI app definitions
text = re.sub(r'app = FastAPI\(.*?\"static\"\)', '', text, flags=re.DOTALL)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Repatched legacy_adapter.py perfectly.")
