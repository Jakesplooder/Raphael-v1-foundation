"""Stable ID generation helpers."""

from ._compat import exports

__all__ = [
    "make_task_id",
    "make_action_id",
    "make_workflow_id",
    "make_goal_id",
    "make_search_request_id",
    "make_build_id",
    "make_build_classification_id",
    "make_opportunity_id",
    "make_blueprint_id",
    "make_kpi_id",
    "make_finance_entry_id",
    "make_notification_id",
    "make_initiative_id",
    "make_employee_id",
    "make_execution_id",
]
globals().update(exports(__all__))
