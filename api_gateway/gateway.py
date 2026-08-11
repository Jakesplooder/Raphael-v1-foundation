import os
import asyncio
import httpx
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse, HTMLResponse, FileResponse
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

# Global list of active websocket connections
active_connections = set()

async def broadcast_event(event_type: str, payload: dict = None):
    if not active_connections:
        return
    msg = json.dumps({"type": event_type, "payload": payload or {}})
    # Copy set to avoid mutation during iteration
    clients = list(active_connections)
    results = await asyncio.gather(*(client.send_text(msg) for client in clients), return_exceptions=True)
    # Remove disconnected clients
    for client, res in zip(clients, results):
        if isinstance(res, Exception):
            if client in active_connections:
                active_connections.remove(client)

async def sse_consumer():
    url = f"{RRK_URL}/api/events/stream"
    backoff = 1.0
    max_backoff = 30.0
    
    while True:
        try:
            async with client.stream("GET", url, timeout=None) as response:
                response.raise_for_status()
                logger.info("Connected to RRK SSE stream")
                await broadcast_event("BRIDGE_RECONNECTED")
                backoff = 1.0 # Reset backoff on success
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[len("data: "):].strip()
                        if data_str:
                            try:
                                # We broadcast the exact payload parsed from RRK
                                parsed = json.loads(data_str)
                                # The RRK SSE streams {"type": ..., "payload": ...} etc.
                                # Send exactly what came in, avoiding re-wrapping if not needed, 
                                # but gateway broadcast sends {"type": event_type, "payload": payload}.
                                # So let's just forward the raw text!
                                clients = list(active_connections)
                                if clients:
                                    res_list = await asyncio.gather(*(c.send_text(data_str) for c in clients), return_exceptions=True)
                                    for c, r in zip(clients, res_list):
                                        if isinstance(r, Exception):
                                            if c in active_connections:
                                                active_connections.remove(c)
                            except json.JSONDecodeError:
                                pass
        except Exception as e:
            logger.error(f"SSE connection dropped: {e}. Reconnecting in {backoff}s...")
            await broadcast_event("BRIDGE_DISCONNECTED", {"error": str(e)})
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, max_backoff)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(sse_consumer())
    yield
    task.cancel()
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
        
        json_data = await get_overview()
        
        import httpx
        inspector_data = {}
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{RRK_URL}/api/inspector", timeout=5.0)
                if resp.status_code == 200:
                    inspector_data = resp.json()
        except:
            pass
            
        json_data["inspector"] = inspector_data
        
        import json
        html = html.replace("var data = null;", f"var data = {json.dumps(json_data)};")
        
        response = HTMLResponse(content=html)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
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

    t0 = time.time()
    legacy_data = legacy_adapter.overview()
    logger.info(f"FeatureResolver: legacy_adapter.overview took {(time.time() - t0)*1000:.2f}ms")
    final_data = dict(legacy_data) # Start with legacy as the base map
    
    # 3. Route specific features based on registry
    # This is a translation mapping table (RRK endpoints -> Legacy Keys)
    # The Legacy UI expects very specific keys in the overview payload (e.g., 'tasks', 'goals_active')
    
    # 3. Route specific features in parallel with asyncio.gather and strict 1.5s timeout
    rrk_tasks_to_run = []
    if registry.get("goals") == "rrk":
        rrk_tasks_to_run.append(("goals", f"{RRK_URL}/api/goals"))
    if registry.get("tasks") == "rrk":
        rrk_tasks_to_run.append(("tasks", f"{RRK_URL}/api/tasks"))
        rrk_tasks_to_run.append(("council_tasks", f"{RRK_URL}/api/council_tasks"))

    if rrk_tasks_to_run:
        fast_timeout = httpx.Timeout(1.5, connect=1.0)
        async def fetch_rrk(name, url):
            try:
                r_start = time.time()
                resp = await client.get(url, timeout=fast_timeout)
                if resp.status_code == 200:
                    logger.info(f"FeatureResolver: {name} -> RRK (Latency: {(time.time() - r_start)*1000:.2f}ms)")
                    return name, resp.json()
                logger.error(f"FeatureResolver: {name} -> RRK failed ({resp.status_code})")
            except Exception as e:
                logger.error(f"FeatureResolver: {name} -> RRK exception: {e}")
            return name, None

        results = await asyncio.gather(*(fetch_rrk(name, url) for name, url in rrk_tasks_to_run))
        res_map = dict(results)

        if "goals" in res_map and res_map["goals"]:
            final_data["goals"] = res_map["goals"].get("items", [])
            final_data["counts"]["goals_active"] = sum(1 for g in final_data["goals"] if g.get("status") == "Active")

        if "tasks" in res_map and res_map["tasks"]:
            final_data["tasks"] = res_map["tasks"].get("items", [])
            final_data["counts"]["tasks_open"] = sum(1 for t in final_data["tasks"] if t.get("status") not in {"Done", "Archived"})
            final_data["counts"]["tasks_blocked"] = sum(1 for t in final_data["tasks"] if t.get("status") == "Blocked")

        if "council_tasks" in res_map and res_map["council_tasks"]:
            final_data["council_tasks"] = res_map["council_tasks"].get("items", [])

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
        
    try:
        # Route to IntentRouter in RRK
        resp = await client.post(
            f"{RRK_URL}/api/intent", 
            json={"prompt": phrase}
        )
        if resp.status_code == 200:
            data = resp.json()
            return {
                "response": data.get("response", "Processing..."),
                "intent": data.get("intent", "UNKNOWN"),
                "mission_id": data.get("mission_id", ""),
                "route_info": data.get("route_info", {}),
                "command": data.get("command", ""),
                "status": data.get("status", "Processed"),
                "confirmation_required": data.get("confirmation_required", False),
                "awaiting_confirmation": data.get("awaiting_confirmation", False),
            }
        else:
            logger.error(f"Intent routing failed: {resp.status_code} {resp.text}")
    except Exception as e:
        logger.error(f"Intent routing exception: {e}")
        
    # Fallback to legacy
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

@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            # We just keep the connection alive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        if websocket in active_connections:
            active_connections.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

