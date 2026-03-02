import uuid
from random import choice, randint
from typing import Iterable

from src.models.task import Task


class ApiTaskResource:
    def __init__(self, path: str):
        self.task_count = randint(1, 10)
        self.path = path

    def get_tasks(self) -> Iterable[Task]:
        for _ in range(self.task_count):
            yield Task(id=uuid.uuid4().int, payload=choice(self.payload_samples))
