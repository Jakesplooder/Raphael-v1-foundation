import os

# Patch docker_manager.py
path1 = 'c:/Users/cyber/Downloads/RalphaelOS/raphael_core/docker_manager.py'
text1 = open(path1, 'r', encoding='utf-8').read()
text1 = text1.replace('"health_check": "http://127.0.0.1:6333"', '"health_check": os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")')
open(path1, 'w', encoding='utf-8').write(text1)

# Patch service_manager.py
path2 = 'c:/Users/cyber/Downloads/RalphaelOS/raphael_core/service_manager.py'
text2 = open(path2, 'r', encoding='utf-8').read()
if "import os" not in text2:
    text2 = "import os\n" + text2
text2 = text2.replace('"health_check_target": "http://127.0.0.1:6333"', '"health_check_target": os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")')
open(path2, 'w', encoding='utf-8').write(text2)

# Patch legacy.py (was previously hardcoded to localhost:6333 in some places)
path3 = 'c:/Users/cyber/Downloads/RalphaelOS/raphael_core/legacy.py'
text3 = open(path3, 'r', encoding='utf-8').read()
text3 = text3.replace('os.environ.get("QDRANT_URL", "http://localhost:6333")', 'os.environ.get("QDRANT_URL", "http://qdrant:6333")')
text3 = text3.replace('os.environ.get("QDRANT_URL", "http://127.0.0.1:6333")', 'os.environ.get("QDRANT_URL", "http://qdrant:6333")')
open(path3, 'w', encoding='utf-8').write(text3)

print("Qdrant URLs patched successfully!")
