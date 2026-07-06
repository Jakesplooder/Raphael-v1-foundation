"""Local pandas-backed structured analysis utilities."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from . import legacy


def pandas_status() -> dict[str, Any]:
    available = importlib.util.find_spec("pandas") is not None
    version = ""
    error = ""
    if available:
        try:
            import pandas as pd
            version = str(pd.__version__)
        except Exception as exc:
            available = False
            error = str(exc)
    return {
        "available": available,
        "version": version,
        "status": "READY" if available else "FAILED",
        "error": error or ("" if available else "pandas is not installed in Raphael's Python environment."),
    }


def require_pandas():
    status = pandas_status()
    if not status["available"]:
        raise RuntimeError(status["error"])
    import pandas as pd
    return pd


def analyze_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    pd = require_pandas()
    frame = pd.DataFrame(records)
    if frame.empty:
        return {"rows": 0, "columns": [], "summary": [], "records": []}
    frame = frame.fillna("")
    summary = []
    for column in frame.columns:
        series = frame[column]
        summary.append({
            "column": str(column),
            "non_empty": int(series.astype(str).str.strip().ne("").sum()),
            "unique": int(series.astype(str).nunique()),
        })
    return {
        "rows": int(len(frame)),
        "columns": [str(column) for column in frame.columns],
        "summary": summary,
        "records": frame.to_dict(orient="records"),
    }


def analyze_csv(config: legacy.RaphaelConfig, csv_path: Path) -> dict[str, Any]:
    pd = require_pandas()
    path = legacy.ensure_safe_read_path(csv_path, config)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError("pandas-analyze-csv accepts .csv files only.")
    frame = pd.read_csv(path)
    numeric = frame.select_dtypes(include="number")
    return {
        "path": str(path),
        "rows": int(len(frame)),
        "columns": [str(column) for column in frame.columns],
        "missing_values": {str(key): int(value) for key, value in frame.isna().sum().items()},
        "numeric_summary": numeric.describe().fillna("").to_dict() if not numeric.empty else {},
        "preview": frame.head(20).fillna("").to_dict(orient="records"),
    }
