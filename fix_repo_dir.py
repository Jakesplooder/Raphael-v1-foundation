import os
path = 'api_gateway/legacy_adapter.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('repo_dir = str(APP_DIR.parent)', 'repo_dir = str(REPO_DIR)')
content = content.replace('sys.path.insert(0, repo_dir)', 'sys.path.insert(0, str(REPO_DIR))')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
