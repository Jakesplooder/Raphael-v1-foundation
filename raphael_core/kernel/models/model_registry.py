from typing import Dict, Any

MODELS: Dict[str, Dict[str, Any]] = {
    "fast_reasoning": {
        "provider": "ollama",
        "model": "llama3.1:8b",
        "capabilities": [
            "chat",
            "summary",
            "support"
        ],
        "fallbacks": ["qwen3:14b"]
    },
    "strategic_reasoning": {
        "provider": "ollama",
        "model": "qwen3:14b",
        "capabilities": [
            "planning",
            "research",
            "business",
            "documentation"
        ],
        "fallbacks": ["llama3.1:8b", "deepseek-r1:8b"]
    },
    "engineering": {
        "provider": "ollama",
        "model": "qwen2.5-coder:14b",
        "capabilities": [
            "python",
            "javascript",
            "architecture",
            "docker",
            "debugging"
        ],
        "fallbacks": ["deepseek-r1:8b", "llama3.1:8b"]
    },
    "deep_reasoning": {
        "provider": "ollama",
        "model": "deepseek-r1:8b",
        "capabilities": [
            "complex_reasoning",
            "algorithms",
            "math",
            "architecture_review"
        ],
        "fallbacks": ["qwen2.5-coder:14b", "qwen3:14b"]
    },
    "vision": {
        "provider": "ollama",
        "model": "llava",
        "capabilities": [
            "ocr",
            "image_analysis",
            "ui_analysis"
        ],
        "fallbacks": ["qwen2.5vl"]
    },
    "embedding": {
        "provider": "ollama",
        "model": "nomic-embed-text",
        "capabilities": [
            "vector_search",
            "memory_retrieval"
        ],
        "fallbacks": ["bge-large"]
    }
}
