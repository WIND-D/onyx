from datetime import timedelta

from danswer.background.celery.tasks.tasks import (
    tasks_to_schedule as base_tasks_to_schedule,
)

ee_tasks_to_schedule = [
    {
        "name": "sync-external-doc-permissions",
        "task": "check_sync_external_doc_permissions_task",
        "schedule": timedelta(seconds=5),  # TODO: optimize this
    },
    {
        "name": "sync-external-group-permissions",
        "task": "check_sync_external_group_permissions_task",
        "schedule": timedelta(seconds=5),  # TODO: optimize this
    },
    {
        "name": "autogenerate_usage_report",
        "task": "autogenerate_usage_report_task",
        "schedule": timedelta(days=30),  # TODO: change this to config flag
    },
    {
        "name": "check-ttl-management",
        "task": "check_ttl_management_task",
        "schedule": timedelta(hours=1),
    },
]


def get_tasks_to_schedule():
    return ee_tasks_to_schedule + base_tasks_to_schedule
