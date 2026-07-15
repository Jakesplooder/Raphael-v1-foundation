import re

source_path = '/app/runtime/dashboard/app.py'
target_path = '/app/api_gateway/legacy_adapter.py'

with open(source_path, 'r', encoding='utf-8') as f:
    text = f.read()

# patch 1 & 2: Fix paths and strip FastAPI app
text = re.sub(r'def vault_path\(\) -> Path:.*?return Path\(load_settings\(\)\.get\("vault_path", ".*?"\)\)', 'def vault_path() -> Path:\n    return Path("/app/vault")', text, flags=re.DOTALL)
text = re.sub(r'def runtime_path\(\) -> Path:.*?return Path\(load_settings\(\)\.get\("runtime_path", ".*?"\)\)', 'def runtime_path() -> Path:\n    return Path("/app/runtime")', text, flags=re.DOTALL)
text = re.sub(r'app = FastAPI\(.*?\"static\"\)', '', text, flags=re.DOTALL)

# patch 3 & 4: Add DummyApp
dummy_app_new = """
class DummyApp:
    def __init__(self):
        self.routes = []
    def get(self, *args, **kwargs): return lambda f: f
    def post(self, *args, **kwargs): return lambda f: f
    def mount(self, *args, **kwargs): pass
app = DummyApp()
"""
text = re.sub(r'(from fastapi\.staticfiles import StaticFiles)', r'\1\n' + dummy_app_new.strip(), text)

# patch 5: patch http_json
http_json_new = """def http_json(url: str, timeout: int = 3) -> tuple[bool, Any]:
    return True, {}"""
text = re.sub(r'def http_json.*?except Exception as exc:.*?return False, str\(exc\)', http_json_new, text, flags=re.DOTALL)

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("legacy_adapter.py regenerated successfully!")
