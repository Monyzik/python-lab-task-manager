from typing import Protocol, Iterable

from src.models.task import Task

class TaskContract(Protocol):
    def get_tasks(self) -> Iterable[Task]:
        ...
