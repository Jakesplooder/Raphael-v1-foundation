import sys
import os
import asyncio

from raphael_core.kernel.dashboard import KernelDashboard
import uvicorn

dashboard = KernelDashboard()
app = dashboard.app

from fastapi import FastAPI, Response
from raphael_core.kernel.event_bus import global_event_bus, Event

@app.on_event("startup")
async def startup_event():
    await global_event_bus.initialize()
    await global_event_bus.start()

@app.on_event("shutdown")
async def shutdown_event():
    await global_event_bus.stop()

@app.post("/api/test-trigger")
async def test_trigger():
    await global_event_bus.publish(Event(type="job_started", source="test", target="all", payload={"job_id": "test_job_1"}))
    await asyncio.sleep(1)
    await global_event_bus.publish(Event(type="job_progress", source="test", target="all", payload={"job_id": "test_job_1", "status": "running"}))
    await asyncio.sleep(1)
    await global_event_bus.publish(Event(type="job_progress", source="test", target="all", payload={"job_id": "test_job_1", "status": "retrying", "retry_count": 1}))
    await asyncio.sleep(1)
    await global_event_bus.publish(Event(type="job_progress", source="test", target="all", payload={"job_id": "test_job_1", "status": "failed", "error": "Simulated unrecoverable error"}))
    
    await global_event_bus.publish(Event(type="job_started", source="test", target="all", payload={"job_id": "test_job_2"}))
    await asyncio.sleep(1)
    await global_event_bus.publish(Event(type="asset_generated", source="test", target="all", payload={"job_id": "test_job_2", "asset_id": "test_img_123"}))
    return {"status": "ok"}

@app.get("/api/asset/{asset_id}")
async def get_asset(asset_id: str):
    if asset_id == "test_img_123":
        png_data = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000a49444154789c63000100000500010d0a2db40000000049454e44ae426082")
        return Response(content=png_data, media_type="image/png")
    return Response(status_code=404)

if __name__ == "__main__":
    if sys.platform == 'win32':
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(app, host="127.0.0.1", port=8788)
