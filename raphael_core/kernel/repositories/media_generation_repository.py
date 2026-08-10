import json
import logging
from pathlib import Path
from typing import List, Optional, Any

from ..models.media_generation import GenerationJob

logger = logging.getLogger("rrk.repositories.media_generation")

class MediaGenerationRepository:
    """Universal repository for persisting media generation jobs (Execution Ledger)."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.jobs_file = self.base_path / "generation_jobs.json"
        
        if not self.jobs_file.exists():
            self._write_json(self.jobs_file, [])

    def _read_json(self, path: Path) -> List[Any]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []

    def _write_json(self, path: Path, data: List[Any]) -> None:
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        temp.replace(path)

    # --- Jobs ---
    def get_jobs(self) -> List[GenerationJob]:
        data = self._read_json(self.jobs_file)
        return [GenerationJob(**row) for row in data]

    def get_job(self, job_id: str) -> Optional[GenerationJob]:
        return next((j for j in self.get_jobs() if j.job_id == job_id), None)

    def save_jobs(self, jobs: List[GenerationJob]) -> None:
        self._write_json(self.jobs_file, [j.model_dump() for j in jobs])

    def upsert_job(self, job: GenerationJob) -> None:
        jobs = self.get_jobs()
        idx = next((i for i, j in enumerate(jobs) if j.job_id == job.job_id), -1)
        if idx >= 0:
            jobs[idx] = job
        else:
            jobs.append(job)
        self.save_jobs(jobs)
