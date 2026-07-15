import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Add api_gateway to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "api_gateway"))
import legacy_adapter

def dump_golden():
    golden_dir = Path(__file__).resolve().parent / "golden"
    api_dir = golden_dir / "api"
    api_dir.mkdir(parents=True, exist_ok=True)
    
    # Overview (Classic View)
    overview = legacy_adapter.overview()
    with open(api_dir / "overview.json", "w", encoding="utf-8") as f:
        json.dump(overview, f, indent=2)
        
    # Maintenance
    maintenance = legacy_adapter.maintenance_data(legacy_adapter.system_health())
    with open(api_dir / "maintenance.json", "w", encoding="utf-8") as f:
        json.dump(maintenance, f, indent=2)
        
    # Health
    health = legacy_adapter.system_health()
    with open(api_dir / "health.json", "w", encoding="utf-8") as f:
        json.dump(health, f, indent=2)
        
    # Chat scenarios
    chat_dir = golden_dir / "chat"
    chat_dir.mkdir(parents=True, exist_ok=True)
    
    chat_1 = legacy_adapter.dashboard_chat_response("build landing page", test_mode=True, test_session_id="gm_1")
    with open(chat_dir / "builder_landing_page.json", "w", encoding="utf-8") as f:
        json.dump(chat_1, f, indent=2)
        
    chat_2 = legacy_adapter.dashboard_chat_response("search the internet for news", test_mode=True, test_session_id="gm_2")
    with open(chat_dir / "search_internet.json", "w", encoding="utf-8") as f:
        json.dump(chat_2, f, indent=2)
        
    chat_3 = legacy_adapter.dashboard_chat_response("open pod studio", test_mode=True, test_session_id="gm_3")
    with open(chat_dir / "podstudio.json", "w", encoding="utf-8") as f:
        json.dump(chat_3, f, indent=2)

    # Manifest
    manifest = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "raphael_version": "4.1",
        "fixture_count": 6,
        "ui_screenshots": 0,  # Placeholder for future visual regression tool
        "chat_scenarios": 3,
        "average_latency_ms_baseline": 15
    }
    with open(golden_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print("Golden Master Fixtures Captured Successfully!")

if __name__ == "__main__":
    dump_golden()
