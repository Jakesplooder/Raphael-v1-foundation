import os
import asyncio
import httpx
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import time
import json
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gateway")
RRK_URL = os.getenv("RRK_URL", "http://localhost:8788")

# We use httpx.AsyncClient for reverse proxying with a 5-minute timeout for builder/comfy workloads
client = httpx.AsyncClient(base_url=RRK_URL, timeout=300.0)

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await client.aclose()

app = FastAPI(title="Raphael API Gateway", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_dashboard():
    try:
        with open("index_html.txt", "r", encoding="utf-8") as f:
            html = f.read()
        return HTMLResponse(content=html)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading dashboard</h1><p>{e}</p>", status_code=500)

import legacy_adapter

@app.get("/api/health")
async def health_check():
    # Merge RRK health with Legacy Health for Classic View parity
    health_data = legacy_adapter.system_health()
    health_data["gateway_status"] = "online"
    health_data["rrk_url"] = RRK_URL
    return health_data

@app.get("/api/overview")
async def get_overview():
    """
    Feature Resolver (Epic C)
    Acts as the single source of truth, routing features to either RRK or Legacy Adapter
    based on feature_registry.json. Ensures the Classic View schema remains identical.
    """
    start_time = time.time()
    
    # 1. Load the registry
    registry_path = os.path.join(os.path.dirname(__file__), "feature_registry.json")
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)
    except Exception as e:
        logger.error(f"Failed to load feature registry: {e}")
        registry = {}

    # 2. Get baseline from legacy
    legacy_data = legacy_adapter.overview()
    final_data = dict(legacy_data) # Start with legacy as the base map
    
    # 3. Route specific features based on registry
    # This is a translation mapping table (RRK endpoints -> Legacy Keys)
    # The Legacy UI expects very specific keys in the overview payload (e.g., 'tasks', 'goals_active')
    
    # Example Translator for Goals (RRK -> Classic JSON)
    if registry.get("goals") == "rrk":
        try:
            r_start = time.time()
            resp = await client.get(f"{RRK_URL}/api/goals")
            if resp.status_code == 200:
                rrk_goals = resp.json()
                # Translation Adapter
                final_data["goals"] = rrk_goals.get("items", [])
                # Update counts which the legacy UI expects
                final_data["counts"]["goals_active"] = sum(1 for g in final_data["goals"] if g.get("status") == "Active")
                logger.info(f"FeatureResolver: goals -> RRK (Latency: {(time.time() - r_start)*1000:.2f}ms)")
            else:
                logger.error(f"FeatureResolver: goals -> RRK failed ({resp.status_code})")
        except Exception as e:
            logger.error(f"FeatureResolver: goals -> RRK exception: {e}")
            
    # Example Translator for Tasks (RRK -> Classic JSON)
    if registry.get("tasks") == "rrk":
        try:
            r_start = time.time()
            resp = await client.get(f"{RRK_URL}/api/tasks")
            if resp.status_code == 200:
                rrk_tasks = resp.json()
                # Translation Adapter
                final_data["tasks"] = rrk_tasks.get("items", [])
                final_data["counts"]["tasks_open"] = sum(1 for t in final_data["tasks"] if t.get("status") not in {"Done", "Archived"})
                final_data["counts"]["tasks_blocked"] = sum(1 for t in final_data["tasks"] if t.get("status") == "Blocked")
                
                # Fetch council tasks
                resp_ct = await client.get(f"{RRK_URL}/api/council_tasks")
                if resp_ct.status_code == 200:
                    final_data["council_tasks"] = resp_ct.json().get("items", [])
                else:
                    logger.error(f"FeatureResolver: council_tasks -> RRK failed ({resp_ct.status_code})")
                    
                logger.info(f"FeatureResolver: tasks -> RRK (Latency: {(time.time() - r_start)*1000:.2f}ms)")
            else:
                logger.error(f"FeatureResolver: tasks -> RRK failed ({resp.status_code})")
        except Exception as e:
            logger.error(f"FeatureResolver: tasks -> RRK exception: {e}")

    # For everything else, log that it routed to legacy
    # We don't need to actually 'route' it since we copied legacy_data into final_data
    for feature, backend in registry.items():
        if backend == "legacy" and feature not in ["goals", "tasks"]:
            # logger.info(f"FeatureResolver: {feature} -> Legacy")
            pass
            
    logger.info(f"FeatureResolver: /api/overview total latency: {(time.time() - start_time)*1000:.2f}ms")
    return final_data

