from typing import Any

from src.models.task import Task


class TaskMapper:
    @staticmethod
    def to_task(data: dict[str, Any]) -> Task:
        task_id = data.get("id")
        payload = data.get("payload")
        return Task(id=task_id, payload=payload)
