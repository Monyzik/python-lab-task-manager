import pytest
from _pytest.monkeypatch import MonkeyPatch

import src
from src.common.constants import TASK_TEXT_SAMPLE
from src.common.exceptions import InvalidConfigurationForResource
from src.models.task_states import TaskStates
from src.resources.generator_resource import GeneratorTaskResource


@pytest.mark.asyncio
async def test_generator_resource(monkeypatch: MonkeyPatch):
    async with GeneratorTaskResource(10, TASK_TEXT_SAMPLE[1:3]) as resource:
        tasks = [task async for task in resource.get_tasks()]
        assert len(tasks) == 10
    monkeypatch.setattr(src.resources.generator_resource.GeneratorTaskResource, "generate_tasks",
                        lambda x: [{"id": "1", "payload": TASK_TEXT_SAMPLE[0]}])
    tasks = [task async for task in resource.get_tasks()]
    assert len(tasks) == 1
    assert tasks[0].state == TaskStates.BACKLOG
    assert tasks[0].id == "1"


def test_invalid_task_count():
    with pytest.raises(InvalidConfigurationForResource):
        GeneratorTaskResource(0, ["Task 0", "Task 1", "Task 2"])
