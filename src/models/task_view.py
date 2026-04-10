from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Callable

from src.common.exceptions import TaskManagerException
from src.models.task import Task
from src.models.task_states import TaskStates

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
        """
        Фильтрует коллекцию по определенному условию.
        :param condition: Условие, по котором будет отфильтрована коллекция.
        :return: Возвращает объект TaskView, который содержит задачи, удовлетворяющие условию.
        """
        return TaskView(self._tasks, self._conditions + (condition,))

    def filter_by_state(self, state: TaskStates) -> TaskView:
        """
        Фильтрует коллекцию по состоянию задачи.
        :param state: Состояние задачи.
        :return: Возвращает объект TaskView, который содержит задачи, удовлетворяющие условию по состоянию.
        """
        if not isinstance(state, TaskStates):
            raise TaskManagerException("Неверный тип состояния задачи. Ожидается TaskStates.")
        return self.filter(lambda t: t.state == state)

    def filter_by_priority(self, min_priority: int, max_priority: int) -> TaskView:
        """
        Фильтрует коллекцию по приоритету в диапазоне [min_priority, max_priority].
        :param min_priority: Минимальный приоритет.
        :param max_priority: Максимальный приоритет.
        :return: Возвращает объект TaskView, который содержит задачи, удовлетворяющие условию по приоритету.
        """
        if not isinstance(min_priority, int) or not isinstance(max_priority, int):
            raise TaskManagerException("Неверный тип приоритета. Ожидается int.")
        return self.filter(lambda t: min_priority <= t.priority <= max_priority)
