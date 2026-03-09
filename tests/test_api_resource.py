import pytest
from _pytest.monkeypatch import MonkeyPatch

import src.resources.api_resource
from src.common.exceptions import InvalidApiResponseFormat
from src.resources.api_resource import ApiTaskResource


def test_api_resource(monkeypatch: MonkeyPatch):
    resource = ApiTaskResource("https://hello_world")
    list(resource.get_tasks())
    monkeypatch.setattr(src.resources.api_resource.ApiTaskResource, 'get_tasks_from_api',
                        lambda x: [{"id": "1", "payload": "Task 1"}])
    tasks = list(resource.get_tasks())
    assert len(tasks) == 1
    assert tasks[0].payload == "Task 1"
    assert tasks[0].id == "1"


def test_invalid_response_format(monkeypatch: MonkeyPatch):
    with pytest.raises(InvalidApiResponseFormat):
        resource = ApiTaskResource("https://hello_world")
        monkeypatch.setattr(src.resources.api_resource.ApiTaskResource, 'get_tasks_from_api',
                            lambda x: 67)
        list(resource.get_tasks())
