import asyncio
import logging
import sys

from raphael_core.kernel.providers.commerce.comfyui_adapter import ComfyUIAdapter
from raphael_core.kernel.models.media_generation import GenerationRequest
from raphael_core.kernel.models.commerce import AssetType
import uuid
import time

logging.basicConfig(level=logging.INFO)

async def test_mock():
    adapter = ComfyUIAdapter()
    req = GenerationRequest(
        request_id=str(uuid.uuid4()),
        mission_id="test-mock",
        business_id="test",
        asset_type=AssetType.PNG,
        prompt="A simple mock test",
        metadata={"mode": "mock"}
    )
    
    job = await adapter.submit(req)
    if job.status.value == "failed":
        print("Submit failed")
        sys.exit(1)
        
    while True:
        res = await adapter.retrieve_outputs(job.job_id)
        if res.get("status") == "completed":
            print(f"Mock test completed! Model name: {res.get('model_name')}")
            break
        elif res.get("status") == "failed":
            print("Failed")
            break
        await asyncio.sleep(1)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_mock())