@app.get("/api/migration/report")
async def get_migration_report():
    try:
        path = os.path.join(os.path.dirname(__file__), "migration_report.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"message": "Migration report not generated yet. Run parity harness."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/migration/parity")
async def get_migration_parity():
    try:
        path = os.path.join(os.path.dirname(__file__), "migration_parity.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"message": "Parity mapping not generated yet."}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/maintenance")
async def get_maintenance():
    try:
        from translators import maintenance_v1
        return maintenance_v1.build_maintenance_payload()
    except Exception as e:
        logger.error(f"Maintenance Translator Error: {e}")
        # Fallback to pure legacy on catastrophic translator failure
        return legacy_adapter.maintenance_data(legacy_adapter.system_health())

# Redirect service actions directly to RRK endpoints
@app.post("/api/services/action")
async def api_services_action(payload: dict = {}):
    action = str(payload.get("action", "")).replace("-", "_")
    service_id = str(payload.get("service_id", ""))
    
    if action in ["start", "stop", "restart"] and service_id:
        try:
            resp = await client.post(f"{RRK_URL}/api/infrastructure/service/{service_id}/{action}")
            if resp.status_code == 200:
                # Return standard legacy action payload
                return {"status": resp.json().get("status"), "service_id": service_id}
        except Exception as e:
            logger.error(f"Failed to route service action to RRK: {e}")
    
    # Fallback to legacy action adapter
    result, status = legacy_adapter.service_bus_action(action, payload)
    from fastapi.responses import JSONResponse
    return JSONResponse(result, status_code=status)

from pydantic import BaseModel
from typing import Any

class ChatPayload(BaseModel):
    message: str = ""
    test_mode: bool = False
    test_session_id: str = ""
    reset_test_session: bool = False
    test_scenario: str = ""

@app.post("/api/chat")
async def api_chat(payload: ChatPayload):
    phrase = payload.message.strip()
    if not phrase:
        return {
            "response": "Type a message for Raphael first.",
            "intent": "empty",
            "command": "",
            "status": "Empty",
            "confirmation_required": False,
            "awaiting_confirmation": False,
        }
    return legacy_adapter.dashboard_chat_response(
        phrase,
        test_mode=payload.test_mode,
        test_session_id=payload.test_session_id,
        reset_test_session=payload.reset_test_session,
        test_scenario=payload.test_scenario
    )

@app.get("/api/raphael/presence")
async def get_presence():
    return legacy_adapter.raphael_presence_data()

@app.post("/api/raphael/presence/action")
async def post_presence_action(payload: dict = {}):
    return legacy_adapter.raphael_presence_action(payload)

@app.get("/api/matrix/departments")
async def get_matrix_departments():
    return legacy_adapter.matrix_department_data()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def proxy_to_rrk(request: Request, path: str):
    """
    Reverse proxy all standard API calls directly to RRK.
    """
    url = f"{RRK_URL}/{path}"
    
    # Exclude internal headers that httpx should manage
    headers = dict(request.headers)
    headers.pop("host", None)
    
    try:
        req_body = await request.body()
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=req_body,
            params=request.query_params
        )
        return StreamingResponse(
            response.aiter_bytes(),
            status_code=response.status_code,
            headers=dict(response.headers)
        )
    except httpx.RequestError as exc:
        return JSONResponse({"error": f"Failed to route request to RRK: {exc}"}, status_code=502)

# Global list of active websocket connections
active_connections = []

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # For now, we just keep the connection alive
            # Later this will receive events from RRK EventBus via Redis or ZeroMQ, or direct bridge
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

