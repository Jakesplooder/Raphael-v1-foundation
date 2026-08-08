from .n8n import N8nConnector
from .comfyui import ComfyUIConnector
from .youtube import YouTubeConnector
from .shopify import ShopifyConnector
from .filesystem import FilesystemConnector

CONNECTOR_REGISTRY = {
    "n8n": N8nConnector,
    "comfyui": ComfyUIConnector,
    "youtube": YouTubeConnector,
    "shopify": ShopifyConnector,
    "filesystem": FilesystemConnector
}
