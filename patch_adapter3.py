import re

path = 'c:/Users/cyber/Downloads/RalphaelOS/api_gateway/legacy_adapter.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Add a dummy app object so that @app.get decorators don't crash
dummy_app_code = """
class DummyApp:
    def get(self, *args, **kwargs): return lambda f: f
    def post(self, *args, **kwargs): return lambda f: f
    def mount(self, *args, **kwargs): pass
app = DummyApp()
"""

# Insert it after imports
text = re.sub(r'(from fastapi\.staticfiles import StaticFiles)', r'\1\n' + dummy_app_code, text)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Added DummyApp to legacy_adapter.py")
