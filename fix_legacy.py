import os
path = 'api_gateway/legacy_adapter.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
# Find where APP_DIR = ... is
start_idx = content.find('APP_DIR = Path(__file__).resolve().parent')

top = content[:start_idx]
# clean duplicates in top
top = re.sub(r'import json\nimport logging\nimport os\nimport re\nimport sys\nfrom collections\.abc import Generator\nfrom pathlib import Path\nfrom typing import Any\n\n', '', top)

rest = content[start_idx:]
end_idx = rest.find('DASHBOARD_CHAT_LOG =')

new_logic = '''APP_DIR = Path(__file__).resolve().parent
if "RAPHAEL_CLI_PATH" in os.environ:
    REPO_DIR = Path(os.environ["RAPHAEL_CLI_PATH"]).parent
else:
    REPO_DIR = APP_DIR.parent

if str(REPO_DIR) not in sys.path:
    sys.path.insert(0, str(REPO_DIR))

CONFIG_PATH = Path(os.environ.get("RAPHAEL_CONFIG_PATH", str(REPO_DIR / "config.json")))
'''

final_content = top + new_logic + rest[end_idx:]

with open(path, 'w', encoding='utf-8') as f:
    f.write(final_content)
