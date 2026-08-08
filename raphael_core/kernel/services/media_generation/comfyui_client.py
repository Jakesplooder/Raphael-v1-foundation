import urllib.request
import urllib.error
import urllib.parse
import json
import logging
import time
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger("kernel.media_generation.comfyui_client")

COMFY_API_URL = "http://127.0.0.1:8188"

class ComfyUIError(Exception):
    pass

class ExpectedTimeoutError(ComfyUIError):
    pass

class WarningTimeoutError(ComfyUIError):
    pass

class ServerUnreachableError(ComfyUIError):
    pass

class WorkflowFailureError(ComfyUIError):
    pass

class RestartDetectedError(ComfyUIError):
    pass

class ComfyUIClient:
    def __init__(self, base_url: str = COMFY_API_URL):
        self.base_url = base_url

    def _make_request(self, endpoint: str, payload: Optional[Dict] = None, timeout: int = 10, is_polling: bool = False) -> Dict:
        url = urllib.parse.urljoin(self.base_url, endpoint)
        req_kwargs = {}
        
        if payload is not None:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        else:
            req = urllib.request.Request(url)
            
        start_time = time.time()
        try:
            response = urllib.request.urlopen(req, timeout=timeout)
            return json.loads(response.read())
        except urllib.error.HTTPError as e:
            if e.code >= 500:
                raise WorkflowFailureError(f"HTTP {e.code}: {e.read().decode('utf-8', 'ignore')}")
            raise ComfyUIError(f"HTTP {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            elapsed = time.time() - start_time
            reason = str(e.reason)
            
            if "Connection refused" in reason or "actively refused" in reason or "No connection could be made" in reason:
                raise ServerUnreachableError("Server unreachable (Connection Refused). Health check required.")
            if "The underlying connection was closed" in reason or "Connection reset" in reason or "RemoteDisconnected" in reason:
                raise RestartDetectedError("Connection reset. Possible OOM or Server restart detected.")
            if "timed out" in reason or "The operation has timed out" in reason:
                if elapsed < 30 and is_polling:
                    raise ExpectedTimeoutError("Expected timeout during polling (Event loop starvation).")
                else:
                    raise WarningTimeoutError("Warning: Timeout exceeded expected threshold.")
            raise ComfyUIError(f"Unexpected network error: {e}")
        except TimeoutError:
            elapsed = time.time() - start_time
            if elapsed < 30 and is_polling:
                raise ExpectedTimeoutError("Expected timeout during polling (Event loop starvation).")
            raise WarningTimeoutError("Warning: Timeout exceeded expected threshold.")
        except Exception as e:
            if "The underlying connection was closed" in str(e):
                 raise RestartDetectedError("Connection reset. Possible OOM or Server restart detected.")
            raise ComfyUIError(f"Unhandled client error: {e}")

    def queue_prompt(self, workflow_json: Dict) -> str:
        """Submits a workflow. DO NOT retry this blindly on timeout."""
        result = self._make_request("/prompt", payload={"prompt": workflow_json}, timeout=15)
        return result.get("prompt_id")

    def get_history(self, prompt_id: str) -> Optional[Dict]:
        """Polls history. Safe to retry on timeouts."""
        result = self._make_request(f"/history/{prompt_id}", timeout=10, is_polling=True)
        if result and prompt_id in result:
            return result[prompt_id]
        return None

    def get_system_stats(self) -> Dict:
        """Fetches health data from ComfyUI."""
        # Short timeout to quickly detect if the event loop is starved vs dead
        return self._make_request("/system_stats", timeout=5)
