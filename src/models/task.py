from datetime import datetime
from typing import Any

from src.common.exceptions import ImmutableAttributeError
from src.models.descriptors import TypedFieldDescriptor, PriorityFieldDescriptor, CreatedAtFieldDescriptor
from src.models.task_states import TaskStates


class Task:
    state = TypedFieldDescriptor(TaskStates)
    description = TypedFieldDescriptor(str)
    priority = PriorityFieldDescriptor(0, 10)
    created_at = CreatedAtFieldDescriptor()

    def __init__(self, task_id: str, description: str = "", priority: int = 0,
                 state: TaskStates = TaskStates.BACKLOG) -> None:
        self._id = task_id
        self.description = description
        self.priority = priority
        self.state = state
        self._created_at = datetime.now()

    def __setattr__(self, key: str, value: Any) -> None:
        if (key.startswith("_") or key in ["created_at"]) and hasattr(self, key):
            raise ImmutableAttributeError(f"Значение {key} является неизменяемым.")
        super().__setattr__(key, value)

    @property
    def id(self) -> str:
        """
        Идентификатор задачи.
        :return: Возвращает строку - идентификатор задачи.
        """
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        raise ImmutableAttributeError("Идентификатор задачи является неизменяемым.")

    @property
    def is_ready(self) -> bool:
        """
        Значение готова ли задача.
        :return: Возвращает bool значение, готова ли задача.
        """
        return self.state == TaskStates.DONE or self.state == TaskStates.IN_REVIEW

    @property
    def is_important(self) -> bool:
        """
        Значение важная ли задача.
        :return: Возвращает bool значение, важная ли задача.
        """
        return self.priority > 5

    def __repr__(self) -> str:
        return f"Task(id={self.id}, description={self.description}, priority={self.priority}, state={self.state.value})"
