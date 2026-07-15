import os

path = 'C:/RaphaelOS/command_bus.py'
text = open(path, 'r', encoding='utf-8').read()

if 'import os' not in text:
    text = text.replace('import sys', 'import sys\nimport os')

text = text.replace('RUNTIME_DIR = Path("C:/RaphaelOS")', 'RUNTIME_DIR = Path(os.environ.get("RAPHAEL_RUNTIME_DIR", "C:/RaphaelOS"))')
text = text.replace('SETTINGS_PATH = Path("C:/Users/cyber/Downloads/RalphaelOS/config/settings.json")', 'SETTINGS_PATH = Path(os.environ.get("RAPHAEL_SETTINGS_PATH", "C:/Users/cyber/Downloads/RalphaelOS/config/settings.json"))')

# I also need to make sure the api-gateway passes these environment variables!
open(path, 'w', encoding='utf-8').write(text)

print("command_bus.py patched!")
