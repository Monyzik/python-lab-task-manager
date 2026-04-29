import asyncio
from random import randint

from src.common.config import logger
from src.handlers.task_handler_protocol import TaskHandlerProtocol
from src.models.task import Task


class TaskHandler(TaskHandlerProtocol):
    async def handle(self, task: Task) -> None:
        logger.info(f"Начинало обработки задачи {task}")
        await asyncio.sleep(0.1 * randint(1, 5))
        logger.info(f"Конец обработки задачи {task}")
