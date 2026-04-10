from collections import deque
from typing import Any, Iterator

from src.common.config import logger
from src.common.exceptions import InvalidResourceType, InvalidTaskType, TaskManagerException
from src.models.task import Task
from src.models.task_contract import TaskContract
from src.models.task_states import TaskStates
from src.models.task_view import TaskView


class TaskQueue(TaskView):
    def __init__(self, tasks: list[Task] | None = None) -> None:
        self._data = deque(self.validate(task) for task in tasks or ())
        super().__init__(self)

    def __iter__(self) -> Iterator[Task]:
        return iter(self._data)

    def __getitem__(self, item: int) -> Task:
        if not isinstance(item, int):
            raise TaskManagerException("TaskQueue поддерживает только индексирование целыми числами.")
        return self._data[item]

    def __len__(self) -> int:
        return len(self._data)

    def enqueue(self, task: Task) -> None:
        """
        Добавляет элемент в конец очереди.
        :param task: Задача, которую надо добавить в конец очереди.
        :return: Ничего не возвращает.
        """
        if not isinstance(task, Task):
            raise InvalidTaskType(Task.__name__)
        self._data.append(task)

    def dequeue(self) -> Task:
        """
        Удаляет элемент из начала очереди.
        :return: Возвращает удаленный элемент из начала очереди.
        """
        if len(self) == 0:
            raise TaskManagerException("Невозможно удалить задачу из пустой очереди.")
        return self._data.popleft()

    @property
    def tasks_ids(self) -> list[str]:
        """
        Метод для получения списка идентификаторов всех задач в менеджере.
        :return: Возвращает список строк, представляющих идентификаторы задач.
        """
        return [task.id for task in self._data]

    @staticmethod
    def validate(task: Any) -> Task:
        """
        Метод для проверки, что переданный объект является экземпляром класса Task.
        :param task: Переданный объект, который нужно проверить.
        :return: Возвращает объект Task, если он является экземпляром класса Task.
        """
        if not isinstance(task, Task):
            raise InvalidTaskType(Task.__name__)
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
            self.enqueue(task)

    def __repr__(self):
        return f"TaskQueue({list(self._data)})"
