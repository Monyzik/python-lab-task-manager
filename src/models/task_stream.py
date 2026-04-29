from collections.abc import Iterable
from typing import Iterator, AsyncIterable, AsyncIterator

from src.models.task import Task
from src.models.task_contract import AsyncTaskContract


class TaskStream(AsyncIterable[Task]):
    def __init__(self, source: AsyncTaskContract) -> None:
        self._source = source
        self._tasks: list[Task] = []
        self._is_executed: bool = False

    async def __aiter__(self) -> AsyncIterator[Task]:
        for task in self._tasks:
            yield task

        if self._is_executed:
            return

        async for task in self._source.get_tasks():
            self._tasks.append(task)
            yield task

        self._is_executed = True
