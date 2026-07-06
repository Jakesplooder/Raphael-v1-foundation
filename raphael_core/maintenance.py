"""System diagnostics, repair, backup, and maintenance domain."""

from ._domain import get as __getattr__, names as _names

__all__ = [
    name for name in _names()
    if "system_check" in name.lower()
    or "maintenance" in name.lower()
    or name in {
        "repair_generated_files",
        "backup_system",
        "cleanup_logs",
        "route_check_data",
        "dependency_check_data",
        "config_validation",
    }
]
