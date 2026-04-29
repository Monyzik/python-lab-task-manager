from __future__ import annotations

import asyncio
from typing import Callable, AsyncIterable, AsyncIterator

from src.common.config import logger
from src.common.exceptions import TaskManagerException
from src.handlers.task_handler_protocol import TaskHandlerProtocol
from src.models.task import Task
from src.models.task_contract import AsyncTaskContract
from src.models.task_states import TaskStates
from src.models.task_stream import TaskStream

Condition = Callable[[Task], bool]


class TaskQueue(AsyncIterable[Task]):
    def __init__(self, source: AsyncTaskContract,
                 handler: TaskHandlerProtocol,
                 stream: AsyncIterable[Task] | None = None,
                 conditions: tuple[Condition, ...] = (),
                 workers_number: int = 3) -> None:
        self._queue = asyncio.Queue()
        self._source = source
        self._handler = handler
        self._workers_number = workers_number
        self._stream = stream or TaskStream(source)
        self._conditions = conditions

    async def worker(self) -> None:
        """
        Функция для обработки задач из очереди.
        :return: Ничего не возвращает.
        """
        while True:
            task = await self._queue.get()
            try:
                if task is None:
                    return
                try:
                    await self._handler.handle(task)
                except Exception:
                    logger.exception(f"Ошибка при обработке задачи {task}")
            finally:
                self._queue.task_done()

    async def run(self, source: AsyncIterable[Task]) -> None:
        """
        Функция для запуска обработки задач из источника.
        :param source: Источник задач.
        :return: Ничего не возвращает.
        """
        workers = [asyncio.create_task(self.worker()) for _ in range(self._workers_number)]
        try:
            async for task in source:
                if all(cond(task) for cond in self._conditions):
                    await self._queue.put(task)
            await self._queue.join()
        finally:
            for _ in workers:
                await self._queue.put(None)
            await asyncio.gather(*workers, return_exceptions=True)

    async def __aiter__(self) -> AsyncIterator[Task]:
        async for task in self._stream:
            if all(cond(task) for cond in self._conditions):
                yield task

    def filter(self, condition: Condition) -> TaskQueue:
        """
        Фильтрует коллекцию по определенному условию.
        :param condition: Условие, по котором будет отфильтрована коллекция.
        :return: Возвращает объект TaskQueue, который содержит задачи, удовлетворяющие условию.
        """
        return TaskQueue(self._source, self._handler, self._stream, self._conditions + (condition,))

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

    def __repr__(self):
        return f"TaskQueue(source={type(self._source).__name__}, handler={type(self._handler).__name__}, conditions={self._conditions})"
