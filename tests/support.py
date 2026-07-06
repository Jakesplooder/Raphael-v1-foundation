from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CLI = ROOT / "raphael.py"


class TempRaphael:
    def __init__(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="raphael-tests-")
        self.root = Path(self.temp.name)
        self.vault = self.root / "vault"
        self.runtime = self.root / "runtime"
        self.builder_workspace = self.runtime / "builder" / "workspace"
        self.builder_output = self.runtime / "builder" / "output"
        raw = json.loads((ROOT / "config" / "settings.json").read_text(encoding="utf-8"))
        raw.update(
            {
                "vault_path": str(self.vault),
                "runtime_path": str(self.runtime),
                "builder_workspace": str(self.builder_workspace),
                "builder_output_folder": str(self.builder_output),
                "builder_allowed_write_folders": [str(self.builder_workspace), str(self.builder_output)],
                "approved_read_folders": [str(self.root), "K:/"],
                "approved_write_folders": [str(self.vault), str(self.runtime)],
                "ai_provider": "none",
                "default_ai_provider": "none",
                "qdrant_enabled": False,
                "docker_enabled": False,
                "internet_search_enabled": False,
                "external_execution_enabled": False,
                "n8n_allow_execution": True,
                "n8n_allow_activation": False,
                "n8n_store_credentials": False,
                "n8n_allow_external_calls": False,
            }
        )
        self.config = self.root / "settings.json"
        self.config.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        result = self.run("init")
        if result.returncode != 0:
            raise RuntimeError(result.stderr or result.stdout)

    def close(self) -> None:
        self.temp.cleanup()

    def run(self, *args: str, timeout: int = 90) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(CLI), "--config", str(self.config), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )


def source_hashes() -> dict[str, str]:
    paths = [ROOT / "raphael.py", ROOT / "README.md"]
    paths.extend(sorted((ROOT / "raphael_core").glob("*.py")))
    paths.extend(
        [
            Path("C:/RaphaelOS/dashboard/app.py"),
            Path("C:/RaphaelOS/command_bus.py"),
            Path("C:/RaphaelOS/voice_gateway.py"),
        ]
    )
    result: dict[str, str] = {}
    for path in paths:
        if path.exists():
            result[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result
