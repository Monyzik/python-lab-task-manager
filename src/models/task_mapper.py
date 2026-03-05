from typing import Any

from src.common.exceptions import InvalidMappingForTask
from src.models.task import Task


class TaskMapper:
    @staticmethod
    def to_task(data: dict[str, Any]) -> Task:
        """
        Преобразует словарь в объект Task.
        :param data: Словарь, содержащий данные для создания Task.
        :return: Объект Task, созданный на основе данных из словаря.
        """
        if "id" not in data:
            raise InvalidMappingForTask("id")
        if "payload" not in data:
            raise InvalidMappingForTask("payload")
        task_id = data["id"]
        payload = data["payload"]

        return Task(id=task_id, payload=payload)
