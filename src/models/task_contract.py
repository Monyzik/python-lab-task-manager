from typing import Protocol, Iterable, runtime_checkable

from src.models.task import Task


@runtime_checkable
class TaskContract(Protocol):
    def get_tasks(self) -> Iterable[Task]:
        """
        Метод для получения задач из ресурса.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        ...
