"""Read-only inspection for allowlisted ComfyUI POD workflow templates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import legacy


TEMPLATES = {
    "flux": "flux_schnell_workflow.json",
    "sdxl": "SDXL_workflow.json",
}


def template_path(config: legacy.RaphaelConfig, template_id: str) -> Path:
    key = template_id.strip().lower()
    if key not in TEMPLATES:
        raise ValueError(f"Unknown POD template `{template_id}`. Allowed templates: flux, sdxl.")
    return config.os_root / "PODStudio" / "templates" / TEMPLATES[key]


def _failed(template_id: str, path: Path, reason: str, **values: Any) -> dict[str, Any]:
    return {
        "template_id": template_id,
        "status": "FAILED",
        "reason": reason,
        "workflow_file": str(path),
        "workflow_file_exists": path.exists(),
        "json_valid": False,
        "checkpoint_node_id": None,
        "checkpoint_filename": "",
        "positive_prompt_node_id": None,
        "negative_prompt_node_id": None,
        "save_image_node_id": None,
        "width_height_node_id": None,
        "width": None,
        "height": None,
        "workflow_type_detected": "unknown",
        **values,
    }


def _node_map(nodes: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for node in nodes:
        node_id = node.get("id")
        if not isinstance(node_id, int):
            raise ValueError("Every workflow node must have an integer id.")
        if node_id in result:
            raise ValueError(f"Duplicate workflow node id: {node_id}")
        result[node_id] = node
    return result


def _links(data: dict[str, Any]) -> list[list[Any]]:
    links = data.get("links")
    if not isinstance(links, list):
        raise ValueError("Workflow links must be an array.")
    for link in links:
        if not isinstance(link, list) or len(link) < 6:
            raise ValueError("Each workflow link must contain source and target node data.")
    return links


def _incoming(links: list[list[Any]], target_id: int, target_slot: int | None = None) -> list[list[Any]]:
    return [
        link for link in links
        if link[3] == target_id and (target_slot is None or link[4] == target_slot)
    ]


def _connected_loaders(nodes: dict[int, dict[str, Any]], links: list[list[Any]]) -> list[dict[str, Any]]:
    loader_ids = {
        node_id for node_id, node in nodes.items()
        if node.get("type") == "CheckpointLoaderSimple"
    }
    source_ids = {int(link[1]) for link in links if isinstance(link[1], int)}
    return [nodes[node_id] for node_id in sorted(loader_ids & source_ids)]


def _sampler(nodes: dict[int, dict[str, Any]]) -> dict[str, Any]:
    samplers = [node for node in nodes.values() if node.get("type") in {"KSampler", "KSamplerAdvanced"}]
    if len(samplers) != 1:
        raise ValueError(f"Expected exactly one sampler node; found {len(samplers)}.")
    return samplers[0]


def _prompt_node(
    nodes: dict[int, dict[str, Any]],
    links: list[list[Any]],
    sampler: dict[str, Any],
    input_name: str,
) -> dict[str, Any]:
    sampler_input = next(
        (item for item in sampler.get("inputs", []) if item.get("name") == input_name),
        None,
    )
    if not sampler_input or sampler_input.get("link") is None:
        raise ValueError(f"Sampler `{input_name}` input is not connected.")
    link_id = sampler_input["link"]
    matching = [link for link in links if link[0] == link_id and link[3] == sampler["id"]]
    if len(matching) != 1:
        raise ValueError(f"Sampler `{input_name}` link {link_id} is invalid or ambiguous.")
    source_id = matching[0][1]
    node = nodes.get(source_id)
    if not node or node.get("type") != "CLIPTextEncode":
        raise ValueError(f"Sampler `{input_name}` must be connected from a CLIPTextEncode node.")
    return node


def _dimensions(nodes: dict[int, dict[str, Any]]) -> tuple[dict[str, Any], int, int]:
    candidates = [
        node for node in nodes.values()
        if node.get("type") in {"EmptyLatentImage", "EmptySD3LatentImage"}
    ]
    if len(candidates) != 1:
        raise ValueError(f"Expected exactly one width/height latent node; found {len(candidates)}.")
    values = candidates[0].get("widgets_values", [])
    if len(values) < 2 or not isinstance(values[0], (int, float)) or not isinstance(values[1], (int, float)):
        raise ValueError("Width/height node does not contain numeric width and height values.")
    return candidates[0], int(values[0]), int(values[1])


def _workflow_type(checkpoint: str, dimension_node: dict[str, Any]) -> str:
    lowered = checkpoint.lower()
    if "flux" in lowered or dimension_node.get("type") == "EmptySD3LatentImage":
        return "flux_schnell"
    if "sd_xl" in lowered or "sdxl" in lowered:
        return "sdxl"
    return "stable_diffusion"


def inspect_template(config: legacy.RaphaelConfig, template_id: str) -> dict[str, Any]:
    key = template_id.strip().lower()
    path = template_path(config, key)
    if not path.exists():
        return _failed(key, path, f"Workflow file does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _failed(key, path, f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    except OSError as exc:
        return _failed(key, path, f"Workflow file could not be read: {exc}")
    if not isinstance(data, dict):
        return _failed(key, path, "Workflow JSON root must be an object.", json_valid=True)
    try:
        raw_nodes = data.get("nodes")
        if not isinstance(raw_nodes, list):
            raise ValueError("Workflow nodes must be an array.")
        nodes = _node_map(raw_nodes)
        links = _links(data)
        sampler = _sampler(nodes)
        positive = _prompt_node(nodes, links, sampler, "positive")
        negative = _prompt_node(nodes, links, sampler, "negative")
        saves = [node for node in nodes.values() if node.get("type") == "SaveImage"]
        if len(saves) != 1:
            raise ValueError(f"Expected exactly one SaveImage node; found {len(saves)}.")
        dimension_node, width, height = _dimensions(nodes)
        loaders = _connected_loaders(nodes, links)
        if len(loaders) != 1:
            raise ValueError(f"Expected exactly one connected CheckpointLoaderSimple node; found {len(loaders)}.")
        loader = loaders[0]
        widget_values = loader.get("widgets_values", [])
        checkpoint = str(widget_values[0]).strip() if widget_values else ""
        if not checkpoint:
            raise ValueError(f"Checkpoint node {loader['id']} has no checkpoint filename.")
        detected = _workflow_type(checkpoint, dimension_node)
        if key == "flux":
            if detected != "flux_schnell":
                raise ValueError(f"Expected Flux Schnell workflow but detected `{detected}` from `{checkpoint}`.")
            for prompt_name, prompt in [("positive", positive), ("negative", negative)]:
                clip_input = next(
                    (item for item in prompt.get("inputs", []) if item.get("name") == "clip"),
                    None,
                )
                if not clip_input or clip_input.get("link") is None:
                    raise ValueError(f"Flux {prompt_name} prompt node {prompt['id']} has no CLIP input link.")
                incoming = [link for link in links if link[0] == clip_input["link"]]
                valid = any(
                    link[1] == loader["id"] and link[2] == 1
                    and link[3] == prompt["id"] and link[4] == 0
                    and link[5] == "CLIP"
                    for link in incoming
                )
                if not valid:
                    raise ValueError(
                        f"Flux checkpoint node {loader['id']} CLIP output is not connected "
                        f"to {prompt_name} prompt node {prompt['id']}."
                    )
        if key == "sdxl" and detected != "sdxl":
            raise ValueError(f"Expected SDXL workflow but detected `{detected}` from `{checkpoint}`.")
    except (ValueError, TypeError, KeyError) as exc:
        return _failed(key, path, str(exc), json_valid=True)
    return {
        "template_id": key,
        "status": "READY",
        "reason": "Workflow structure is valid and required nodes are connected.",
        "workflow_file": str(path),
        "workflow_file_exists": True,
        "json_valid": True,
        "checkpoint_node_id": loader["id"],
        "checkpoint_filename": checkpoint,
        "positive_prompt_node_id": positive["id"],
        "negative_prompt_node_id": negative["id"],
        "save_image_node_id": saves[0]["id"],
        "width_height_node_id": dimension_node["id"],
        "width": width,
        "height": height,
        "workflow_type_detected": detected,
        "flux_clip_connected_to_both_prompts": True if key == "flux" else None,
    }


def template_status(config: legacy.RaphaelConfig) -> dict[str, Any]:
    templates = [inspect_template(config, template_id) for template_id in ("flux", "sdxl")]
    failed = [row for row in templates if row["status"] != "READY"]
    return {
        "status": "FAILED" if failed else "READY",
        "reason": "; ".join(f"{row['template_id']}: {row['reason']}" for row in failed)
        if failed else "All POD workflow templates are ready.",
        "templates": templates,
    }
