import asyncio
from typing import Dict, Any
from .automation_provider import AutomationProvider

class PythonProvider(AutomationProvider):
    """
    Basic AutomationProvider that executes python logic internally.
    Primarily used for testing and safe RRK-native logic before external platforms (e.g. n8n) are integrated.
    """

    @property
    def provider_name(self) -> str:
        return "python_native"

    async def execute_step(self, action: str, parameters: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Executes a python action.
        """
        if action == "echo":
            # Simple dummy action for testing
            return {"status": "success", "message": parameters.get("message", "hello")}
        elif action == "sleep":
            duration = parameters.get("duration", 1)
            await asyncio.sleep(duration)
            return {"status": "success", "waited": duration}
        elif action == "fail":
            raise Exception(f"Intentional failure: {parameters.get('reason', 'unknown')}")
        elif action == "search.searxng":
            import urllib.request
            import urllib.parse
            import json
            import os
            query = parameters.get("query", "")
            searxng_url = os.environ.get("SEARXNG_URL", "http://127.0.0.1:8080").rstrip("/")
            url = f"{searxng_url}/search?{urllib.parse.urlencode({'q': query, 'format': 'json'})}"
            req = urllib.request.Request(url, headers={"User-Agent": "RaphaelOS"})
            try:
                with urllib.request.urlopen(req, timeout=15) as response:
                    data = json.loads(response.read().decode())
                    results = data.get("results", [])[:5]
                    return {"status": "success", "results": results}
            except Exception as e:
                raise Exception(f"SearXNG search failed: {e}")
                
        elif action == "llm.ollama":
            import urllib.request
            import json
            prompt = parameters.get("prompt", "")
            model = parameters.get("model", "llama3.1:latest")
            data = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
            req = urllib.request.Request("http://localhost:11434/api/generate", data=data, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=60) as response:
                    res = json.loads(response.read().decode())
                    return {"status": "success", "response": res.get("response", "")}
            except Exception as e:
                raise Exception(f"Ollama generation failed: {e}")
                
        elif action == "memory.store":
            from raphael_core.kernel.registry import registry
            memory_mgr = registry.get_service("Memory")
            if not memory_mgr:
                raise Exception("MemoryManager not available in registry")
            
            content = parameters.get("content", "")
            if not content:
                raise Exception("Content required for memory.store")
                
            from raphael_core.kernel.models.memory import MemoryType
            record = await memory_mgr.service.store_memory(
                content=content,
                source=parameters.get("source", "Workflow.Mission2"),
                type=MemoryType.FACT,
                importance=0.9
            )
            return {"status": "success", "memory_id": record.id}
            
        elif action == "world_model.create_node":
            from raphael_core.kernel.registry import registry
            world_mgr = registry.get_service("WorldModelService")
            if not world_mgr:
                raise Exception("WorldModel not available in registry")
                
            node_id = parameters.get("node_id", "BRIEF-TEST")
            title = parameters.get("title", "Research Brief")
            desc = parameters.get("description", "")
            
            # Use real source reference path
            import os
            vault_path = os.environ.get("RAPHAEL_DATA_DIR", ".")
            source_ref = os.path.join(vault_path, "00_Raphael", "Briefs", f"{node_id}.md")
            os.makedirs(os.path.dirname(source_ref), exist_ok=True)
            with open(source_ref, "w") as f:
                f.write(desc)
                
            world_mgr.service.add_node("Brief", node_id, title, "WorkflowService", source_ref)
            return {"status": "success", "node_id": node_id, "source_reference": source_ref}
            
        elif action == "commerce.publish":
            import urllib.request
            import urllib.parse
            import json
            import os
            
            # Application-level idempotency via SKU mapping
            idempotency_key = kwargs.get("idempotency_key")
            if not idempotency_key:
                raise Exception("Missing idempotency_key required for commerce.publish")
                
            shop_id = parameters.get("shop_id", "1")
            base_url = f"http://localhost:8082/v3/application/shops/{shop_id}/listings"
            
            # Step 1: SEARCH (Dumb API search by SKU)
            search_url = f"{base_url}?sku={idempotency_key}"
            req = urllib.request.Request(search_url)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                
            if data.get("count", 0) > 0:
                listing_id = data["results"][0]["id"]
                return {"status": "success", "listing_id": listing_id, "idempotent_replay": True, "message": f"Listing already exists with idempotency_key {idempotency_key} - recovering state"}
                
            # Step 2: CREATE
            payload = {
                "title": parameters.get("title", "POD Product"),
                "description": parameters.get("description", ""),
                "sku": idempotency_key
            }
            
            post_data = json.dumps(payload).encode("utf-8")
            post_req = urllib.request.Request(base_url, data=post_data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(post_req) as response:
                res_data = json.loads(response.read().decode())
                
            # Hard crash injection right AFTER the external system successfully commits, 
            # but BEFORE we return to the orchestrator to save the state!
            if parameters.get("hard_kill") is True:
                raise SystemExit("Simulated Hard Crash (SIGKILL) right after external execution!")
                
            return {"status": "success", "listing_id": res_data.get("id")}
            
        else:
            raise NotImplementedError(f"Action '{action}' is not supported by PythonProvider.")
