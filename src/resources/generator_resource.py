import uuid
from typing import Iterable

from src.common.constants import TASK_TEXT_SAMPLE
from src.common.exceptions import InvalidConfigurationForResource
from src.models.task import Task
from random import choice


class GeneratorTaskResource:
    def __init__(self, task_count: int = 1, payload_samples: list = TASK_TEXT_SAMPLE):
        if task_count < 1:
            raise InvalidConfigurationForResource()
        self.task_count = task_count
        self.payload_samples = payload_samples

    def get_tasks(self) -> Iterable[Task]:
        for _ in range(self.task_count):
            yield Task(id=uuid.uuid4().int, payload=choice(self.payload_samples))
