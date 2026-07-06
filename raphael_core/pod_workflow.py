"""Persistent, confirmation-gated POD Studio workflow orchestration."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from . import internet_access, legacy, typography


STAGES = [
    "tool status",
    "internet research",
    "create concept",
    "generate prompts",
    "create generation request",
    "generate images",
    "review batch",
    "create typography",
    "compose design",
    "export SVG",
    "export print-ready PNG",
    "create listing draft",
    "create export package",
]


def workflow_root(config: legacy.RaphaelConfig) -> Path:
    path = config.os_root / "PODStudio" / "workflows"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _workflow_id(request: str) -> str:
    seed = f"{request}|{dt.datetime.now().isoformat()}".encode("utf-8")
    return f"PODFLOW-{dt.datetime.now():%Y%m%d}-{hashlib.sha1(seed).hexdigest()[:8].upper()}"


def _path(config: legacy.RaphaelConfig, workflow_id: str) -> Path:
    clean = workflow_id.strip().upper()
    if not re.fullmatch(r"PODFLOW-\d{8}-[A-F0-9]{8}", clean):
        raise ValueError(f"Invalid POD workflow ID: {workflow_id}")
    return workflow_root(config) / f"{clean}.json"


def _save(config: legacy.RaphaelConfig, state: dict[str, Any]) -> None:
    path = _path(config, state["workflow_id"])
    temp = path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    temp.replace(path)


def _load(config: legacy.RaphaelConfig, workflow_id: str) -> dict[str, Any]:
    path = _path(config, workflow_id)
    if not path.exists():
        raise FileNotFoundError(f"POD workflow not found: {workflow_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def _id_from_path(path: Path, prefix: str) -> str:
    match = re.search(rf"\b({re.escape(prefix)}-[A-Z0-9-]+)\b", path.name, flags=re.I)
    if not match:
        raise RuntimeError(f"Could not extract {prefix} ID from {path}")
    return match.group(1).upper()


def _section(path: Path, heading: str, config: legacy.RaphaelConfig) -> str:
    return legacy.section_value(legacy.read_text_if_exists(path, config, 100000), heading)


def _research_requested(request: str) -> bool:
    lowered = request.lower()
    return any(term in lowered for term in ["research", "trend", "current", "latest", "look up", "search the web", "internet"])


def _model(request: str, config: legacy.RaphaelConfig) -> str:
    lowered = request.lower()
    if "flux" in lowered:
        return "flux"
    if "sdxl" in lowered:
        return "sdxl"
    return config.pod_default_generation_model


def _phrase_from_request(request: str) -> str:
    patterns = [
        r"\btypography(?:\s+saying|\s+with|\s+for)?\s+[\"“']([^\"”']+)[\"”']",
        r"\btext(?:\s+saying|\s+with)?\s+[\"“']([^\"”']+)[\"”']",
        r"\bphrase\s+[\"“']([^\"”']+)[\"”']",
    ]
    for pattern in patterns:
        match = re.search(pattern, request, flags=re.I)
        if match:
            return match.group(1).strip()
    return ""


def _concept_phrase(path: Path, config: legacy.RaphaelConfig) -> str:
    text = _section(path, "Possible Phrases", config)
    for line in text.splitlines():
        if line.strip().startswith("- "):
            return line.strip()[2:].strip()
    return ""


def _progress(state: dict[str, Any], *, started: bool = False) -> dict[str, Any]:
    completed = int(state["completed_stage"])
    next_index = int(state["next_stage"])
    complete = state["status"] in {"completed", "cancelled"}
    next_name = "none" if complete else STAGES[next_index - 1]
    if complete and state["status"] == "completed":
        message = "POD workflow complete. All local outputs are ready for review."
    elif complete:
        message = "POD workflow cancelled. No remaining stages will run."
    else:
        prefix = "POD workflow started." if started else "POD workflow advanced."
        message = f"{prefix} Stage {completed}/13 complete. Next: {next_name}. Say confirm to continue."
    return {
        "workflow_id": state["workflow_id"],
        "status": state["status"],
        "completed_stage": completed,
        "stage_count": 13,
        "current_stage": STAGES[completed - 1] if completed else "",
        "next_stage_number": None if complete else next_index,
        "next_stage": next_name,
        "message": message,
        "ids": state["ids"],
        "outputs": state["outputs"],
    }


def pod_workflow(config: legacy.RaphaelConfig, request: str) -> dict[str, Any]:
    clean = legacy.redact_secrets(request.strip())
    if not clean:
        raise ValueError("POD workflow request cannot be empty.")
    workflow_id = _workflow_id(clean)
    tool_note = legacy.pod_tool_status(config)
    research = _research_requested(clean)
    state = {
        "version": 1,
        "workflow_id": workflow_id,
        "request": clean,
        "created": dt.datetime.now().isoformat(timespec="seconds"),
        "updated": dt.datetime.now().isoformat(timespec="seconds"),
        "status": "awaiting_confirmation",
        "completed_stage": 1,
        "next_stage": 2 if research else 3,
        "research_requested": research,
        "model": _model(clean, config),
        "typography_phrase": _phrase_from_request(clean),
        "ids": {
            "internet_request_id": "",
            "concept_id": "",
            "generation_request_id": "",
            "review_id": "",
            "batch_review_id": "",
            "typography_id": "",
            "composition_id": "",
        },
        "outputs": {
            "tool_status": str(tool_note),
            "research_result": "",
            "niche_score": "",
            "concept_note": "",
            "prompt_note": "",
            "generation_request_note": "",
            "generated_folder": "",
            "selected_image": "",
            "review_note": "",
            "typography_note": "",
            "composition_note": "",
            "svg_path": "",
            "print_png_path": "",
            "listing_draft": "",
            "export_package": "",
        },
        "history": [{"stage": 1, "name": STAGES[0], "status": "completed", "output": str(tool_note)}],
        "last_error": "",
    }
    _save(config, state)
    return _progress(state, started=True)


def _run_stage(config: legacy.RaphaelConfig, state: dict[str, Any], stage: int) -> str:
    request = state["request"]
    ids = state["ids"]
    outputs = state["outputs"]
    if stage == 2:
        result = internet_access.internet_headless_search(config, f"POD research for: {request}")
        ids["internet_request_id"] = result["request_id"]
        analysis = internet_access.internet_analyze_results(config, result["request_id"])
        score = internet_access.internet_niche_score(config, result["request_id"])
        outputs["research_result"] = f"{analysis['rows']} structured source(s)"
        outputs["niche_score"] = str(score["overall_niche_score"])
        return f"Headless SearXNG research saved and scored {score['overall_niche_score']}/100."
    if stage == 3:
        path = legacy.pod_concept(config, request)
        ids["concept_id"] = _id_from_path(path, "PODCON")
        outputs["concept_note"] = str(path)
        state["typography_phrase"] = state["typography_phrase"] or _concept_phrase(path, config)
        return str(path)
    if stage == 4:
        path = legacy.pod_prompt(config, ids["concept_id"])
        outputs["prompt_note"] = str(path)
        return str(path)
    if stage == 5:
        path = legacy.pod_generation_request(config, ids["concept_id"], state["model"])
        ids["generation_request_id"] = _id_from_path(path, "PODGEN")
        outputs["generation_request_note"] = str(path)
        outputs["generated_folder"] = _section(path, "Output Folder", config)
        return str(path)
    if stage == 6:
        folder = Path(outputs["generated_folder"])
        images = sorted(
            item for item in folder.glob("*")
            if item.is_file() and item.suffix.lower() in legacy.POD_IMAGE_EXTENSIONS
        )
        if images:
            path = Path(outputs["generation_request_note"])
        else:
            path = legacy.pod_generate(config, ids["generation_request_id"])
            images = sorted(
                item for item in folder.glob("*")
                if item.is_file() and item.suffix.lower() in legacy.POD_IMAGE_EXTENSIONS
            )
        if not images:
            raise RuntimeError("ComfyUI completed without a usable local image for the next stage.")
        outputs["selected_image"] = str(images[0])
        return str(path)
    if stage == 7:
        path = legacy.pod_review_batch(config, Path(outputs["generated_folder"]))
        ids["batch_review_id"] = _id_from_path(path, "PODBATCH")
        text = legacy.read_text_if_exists(path, config, 100000)
        review_match = re.search(r"\b(PODREV-[A-Z0-9-]+)\b", text, flags=re.I)
        ids["review_id"] = review_match.group(1).upper() if review_match else ids["batch_review_id"]
        outputs["review_note"] = str(path)
        return str(path)
    if stage == 8:
        phrase = state["typography_phrase"] or "ORIGINAL DESIGN"
        path = typography.pod_typography_create(config, phrase)
        ids["typography_id"] = _id_from_path(path, "PODTYPE")
        outputs["typography_note"] = str(path)
        return str(path)
    if stage == 9:
        path = typography.pod_compose_design(
            config, Path(outputs["selected_image"]), ids["typography_id"]
        )
        ids["composition_id"] = _id_from_path(path, "PODCOMP")
        outputs["composition_note"] = str(path)
        return str(path)
    if stage == 10:
        path = typography.pod_svg_export(config, ids["composition_id"])
        outputs["svg_path"] = _section(path, "SVG Export", config)
        return outputs["svg_path"] or str(path)
    if stage == 11:
        path = typography.pod_print_export(config, ids["composition_id"])
        outputs["print_png_path"] = _section(path, "Print PNG", config)
        return outputs["print_png_path"] or str(path)
    if stage == 12:
        path = legacy.pod_listing_draft(config, ids["concept_id"])
        outputs["listing_draft"] = str(path)
        return str(path)
    if stage == 13:
        path = legacy.pod_export_package(config, ids["concept_id"])
        outputs["export_package"] = str(path)
        return str(path)
    raise RuntimeError(f"Unsupported POD workflow stage: {stage}")


def pod_workflow_continue(config: legacy.RaphaelConfig, workflow_id: str) -> dict[str, Any]:
    state = _load(config, workflow_id)
    if state["status"] == "cancelled":
        raise RuntimeError("POD workflow is cancelled.")
    if state["status"] == "completed":
        return _progress(state)
    legacy.pod_confirmation_granted(
        f"Run POD workflow stage {state['next_stage']}/13 ({STAGES[int(state['next_stage']) - 1]})?"
    )
    stage = int(state["next_stage"])
    try:
        output = _run_stage(config, state, stage)
    except Exception as exc:
        state["status"] = "blocked"
        state["last_error"] = str(exc)
        state["updated"] = dt.datetime.now().isoformat(timespec="seconds")
        state["history"].append({"stage": stage, "name": STAGES[stage - 1], "status": "failed", "error": str(exc)})
        _save(config, state)
        raise
    state["completed_stage"] = stage
    state["history"].append({"stage": stage, "name": STAGES[stage - 1], "status": "completed", "output": output})
    next_stage = stage + 1
    if next_stage == 2 and not state["research_requested"]:
        next_stage = 3
    if stage >= 13:
        state["status"] = "completed"
        state["next_stage"] = 14
    else:
        state["status"] = "awaiting_confirmation"
        state["next_stage"] = next_stage
    state["last_error"] = ""
    state["updated"] = dt.datetime.now().isoformat(timespec="seconds")
    _save(config, state)
    return _progress(state)


def pod_workflow_show(config: legacy.RaphaelConfig, workflow_id: str) -> dict[str, Any]:
    return _load(config, workflow_id)


def pod_workflow_status(config: legacy.RaphaelConfig) -> dict[str, Any]:
    rows = []
    for path in sorted(workflow_root(config).glob("PODFLOW-*.json"), key=lambda item: item.stat().st_mtime, reverse=True):
        state = json.loads(path.read_text(encoding="utf-8"))
        rows.append(_progress(state))
    return {"count": len(rows), "workflows": rows}


def pod_workflow_cancel(config: legacy.RaphaelConfig, workflow_id: str) -> dict[str, Any]:
    legacy.pod_confirmation_granted(f"Cancel POD workflow {workflow_id}?")
    state = _load(config, workflow_id)
    state["status"] = "cancelled"
    state["updated"] = dt.datetime.now().isoformat(timespec="seconds")
    state["history"].append({"stage": state["next_stage"], "name": "workflow", "status": "cancelled"})
    _save(config, state)
    return _progress(state)
