from collections.abc import Iterable
from typing import Iterator

from src.models.task import Task
from src.models.task_contract import TaskContract


class TaskStream(Iterable[Task]):
    def __init__(self, source: TaskContract) -> None:
        self._source = source.get_tasks()
        self._tasks: list[Task] = []
        self._is_executed: bool = False

    def __iter__(self) -> Iterator[Task]:
        yield from self._tasks

        if self._is_executed:
            return

        for task in self._source:
            self._tasks.append(task)
            yield task

        self._is_executed = True
