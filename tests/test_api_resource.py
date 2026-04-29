import pytest
from _pytest.monkeypatch import MonkeyPatch

import src.resources.api_resource
from src.common.exceptions import InvalidApiResponseFormat
from src.models.task_states import TaskStates
from src.resources.api_resource import ApiTaskResource


@pytest.mark.asyncio
async def test_api_resource(monkeypatch: MonkeyPatch):
    resource = ApiTaskResource("https://hello_world")
    monkeypatch.setattr(src.resources.api_resource.ApiTaskResource, 'get_tasks_from_api',
                        lambda x: [{"id": "1", "payload": {"description": "Написать тесты", "priority": 8,
                                                           "state": TaskStates.IN_REVIEW}}])
    tasks = [task async for task in resource.get_tasks()]
    assert len(tasks) == 1
    assert tasks[0].description == "Написать тесты"
    assert tasks[0].id == "1"

    async with ApiTaskResource("https://hello_world") as api:
        assert len([task async for task in api.get_tasks()]) == 1

@pytest.mark.asyncio
async def test_invalid_response_format(monkeypatch: MonkeyPatch):
    with pytest.raises(InvalidApiResponseFormat):
        resource = ApiTaskResource("https://hello_world")
        monkeypatch.setattr(src.resources.api_resource.ApiTaskResource, 'get_tasks_from_api',
                            lambda x: 67)
        tasks = [task async for task in resource.get_tasks()]
        assert tasks
