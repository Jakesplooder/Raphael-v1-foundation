import time
import os
import json
from typing import Dict, Any, List
from datetime import datetime

class OSDashboard:
    """
    Global OS Dashboard (Mission Control).
    Tracks active workflows, daemon uptime, crashes, and exposes the Stuck Workflow Detector.
    """
    def __init__(self, trace_file: str = ".system_generated/traces.jsonl"):
        self.trace_file = trace_file
        self.start_time = time.time()
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        self.crashes = 0
        self.dlq_events = 0
        
        # Expected duration per step type (mock configuration)
        self.expected_durations = {
            "commerce.publish": 30, # seconds
            "default": 10
        }

    def _parse_traces(self):
        """Reads the trace file to build the current OS state view."""
        if not os.path.exists(self.trace_file):
            return
            
        with open(self.trace_file, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                    self._process_event(event)
                except json.JSONDecodeError:
                    continue

    def _process_event(self, event: Dict[str, Any]):
        event_type = event.get("event_type")
        payload = event.get("payload", {})
        
        if event_type == "kernel_crash":
            self.crashes += 1
            
        elif event_type == "dlq_event":
            self.dlq_events += 1
            
        elif event_type == "workflow_started":
            wid = payload.get("workflow_id")
            if wid:
                self.active_workflows[wid] = {
                    "step": "Initializing",
                    "step_start_time": time.time(),
                    "action": "default"
                }
                
        elif event_type == "workflow_step_started":
            wid = payload.get("workflow_id")
            if wid and wid in self.active_workflows:
                self.active_workflows[wid]["step"] = payload.get("step_id")
                self.active_workflows[wid]["step_start_time"] = payload.get("timestamp", time.time())
                self.active_workflows[wid]["action"] = payload.get("action", "default")
                
        elif event_type in ("workflow_completed", "workflow_failed"):
            wid = payload.get("workflow_id")
            if wid in self.active_workflows:
                del self.active_workflows[wid]

    def render(self):
        self._parse_traces()
        
        uptime = int(time.time() - self.start_time)
        m, s = divmod(uptime, 60)
        h, m = divmod(m, 60)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==================================================")
        print("           RAPHAEL OS MISSION CONTROL             ")
        print("==================================================")
        print(f"Daemon Uptime      : {h:02d}:{m:02d}:{s:02d}")
        print(f"Crash Restarts     : {self.crashes}")
        print(f"DLQ Events         : {self.dlq_events}")
        print("--------------------------------------------------")
        print("ACTIVE WORKFLOWS:")
        
        if not self.active_workflows:
            print("  (No active workflows)")
        else:
            for wid, data in self.active_workflows.items():
                step = data["step"]
                action = data["action"]
                start_time = data["step_start_time"]
                
                # We need to handle mock timestamps if reading from a file, but for local rendering we'll assume live
                time_in_step = int(time.time() - start_time)
                expected = self.expected_durations.get(action, self.expected_durations["default"])
                
                # Stuck Workflow Detector
                status = "[RUNNING]"
                if time_in_step > (expected * 3):
                    status = "[STUCK!]"
                    
                print(f"  - {wid[:8]} | Step: {step:<15} | Time: {time_in_step}s {status}")
                
        print("==================================================")
