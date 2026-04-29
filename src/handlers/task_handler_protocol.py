from typing import Protocol

from src.models.task import Task


class TaskHandlerProtocol(Protocol):
    async def handle(self, task: Task) -> None:
        """
        Метод обработки задач
        :param task: Задача, которую необходимо обработать=
        :return: Ничего не возвращает
        """
        ...
