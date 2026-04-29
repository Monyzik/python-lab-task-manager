import uuid
from typing import Iterable, Any, AsyncIterable

from src.common.constants import TASK_TEXT_SAMPLE
from src.common.exceptions import InvalidConfigurationForResource
from src.models.task import Task
from random import choice

from src.models.task_mapper import TaskMapper


class GeneratorTaskResource:
    def __init__(self, task_count: int = 1, payload_samples: list = TASK_TEXT_SAMPLE):
        if task_count < 1:
            raise InvalidConfigurationForResource("Количество задач должно быть не меньше 1.")
        self._task_count = task_count
        self._payload_samples = payload_samples
        self._raw = None

    async def __aenter__(self):
        self._raw = self.generate_tasks()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._raw = None

    def generate_tasks(self) -> Iterable[dict[str, Any]]:
        """
        Метод для генерации задач.
        :return: Возвращает список словарей.
        """
        for _ in range(self._task_count):
            yield {"id": uuid.uuid4().hex, "payload": choice(self._payload_samples)}

    async def get_tasks(self) -> AsyncIterable[Task]:
        """
        Метод для получения сгенерированных задач.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        if self._raw is None:
            self._raw = self.generate_tasks()
        for task in self._raw:
            yield TaskMapper.to_task(task)
