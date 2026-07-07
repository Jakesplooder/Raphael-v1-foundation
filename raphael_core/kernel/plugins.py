import os
import json
import importlib
import sys
from typing import Dict, Any, List

from .observability import ObservabilityLayer
from .state import store
from .registry import registry


class PluginManifest:
    def __init__(self, data: Dict[str, Any]):
        self.name = data.get("name")
        self.version = data.get("version")
        self.author = data.get("author", "Unknown")
        self.permissions = data.get("permissions", [])
        self.dependencies = data.get("dependencies", [])
        self.entrypoint = data.get("entrypoint")
        self.constitution_level = data.get("constitution_level", "untrusted")

    def is_valid(self) -> bool:
        return bool(self.name and self.version and self.entrypoint)


class PluginLoader:
    """
    80.6 Plugin Architecture
    Safely discovers and loads third-party modules based on strict plugin.json manifests.
    """

    def __init__(self, plugin_dir: str = None):
        self.plugin_dir = plugin_dir or os.path.join(os.environ.get("RAPHAEL_DATA_DIR", "."), "plugins")
        self.loaded_plugins: Dict[str, PluginManifest] = {}
        
        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir, exist_ok=True)

    def discover_and_load(self) -> None:
        """Scan the plugins directory for valid manifests and load them."""
        ObservabilityLayer.info("PluginLoader", f"Scanning for plugins in {self.plugin_dir}")
        
        for item in os.listdir(self.plugin_dir):
            plugin_path = os.path.join(self.plugin_dir, item)
            manifest_path = os.path.join(plugin_path, "plugin.json")
            
            if os.path.isdir(plugin_path) and os.path.exists(manifest_path):
                self._load_plugin(plugin_path, manifest_path)

    def _load_plugin(self, plugin_path: str, manifest_path: str) -> None:
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            manifest = PluginManifest(data)
            if not manifest.is_valid():
                ObservabilityLayer.warning("PluginLoader", f"Invalid manifest in {plugin_path}")
                return

            # Note: A real sandbox would evaluate manifest.permissions and manifest.constitution_level here
            # before allowing execution. For RRK v1, we just do strict manifest checking.

            ObservabilityLayer.info("PluginLoader", f"Loading plugin {manifest.name} v{manifest.version}...")
            
            # Add plugin to sys.path to allow import
            if plugin_path not in sys.path:
                sys.path.insert(0, plugin_path)
                
            # Import the entrypoint
            module_name = manifest.entrypoint.replace(".py", "")
            module = importlib.import_module(module_name)
            
            # Expected pattern: plugin entrypoint must have a `register(registry)` function
            if hasattr(module, "register"):
                module.register(registry)
                self.loaded_plugins[manifest.name] = manifest
                store.set_state("PluginLoader", f"plugin_{manifest.name}", "loaded")
                ObservabilityLayer.info("PluginLoader", f"Plugin {manifest.name} successfully registered.")
            else:
                ObservabilityLayer.error("PluginLoader", f"Plugin {manifest.name} missing 'register' function in entrypoint.")

        except Exception as e:
            ObservabilityLayer.error("PluginLoader", f"Failed to load plugin from {plugin_path}: {e}")
