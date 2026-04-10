from __future__ import annotations

from collections.abc import Iterable
from typing import Iterator, Callable

from src.common.exceptions import TaskManagerException
from src.models.task import Task
from src.models.task_contract import TaskContract
from src.models.task_states import TaskStates
from src.models.task_stream import TaskStream

Condition = Callable[[Task], bool]


class TaskQueue(Iterable[Task]):
    def __init__(self, source: TaskContract, stream: Iterable[Task] | None = None,
                 conditions: tuple[Condition, ...] = ()) -> None:
        self._source = source
        self._stream = stream or TaskStream(source)
        self._conditions = conditions

    def __iter__(self) -> Iterator[Task]:
        for task in self._stream:
            if all(cond(task) for cond in self._conditions):
                yield task

    def filter(self, condition: Condition) -> TaskQueue:
        """
        Фильтрует коллекцию по определенному условию.
        :param condition: Условие, по котором будет отфильтрована коллекция.
        :return: Возвращает объект TaskQueue, который содержит задачи, удовлетворяющие условию.
        """
        return TaskQueue(self._source, self._stream, self._conditions + (condition,))

    def filter_by_state(self, state: TaskStates) -> TaskQueue:
        """
        Фильтрует коллекцию по состоянию задачи.
        :param state: Состояние задачи.
        :return: Возвращает объект TaskQueue, который содержит задачи, удовлетворяющие условию по состоянию.
        """
        if not isinstance(state, TaskStates):
            raise TaskManagerException("Неверный тип состояния задачи. Ожидается TaskStates.")
        return self.filter(lambda t: t.state == state)

    def filter_by_priority(self, min_priority: int, max_priority: int) -> TaskQueue:
        """
        Фильтрует коллекцию по приоритету в диапазоне [min_priority, max_priority].
        :param min_priority: Минимальный приоритет.
        :param max_priority: Максимальный приоритет.
        :return: Возвращает объект TaskQueue, который содержит задачи, удовлетворяющие условию по приоритету.
        """
        if not isinstance(min_priority, int) or not isinstance(max_priority, int):
            raise TaskManagerException("Неверный тип приоритета. Ожидается int.")
        return self.filter(lambda t: min_priority <= t.priority <= max_priority)

    def to_list(self) -> list[Task]:
        """
        Преобразует итератор в лист.
        :return: Возвращает лист из задач.
        """
        return list(self)

    def __repr__(self):
        return f"TaskQueue({self.to_list()})"
