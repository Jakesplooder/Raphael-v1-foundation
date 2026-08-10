import asyncio
import sys
import os
import subprocess
import time
import json
import httpx
import websockets

async def main():
    print("Starting RRK Server...")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    rrk_proc = subprocess.Popen(
        [sys.executable, "tests/run_rrk_test.py"],
        env=env
    )
    
    print("Starting Gateway Server...")
    env_gw = env.copy()
    env_gw["RRK_URL"] = "http://127.0.0.1:8788"
    gw_proc = subprocess.Popen(
        [sys.executable, "api_gateway/gateway.py"],
        env=env_gw
    )
    
    try:
        # Wait for servers to boot
        print("Waiting for servers to initialize...")
        await asyncio.sleep(5)
        
        async with websockets.connect("ws://127.0.0.1:8000/ws/events") as ws:
            print("Connected to Gateway WebSocket!")
            
            # The Gateway might have already connected to RRK and sent BRIDGE_RECONNECTED,
            # or it might happen after we connect depending on race conditions.
            
            print("Triggering mock generation via test endpoint...")
            async with httpx.AsyncClient() as client:
                resp = await client.post("http://127.0.0.1:8788/api/test-trigger")
                resp.raise_for_status()
                print(f"Trigger response: {resp.json()}")
            
            print("Listening for events...")
            events_received = set()
            start_time = time.time()
            
            # We expect JOB_STARTED, JOB_PROGRESS, ASSET_GENERATED
            while time.time() - start_time < 30:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    # We passed raw strings via broadcast in gateway.
                    payload = json.loads(msg)
                    # Handle raw RRK payload vs Gateway wrapper if any
                    evt_type = payload.get("type", "UNKNOWN")
                    
                    if evt_type not in ["HEARTBEAT", "UNKNOWN"]:
                        print(f"Received Event: {evt_type}")
                        events_received.add(evt_type)
                        
                    if {"job_started", "job_progress", "asset_generated"}.issubset(events_received):
                        print("Successfully received sequence of job events!")
                        break
                except asyncio.TimeoutError:
                    continue
                    
            assert {"job_started", "job_progress", "asset_generated"}.issubset(events_received), "Did not receive all expected events."
            
            print("Killing RRK Server to test disconnect event...")
            rrk_proc.terminate()
            
            # Wait for BRIDGE_DISCONNECTED
            disconnect_received = False
            start_time = time.time()
            while time.time() - start_time < 15:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    payload = json.loads(msg)
                    evt_type = payload.get("type")
                    print(f"Received Event after kill: {evt_type}")
                    if evt_type == "BRIDGE_DISCONNECTED":
                        disconnect_received = True
                        break
                except asyncio.TimeoutError:
                    continue
                    
            print("Restarting RRK Server to test reconnect event...")
            rrk_proc = subprocess.Popen(
                [sys.executable, "tests/run_rrk_test.py"],
                env=env
            )
            
            # Wait for BRIDGE_RECONNECTED
            reconnect_received = False
            start_time = time.time()
            while time.time() - start_time < 20:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    payload = json.loads(msg)
                    evt_type = payload.get("type")
                    if evt_type not in ["HEARTBEAT", "UNKNOWN"]:
                        print(f"Received Event during reconnect phase: {evt_type}")
                    if evt_type == "BRIDGE_RECONNECTED":
                        reconnect_received = True
                        break
                except asyncio.TimeoutError:
                    continue
                    
            assert reconnect_received, "Did not receive BRIDGE_RECONNECTED event."
            
            # Allow RRK to fully start before hitting trigger endpoint
            await asyncio.sleep(2)
            
            print("Triggering mock generation again post-recovery...")
            async with httpx.AsyncClient() as client:
                resp = await client.post("http://127.0.0.1:8788/api/test-trigger")
                resp.raise_for_status()
                print(f"Trigger response: {resp.json()}")
                
            print("Listening for post-recovery events...")
            events_received_post = set()
            start_time = time.time()
            
            while time.time() - start_time < 30:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    payload = json.loads(msg)
                    evt_type = payload.get("type", "UNKNOWN")
                    
                    if evt_type not in ["HEARTBEAT", "UNKNOWN"]:
                        print(f"Received Event (post-recovery): {evt_type}")
                        events_received_post.add(evt_type)
                        
                    if {"job_started", "job_progress", "asset_generated"}.issubset(events_received_post):
                        print("Successfully received sequence of job events post-recovery!")
                        break
                except asyncio.TimeoutError:
                    continue
                    
            assert {"job_started", "job_progress", "asset_generated"}.issubset(events_received_post), "Did not receive all expected events post-recovery."
            
            print("Integration test passed successfully, including reconnect!")

    finally:
        print("Cleaning up processes...")
        if rrk_proc.poll() is None:
            rrk_proc.terminate()
        if gw_proc.poll() is None:
            gw_proc.terminate()
        rrk_proc.wait()
        gw_proc.wait()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
