import os
path = 'api_gateway/legacy_adapter.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('APP_DIR.parent / "config.json"', 'REPO_DIR / "config.json"')
content = content.replace('APP_DIR.parent / "runtime"', 'Path(os.environ.get("RAPHAEL_RUNTIME_DIR", str(REPO_DIR / "runtime")))')
content = content.replace('APP_DIR.parent / "Ralphael"', 'Path(os.environ.get("RAPHAEL_VAULT_DIR", str(REPO_DIR / "Ralphael")))')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
