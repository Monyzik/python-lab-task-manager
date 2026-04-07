from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Callable

from src.models.task import Task

Condition = Callable[[Task], bool]


class TaskView(Iterable[Task]):
    def __init__(self, tasks: Iterable[Task], conditions: tuple[Condition, ...] = ()) -> None:
        self._tasks = tasks
        self._conditions = conditions

    def __iter__(self) -> Iterator[Task]:
        for task in self._tasks:
            if all(cond(task) for cond in self._conditions):
                yield task

    def filter(self, condition: Condition) -> TaskView:
        return TaskView(self._tasks, self._conditions + (condition,))
