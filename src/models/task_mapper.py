import uuid
from typing import Any

from src.common.exceptions import InvalidMappingForTask, InvalidMappingType
from src.models.task import Task
from src.models.task_states import TaskStates


class TaskMapper:
    @staticmethod
    def to_task(data: dict[str, Any]) -> Task:
        """
        Преобразует словарь в объект Task.
        :param data: Словарь, содержащий данные для создания Task.
        :return: Объект Task, созданный на основе данных из словаря.
        """
        if "payload" not in data:
            raise InvalidMappingForTask("payload")

        task_id = data.get("id", uuid.uuid4().hex)
        payload = data.get("payload", None)

        if not isinstance(payload, dict):
            raise InvalidMappingType("Payload должен быть словарем.")

        if not isinstance(task_id, str):
            raise InvalidMappingType("Id задачи должен быть строкой.")

        description = payload.get("description", "")
        priority = payload.get("priority", 0)

        state = payload.get("state", TaskStates.BACKLOG)
        if isinstance(state, str):
            state = TaskStates(state)

        return Task(task_id=task_id, description=description, priority=priority, state=state)
