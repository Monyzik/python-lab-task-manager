from collections import UserList
from typing import Any

from src.common.config import logger
from src.common.exceptions import InvalidResourceType, TaskManagerException
from src.models.task import Task
from src.models.task_contract import TaskContract


class TaskManager(UserList[Task]):
    def __init__(self, tasks: list[Task] | None = None) -> None:
        if tasks is None:
            tasks = []
        super().__init__(self.validate(task) for task in tasks)

    @staticmethod
    def validate(task: Any) -> Task:
        if not isinstance(task, Task):
            raise TaskManagerException("Элемент должен быть объектом типа Task.")
        return task

    def add_tasks_from_resource(self, resource: TaskContract) -> None:
        """
        Метод для добавления задач из ресурса.
        :param resource: Ресурс, который предоставляет задачи.
        :return: Ничего не возвращает.
        """
        if not isinstance(resource, TaskContract):
            raise InvalidResourceType(TaskContract.__name__)
        for task in resource.get_tasks():
            task = self.validate(task)
            logger.debug(f"Добавление задачи {task}")
            self.data.append(task)

    def remove_task(self, task_id: int) -> Task | None:
        """
        Метод для удаления задачи по ее идентификатору.
        :param task_id: Идентификатор задачи, которую нужно удалить.
        :return: Возвращает удаленную задачу, если она была найдена и удалена, иначе None.
        """
        for i, task in enumerate(self.data):
            if task.id == task_id:
                removed_task = self.data.pop(i)
                logger.debug(f"Удаление задачи {removed_task}")
                return removed_task
        logger.warning(f"Задача с id {task_id} не найдена для удаления.")
        return None

    def pop(self, index: int = -1) -> Task:
        """
        Метод для удаления задачи по индексу.
        :param index: Индекс задачи, которую нужно удалить.
        :return: Возвращает удаленную задачу.
        """
        task = super().pop(index)
        logger.debug(f"Удаление задачи {task}")
        return task
