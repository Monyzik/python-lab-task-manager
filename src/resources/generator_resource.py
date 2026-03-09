import uuid
from typing import Iterable, Any

from src.common.constants import TASK_TEXT_SAMPLE
from src.common.exceptions import InvalidConfigurationForResource
from src.models.task import Task
from random import choice

from src.models.task_mapper import TaskMapper


class GeneratorTaskResource:
    def __init__(self, task_count: int = 1, payload_samples: list = TASK_TEXT_SAMPLE):
        if task_count < 1:
            raise InvalidConfigurationForResource("Количество задач должно быть не меньше 1.")
        self.task_count = task_count
        self.payload_samples = payload_samples

    def generate_tasks(self) -> list[dict[str, Any]]:
        """
        Метод для генерации задач.
        :return: Возвращает список словарей.
        """
        return [{"id": uuid.uuid4().hex, "payload": choice(self.payload_samples)} for _ in range(self.task_count)]

    def get_tasks(self) -> Iterable[Task]:
        """
        Метод для получения сгенерированных задач.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        generated_tasks = self.generate_tasks()
        for task in generated_tasks:
            yield TaskMapper.to_task(task)
