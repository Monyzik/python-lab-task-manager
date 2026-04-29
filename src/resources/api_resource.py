import uuid
from random import choice, randint
from typing import Iterable, Any, AsyncIterable

from src.common.constants import TASK_TEXT_SAMPLE
from src.common.exceptions import InvalidApiResponseFormat
from src.models.task import Task
from src.models.task_mapper import TaskMapper


class ApiTaskResource:
    def __init__(self, path: str, payload_samples: list = TASK_TEXT_SAMPLE):
        self._task_count = randint(1, 10)
        self.path = path
        self._payload_samples = payload_samples
        self._raw = None

    async def __aenter__(self):
        self._raw = self.get_tasks_from_api()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._raw = None

    def get_tasks_from_api(self) -> Iterable[dict[str, Any]]:
        """
        Метод для получения задач из API.
        :return: Возвращает список словарей.
        """
        for _ in range(self._task_count):
            yield {"id": uuid.uuid4().hex, "payload": choice(self._payload_samples)}

    async def get_tasks(self) -> AsyncIterable[Task]:
        """
        Метод для получения задач из API и преобразования их в объекты Task.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        if self._raw is None:
            self._raw = self.get_tasks_from_api()
        if not isinstance(self._raw, Iterable):
            raise InvalidApiResponseFormat("Неправильный формат ответа от API. Ожидается список словарей")
        for task in self._raw:
            if not isinstance(task, dict):
                raise InvalidApiResponseFormat("Неправильный формат ответа от API. Ожидается список словарей")
            yield TaskMapper.to_task(task)
