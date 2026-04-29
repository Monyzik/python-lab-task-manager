import pytest

from src.resources.api_resource import ApiTaskResource
from src.resources.generator_resource import GeneratorTaskResource
from src.resources.multi_task_resource import MultiTaskResource
from src.task_queue import TaskQueue


@pytest.mark.asyncio
async def test_multi_task_resource():
    tasks1 = GeneratorTaskResource(10)
    tasks2 = ApiTaskResource("google.com")
    tasks_list = [tasks1, tasks2]
    resource = MultiTaskResource(tasks_list).get_tasks()
    assert len([task async for task in resource]) >= 10

    async with MultiTaskResource([GeneratorTaskResource(10)]) as resource:
        assert len([task async for task in resource.get_tasks()]) == 10

