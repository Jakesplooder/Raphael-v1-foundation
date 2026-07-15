import re

path = 'c:/Users/cyber/Downloads/RalphaelOS/api_gateway/legacy_adapter.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

dummy_app_new = """
class DummyApp:
    def __init__(self):
        self.routes = []
    def get(self, *args, **kwargs): return lambda f: f
    def post(self, *args, **kwargs): return lambda f: f
    def mount(self, *args, **kwargs): pass
app = DummyApp()
"""

# Replace the old DummyApp with the new one
text = re.sub(r'class DummyApp:.*?app = DummyApp\(\)', dummy_app_new.strip(), text, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)
print("Added routes to DummyApp")
