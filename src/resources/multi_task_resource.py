from typing import Iterable

from src.models.task import Task
from src.models.task_contract import TaskContract


class MultiTaskResource:
    def __init__(self, resources: Iterable[TaskContract]):
        self._resources = resources

    def get_tasks(self) -> Iterable[Task]:
        for resource in self._resources:
            yield from resource.get_tasks()
