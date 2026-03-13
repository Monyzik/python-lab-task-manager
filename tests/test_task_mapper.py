import pytest

from src.common.exceptions import InvalidMappingForTask
from src.models.task_mapper import TaskMapper


def test_task_mapper():
    task = TaskMapper.to_task({"id": 1, "payload": "Test payload"})
    assert task.id == 1
    assert task.payload == "Test payload"
    task = TaskMapper.to_task({"id": 1, "payload": [1, 2, 3]})
    assert task.id == 1
    assert task.payload == [1, 2, 3]


def test_task_mapper_invalid_mapping():
    with pytest.raises(InvalidMappingForTask):
        TaskMapper.to_task({"payload": "Test payload"})
    with pytest.raises(InvalidMappingForTask):
        TaskMapper.to_task({"id": 1})
