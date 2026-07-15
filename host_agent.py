import os
import subprocess
import webbrowser
import platform
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("host-agent")

app = FastAPI(title="Raphael Host Agent")

class ProcessRequest(BaseModel):
    id: str
    command: str
    cwd: Optional[str] = None
    env: Optional[Dict[str, str]] = None

class StopRequest(BaseModel):
    id: str
    
class BrowserRequest(BaseModel):
    url: str

class FolderRequest(BaseModel):
    path: str

class PowerShellRequest(BaseModel):
    script: str

active_processes: Dict[str, subprocess.Popen] = {}

def get_os():
    return platform.system().lower()

@app.post("/process/start")
async def process_start(req: ProcessRequest):
    try:
        env = os.environ.copy()
        if req.env:
            env.update(req.env)
            
        logger.info(f"Starting process {req.id}: {req.command}")
        
        proc = subprocess.Popen(
            req.command,
            shell=True,
            cwd=req.cwd,
            env=env
        )
        active_processes[req.id] = proc
        
        return {"status": "started", "pid": proc.pid, "id": req.id}
    except Exception as e:
        logger.error(f"Failed to start process {req.id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class SyncProcessRequest(BaseModel):
    command: list[str]
    cwd: Optional[str] = None
    log_file: Optional[str] = None

@app.post("/process/run_sync")
async def process_run_sync(req: SyncProcessRequest):
    try:
        proc = subprocess.run(
            req.command,
            cwd=req.cwd,
            capture_output=True,
            text=True
        )
        return {
            "status": "completed",
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process/stop")
async def process_stop(req: StopRequest):
    if req.id not in active_processes:
        raise HTTPException(status_code=404, detail="Process not found or not managed by host agent")
        
    proc = active_processes[req.id]
    try:
        if get_os() == "windows":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)])
        else:
            proc.terminate()
        
        del active_processes[req.id]
        return {"status": "stopped", "id": req.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process/restart")
async def process_restart(req: StopRequest):
    # For restart, we just stop it. The RRK is expected to call start afterwards,
    # or we'd need the command again. Actually, since we don't save the command,
    # we return a failure if we can't restart automatically. 
    # Or RRK just calls stop then start.
    # The user asked for POST /process/restart.
    return {"status": "failed", "detail": "Restart must be orchestrated by RRK (Stop -> Start)"}

@app.get("/process/status")
async def process_status(id: str):
    if id not in active_processes:
        return {"status": "unknown or dead"}
        
    proc = active_processes[id]
    if proc.poll() is None:
        return {"status": "running", "id": id, "pid": proc.pid}
    else:
        del active_processes[id]
        return {"status": "exited", "id": id, "returncode": proc.returncode}

@app.get("/process/pid_status")
async def pid_status(pid: int):
    try:
        import psutil
        p = psutil.Process(pid)
        return {"status": "running", "executable": p.exe(), "create_time": p.create_time()}
    except Exception:
        return {"status": "unknown or dead"}

@app.post("/process/run_background")
async def process_run_background(req: SyncProcessRequest):
    try:
        # DETACHED_PROCESS = 0x00000008, CREATE_NEW_PROCESS_GROUP = 0x00000200
        creationflags = 0x00000008 | 0x00000200 if os.name == "nt" else 0
        
        stdout_dest = subprocess.DEVNULL
        if req.log_file:
            stdout_dest = open(req.log_file, "a")
            
        proc = subprocess.Popen(
            req.command,
            cwd=req.cwd,
            creationflags=creationflags,
            close_fds=True,
            stdin=subprocess.DEVNULL,
            stdout=stdout_dest,
            stderr=subprocess.STDOUT if req.log_file else subprocess.DEVNULL
        )
        return {"status": "started", "pid": proc.pid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/browser/open")
async def browser_open(req: BrowserRequest):
    try:
        webbrowser.open(req.url)
        return {"status": "opened", "url": req.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/folder/open")
async def folder_open(req: FolderRequest):
    try:
        path = req.path
        if not os.path.exists(path):
            raise Exception(f"Path does not exist: {path}")
            
        os_name = get_os()
        if os_name == "windows":
            os.startfile(path)
        elif os_name == "darwin":
            subprocess.run(["open", path])
        else:
            subprocess.run(["xdg-open", path])
            
        return {"status": "opened", "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/docker/run")
async def docker_run(req: ProcessRequest):
    # Just a wrapper over standard process/start, but enforces docker executable
    # In the future this could use the docker SDK
    cmd = f"docker run {req.command}"
    req.command = cmd
    return await process_start(req)

@app.post("/powershell")
async def powershell_run(req: PowerShellRequest):
    if get_os() != "windows":
        raise HTTPException(status_code=400, detail="PowerShell is only natively supported on Windows hosts")
        
    try:
        proc = subprocess.run(
            ["powershell", "-Command", req.script],
            capture_output=True,
            text=True
        )
        return {
            "status": "completed",
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "returncode": proc.returncode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

import urllib.request
import json
import shutil
import psutil

def emit_event(event_type: str, payload: dict):
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8788/api/events",
            data=json.dumps({
                "type": event_type,
                "source": "HostManager",
                "payload": payload
            }).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req, timeout=1)
    except Exception as e:
        logger.warning(f"Failed to emit event {event_type}: {e}")

@app.get("/gpu/status")
async def gpu_status():
    try:
        proc = subprocess.run(["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True)
        if proc.returncode == 0:
            lines = proc.stdout.strip().split('\n')
            gpus = []
            for idx, line in enumerate(lines):
                parts = line.split(',')
                gpus.append({
                    "id": idx,
                    "utilization_percent": int(parts[0].strip()),
                    "memory_used_mb": int(parts[1].strip()),
                    "memory_total_mb": int(parts[2].strip())
                })
            
            # Emit warning if heavily utilized
            if gpus and gpus[0]["utilization_percent"] > 95:
                emit_event("RESOURCE_WARNING", {"gpu_usage": gpus[0]["utilization_percent"], "gpu_id": 0})
                
            return {"status": "ok", "gpus": gpus}
        return {"status": "error", "detail": "nvidia-smi failed"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/docker/status")
async def docker_status():
    try:
        proc = subprocess.run(["docker", "info", "--format", "{{json .}}"], capture_output=True, text=True)
        if proc.returncode == 0:
            return {"status": "ok", "info": json.loads(proc.stdout)}
        return {"status": "error", "detail": "docker not running"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/filesystem/stats")
async def filesystem_stats(path: str = "."):
    try:
        total, used, free = shutil.disk_usage(path)
        gb = 1024 ** 3
        stats = {
            "total_gb": round(total / gb, 2),
            "used_gb": round(used / gb, 2),
            "free_gb": round(free / gb, 2),
            "percent_used": round(used / total * 100, 1)
        }
        
        if stats["percent_used"] > 90:
            emit_event("RESOURCE_WARNING", {"disk_remaining": f"{stats['free_gb']}GB", "path": path})
            
        return {"status": "ok", "stats": stats}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/models/status")
async def models_status():
    try:
        req = urllib.request.urlopen("http://127.0.0.1:11434/api/ps", timeout=2)
        data = json.loads(req.read().decode())
        models = data.get("models", [])
        return {"status": "ok", "loaded_models": models}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/health")
async def health():
    return {"status": "healthy", "os": get_os(), "active_processes": len(active_processes)}

if __name__ == "__main__":
    import uvicorn
    # The host agent runs on a dedicated port natively on the host (e.g. 8789)
    uvicorn.run(app, host="127.0.0.1", port=8789)
