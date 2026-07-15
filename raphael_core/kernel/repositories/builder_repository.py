import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..models.builder import (
    BuildRequest, BuildClassification, BuildPlan, BuildArtifact, 
    BuildWorkspace, BuildReview, BuildExecution
)

class MarkdownBuildRepository:
    """
    Handles state persistence for the Builder subsystem using Markdown and JSON on the filesystem.
    This repository is agnostic to how the build is executed.
    """
    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir)
        self.requests_dir = self.root_dir / "requests"
        self.classifications_dir = self.root_dir / "classifications"
        self.plans_dir = self.root_dir / "plans"
        self.reviews_dir = self.root_dir / "reviews"
        self.executions_dir = self.root_dir / "executions"
        
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        for d in [self.root_dir, self.requests_dir, self.classifications_dir, 
                  self.plans_dir, self.reviews_dir, self.executions_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def save_request(self, request: BuildRequest) -> None:
        path = self.requests_dir / f"{request.id}.json"
        path.write_text(request.model_dump_json(indent=2), encoding="utf-8")

    def get_request(self, request_id: str) -> Optional[BuildRequest]:
        path = self.requests_dir / f"{request_id}.json"
        if path.exists():
            return BuildRequest.model_validate_json(path.read_text(encoding="utf-8"))
        return None

    def save_classification(self, classification: BuildClassification) -> None:
        path = self.classifications_dir / f"{classification.id}.json"
        path.write_text(classification.model_dump_json(indent=2), encoding="utf-8")

    def save_plan(self, plan: BuildPlan) -> None:
        path = self.plans_dir / f"{plan.id}.json"
        path.write_text(plan.model_dump_json(indent=2), encoding="utf-8")

    def save_review(self, review: BuildReview) -> None:
        path = self.reviews_dir / f"{review.id}.json"
        path.write_text(review.model_dump_json(indent=2), encoding="utf-8")

    def save_execution(self, execution: BuildExecution) -> None:
        path = self.executions_dir / f"{execution.id}.json"
        path.write_text(execution.model_dump_json(indent=2), encoding="utf-8")
