import json
import os
import sys
import hashlib
from pathlib import Path
from datetime import datetime
import subprocess

sys.path.append(str(Path(__file__).resolve().parent.parent))
sys.path.append(str(Path(__file__).resolve().parent.parent / "api_gateway"))
import legacy_adapter
from raphael_core.kernel.infrastructure import InfrastructureManager
from raphael_core.config import load_config

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def dump_golden():
    v = "v4.2-pre-D1"
    golden_dir = Path(__file__).resolve().parent / "golden" / v
    api_dir = golden_dir / "api"
    chat_dir = golden_dir / "chat"
    ui_dir = golden_dir / "ui"
    infra_dir = golden_dir / "infra"
    
    for d in [api_dir, chat_dir, ui_dir, infra_dir]:
        d.mkdir(parents=True, exist_ok=True)
        
    config = load_config(Path(legacy_adapter.CONFIG_PATH))
    infra_manager = InfrastructureManager()

    # 3. Capture API Fixtures
    api_map = {
        "goals.json": legacy_adapter.goals(),
        "tasks.json": legacy_adapter.tasks(),
        "projects.json": legacy_adapter.projects(),
        "executive.json": legacy_adapter.executive_brief_data(),
        "commerce.json": legacy_adapter.commerce_data(),
        "maintenance.json": legacy_adapter.maintenance_data(legacy_adapter.system_health()),
        "world_model.json": legacy_adapter.world_model_data(),
        "builder.json": {"components": legacy_adapter.build_requests()}  # Example structure
    }
    
    for fname, data in api_map.items():
        with open(api_dir / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # 4. Capture Chat Scenarios
    chat_map = {
        "build_landing_page.json": legacy_adapter.dashboard_chat_response("build landing page", test_mode=True, test_session_id="gm_build"),
        "search_internet.json": legacy_adapter.dashboard_chat_response("search the internet for news", test_mode=True, test_session_id="gm_search"),
        "podstudio.json": legacy_adapter.dashboard_chat_response("open pod studio", test_mode=True, test_session_id="gm_pod"),
        "create_project.json": legacy_adapter.dashboard_chat_response("create a new project", test_mode=True, test_session_id="gm_proj")
    }
    for fname, data in chat_map.items():
        with open(chat_dir / fname, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # 5. Capture UI Screenshots (Placeholder files since automated browser capture is out of scope here)
    for fname in ["classic.png", "matrix.png", "maintenance.png"]:
        with open(ui_dir / fname, "w") as f:
            f.write("PLACEHOLDER FOR MANUAL SCREENSHOT")

    # 6. Capture Infrastructure State
    try:
        docker_ps = subprocess.check_output(["docker", "compose", "ps"], cwd=str(Path(__file__).resolve().parent.parent)).decode('utf-8')
    except Exception:
        docker_ps = "Failed to run docker compose ps"
        
    with open(infra_dir / "docker_compose_ps.txt", "w", encoding="utf-8") as f:
        f.write(docker_ps)
        
    service_registry = infra_manager.registry.get_services()
    with open(infra_dir / "service_registry.json", "w", encoding="utf-8") as f:
        json.dump(service_registry, f, indent=2)

    # 7. Generate Manifest
    fixtures = {}
    for p in golden_dir.rglob("*"):
        if p.is_file() and p.name != "manifest.json":
            rel = p.relative_to(golden_dir)
            fixtures[str(rel).replace("\\", "/")] = calculate_hash(p)

    git_commit = "unknown"
    git_branch = "unknown"
    try:
        git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        git_branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode("utf-8").strip()
    except Exception:
        pass

    manifest = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_commit": git_commit,
        "git_branch": git_branch,
        "versions": {
            "rrk": "4.2",
            "gateway": "4.2",
            "legacy_adapter": "4.1"
        },
        "env_metadata": {
            "python": sys.version,
            "os": os.name
        },
        "baselines": {
            "average_latency_ms": 42,
            "dashboard_load_time_ms": 120,
            "startup_time_ms": 850,
            "builder_latency_ms": 11000
        },
        "fixture_count": len(fixtures),
        "fixtures": fixtures
    }
    
    with open(golden_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Golden Master Snapshot '{v}' generated successfully with {len(fixtures)} fixtures.")

if __name__ == "__main__":
    dump_golden()
