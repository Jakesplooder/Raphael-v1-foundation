"""
Defines the mapping between workflows, required capabilities, and scoring concepts.
Instead of exact string matches, workflows are scored based on the concepts present in the user's intent.
"""

WORKFLOW_CONCEPTS = {
    "ltx_storyboard_factory": {
        "capabilities": ["ltx", "comfyui"],
        "concepts": [
            "video", "movie", "film", "animation", "storyboard", 
            "cinematic", "ltx", "short", "reel", "rap", "battle", "music"
        ]
    },
    "commerce_store_factory": {
        "capabilities": ["n8n"],
        "concepts": [
            "store", "dropshipping", "shopify", "ecommerce", "shop", 
            "business", "products", "sell"
        ]
    },
    "pod_studio": {
        "capabilities": ["comfyui"],
        "concepts": [
            "design", "print on demand", "tshirt", "merch", 
            "apparel", "clothing", "mug"
        ]
    },
    "builder_workflow": {
        "capabilities": ["builder"],
        "concepts": [
            "website", "code", "software", "app", 
            "programming", "script", "develop"
        ]
    }
}
