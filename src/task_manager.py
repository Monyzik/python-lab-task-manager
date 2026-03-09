from collections import UserList
from typing import Any

from src.common.config import logger
from src.common.exceptions import InvalidResourceType, TaskManagerException, InvalidTaskType
from src.models.task import Task
from src.models.task_contract import TaskContract


class TaskManager(UserList[Task]):
    def __init__(self, tasks: list[Task] | None = None) -> None:
        if tasks is None:
            tasks = []
        super().__init__(self.validate(task) for task in tasks)

    @property
    def tasks_ids(self) -> list[str]:
        """
        Метод для получения списка идентификаторов всех задач в менеджере.
        :return: Возвращает список строк, представляющих идентификаторы задач.
        """
        return [task.id for task in self.data]

    @staticmethod
    def validate(task: Any) -> Task:
        """
        Метод для проверки, что переданный объект является экземпляром класса Task.
        :param task: Переданный объект, который нужно проверить.
        :return: Возвращает объект Task, если он является экземпляром класса Task.
        """
        if not isinstance(task, Task):
            raise InvalidTaskType(Task.__class__.__name__)
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
            if task.id in self.tasks_ids:
                logger.warning(
                    f"Не получилось добавить задачу с id {task.id}, так как задача с таким id уже существует.")
                continue
            self.data.append(task)

    def remove_task(self, task_id: str) -> None:
        """
        Метод для удаления задачи по ее идентификатору.
        :param task_id: Идентификатор задачи, которую нужно удалить.
        :return: Возвращает удаленную задачу, если она была найдена и удалена, иначе None.
        """
        deleted = False
        for i, task in enumerate(self.data):
            if task.id == task_id:
                removed_task = self.data.pop(i)
                logger.debug(f"Удаление задачи {removed_task}")
                deleted = True
        if not deleted:
            logger.warning(f"Задача {task_id} не найдена для удаления.")

    def pop(self, index: int = -1) -> Task:
        """
        Метод для удаления задачи по индексу.
        :param index: Индекс задачи, которую нужно удалить.
        :return: Возвращает удаленную задачу.
        """
        task = super().pop(index)
        logger.debug(f"Удаление задачи {task}")
        return task
