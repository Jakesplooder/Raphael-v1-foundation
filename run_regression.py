import subprocess
import sys

commands = [
    ["py", "raphael.py", "system-check"],
    ["py", "raphael.py", "service-list"],
    ["py", "raphael.py", "service-status"],
    ["py", "raphael.py", "docker-status"],
    ["py", "raphael.py", "build-status"],
    ["py", "raphael.py", "model-status"],
    ["py", "raphael.py", "pod-comfyui-test"]
]

for cmd in commands:
    print(f"\n======================================")
    print(f"Running: {' '.join(cmd)}")
    print(f"======================================")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("ERRORS:")
        print(result.stderr)
        
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(1)
