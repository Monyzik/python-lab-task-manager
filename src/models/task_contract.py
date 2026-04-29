from __future__ import annotations

from collections.abc import AsyncIterable
from typing import Protocol, runtime_checkable, Iterable

from src.models.task import Task


@runtime_checkable
class TaskContract(Protocol):
    def get_tasks(self) -> Iterable[Task]:
        """
        Метод для получения задач из ресурса.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        ...


@runtime_checkable
class AsyncTaskContract(Protocol):

    async def __aenter__(self) -> AsyncTaskContract:
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        ...

    def get_tasks(self) -> AsyncIterable[Task]:
        """
        Метод для асинхронного получения задач из ресурса.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        ...
