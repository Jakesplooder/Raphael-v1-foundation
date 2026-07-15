import json
import os

input_file = "C:/RaphaelOS/launcher/service_registry.json"
output_file = "C:/RaphaelOS/launcher/service_registry.json"

with open(input_file, 'r') as f:
    data = json.load(f)



v2_services = []

for s in data.get("services", []):
    sid = s.get("service_id")
    
    # Policy mapping
    startup = "manual"
    if s.get("auto_start"):
        startup = "auto"
    elif s.get("required"):
        startup = "auto"
    elif not s.get("enabled"):
        startup = "disabled"
    else:
        startup = "on_demand"

    backend = "host_agent"
    if s.get("image") or s.get("container_name"):
        backend = "docker"
    elif not s.get("start_command") and not s.get("image"):
        backend = "internal"

    capabilities = []
    if sid == "comfyui":
        capabilities = ["image_generation", "creative"]
    elif sid == "qdrant":
        capabilities = ["vector_search", "rag"]
    elif sid == "searxng":
        capabilities = ["research"]
    elif sid in ["voice_gateway", "piper"]:
        capabilities = ["voice_synthesis"]
    elif sid == "ollama":
        capabilities = ["llm_inference"]
    elif sid == "dashboard":
        capabilities = ["executive"]

    health_tgt = s.get("health_check_target", "")
    
    v2_service = {
        "identity": {
            "service_id": sid,
            "display_name": s.get("display_name"),
            "category": s.get("category")
        },
        "execution": {
            "backend": backend,
            "start_command": s.get("start_command", ""),
            "working_directory": s.get("working_directory", ""),
            "image": s.get("image", ""),
            "container_name": s.get("container_name", "")
        },
        "policy": {
            "startup": startup,
            "notes": s.get("notes", "")
        },
        "capabilities": capabilities,
        "dependencies": [],
        "health": {
            "type": s.get("health_check_type", "none"),
            "endpoint": health_tgt
        }
    }
    v2_services.append(v2_service)

v2_data = {
    "version": 2,
    "schema_version": "2.0",
    "services": v2_services
}

with open(output_file, 'w') as f:
    json.dump(v2_data, f, indent=2)

print(f"Migrated to {output_file}")
