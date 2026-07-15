import subprocess
import json
import os
from datetime import datetime
from pathlib import Path

def run_cli(command: str) -> str:
    try:
        result = subprocess.run(["python", "raphael.py"] + command.split(), capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {command}: {e.stderr}")
        return "{}"

def save_json(path: str, data: str):
    try:
        parsed = json.loads(data)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2)
    except json.JSONDecodeError:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)

def main():
    base = Path("tests/golden/api")
    base.mkdir(parents=True, exist_ok=True)
    
    commands = {
        "goals.json": "list-goals",
        "tasks.json": "list-tasks",
        "projects.json": "list-projects",
        "executive.json": "executive-brief",
        "commerce.json": "pod-status",
        "maintenance.json": "self-healing-status"
    }

    print("Capturing Golden Master API Responses...")
    for filename, cmd in commands.items():
        print(f"Running {cmd}...")
        output = run_cli(cmd)
        save_json(str(base / filename), output)

    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "raphael_version": "1.0.0",
        "gateway_commit": "HEAD",
        "rrk_commit": "HEAD",
        "legacy_adapter_commit": "HEAD",
        "endpoints_captured": list(commands.keys()),
        "notes": "Baseline before Epic D legacy migration."
    }
    
    with open("tests/golden/manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print("Golden Master Snapshot complete!")

if __name__ == "__main__":
    main()
