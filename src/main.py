import asyncio
import json
import tempfile
import uuid
from random import choice

from src.common.config import logger
from src.common.constants import TASK_TEXT_SAMPLE
from src.handlers.task_handler import TaskHandler
from src.models.task_states import TaskStates
from src.resources.api_resource import ApiTaskResource
from src.resources.file_resource import FileTaskResource
from src.resources.generator_resource import GeneratorTaskResource
from src.resources.multi_task_resource import MultiTaskResource
from src.task_queue import TaskQueue


async def main() -> None:
    """
    Функция, которая является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        id1 = uuid.uuid4().hex
        json.dump([{"id": id1, "payload": choice(TASK_TEXT_SAMPLE)},
                   {"id": uuid.uuid4().hex, "payload": {"state": "Done"}}], tmp, indent=4)
        path = tmp.name

    resources: list = [FileTaskResource(path),
                       GeneratorTaskResource(2),
                       ApiTaskResource("google.com")
                       ]
    async with MultiTaskResource(resources) as multi_resource:
        task_manager = TaskQueue(multi_resource, TaskHandler())
        await task_manager.run(multi_resource.get_tasks())
        logger.info("Первая очередь задач выполнена\n")
        await task_manager.filter_by_state(state=TaskStates.DONE).run(multi_resource.get_tasks())
    # async for task in task_manager:
    #     print(task)
    # print(*task_manager.filter(lambda t: t.is_important))
    # filtered = task_manager.filter_by_priority(1, 4)
    # print(filtered.to_list())


if __name__ == "__main__":
    asyncio.run(main())
