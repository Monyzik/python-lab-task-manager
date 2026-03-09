import pytest
from _pytest.monkeypatch import MonkeyPatch

import src
from src.common.exceptions import InvalidConfigurationForResource
from src.resources.generator_resource import GeneratorTaskResource


def test_generator_resource(monkeypatch: MonkeyPatch):
    resource = GeneratorTaskResource(10, ["Task 0", "Task 1", "Task 2"])
    tasks = list(resource.get_tasks())
    assert len(tasks) == 10
    monkeypatch.setattr(src.resources.generator_resource.GeneratorTaskResource, "generate_tasks",
                        lambda x: [{"id": "1", "payload": "Task 1"}])
    tasks = list(resource.get_tasks())
    assert len(tasks) == 1
    assert tasks[0].payload == "Task 1"
    assert tasks[0].id == "1"


def test_invalid_task_count():
    with pytest.raises(InvalidConfigurationForResource):
        GeneratorTaskResource(0, ["Task 0", "Task 1", "Task 2"])
