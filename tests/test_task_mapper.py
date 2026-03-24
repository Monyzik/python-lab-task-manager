import pytest

from src.common.constants import TASK_TEXT_SAMPLE
from src.common.exceptions import InvalidMappingForTask, InvalidMappingType
from src.models.task_mapper import TaskMapper
from src.models.task_states import TaskStates


def test_task_mapper():
    task = TaskMapper.to_task({"id": "1", "payload": TASK_TEXT_SAMPLE[0]})
    assert task.id == "1"
    assert task.description == "Сделать матан"
    assert task.priority == 3
    assert task.state == TaskStates.BACKLOG
    task = TaskMapper.to_task({"id": "1", "payload": TASK_TEXT_SAMPLE[3]})
    assert task.id == "1"
    assert task.description == "Проверить обработку ошибок"


def test_task_mapper_invalid_mapping():
    with pytest.raises(InvalidMappingType):
        TaskMapper.to_task({"payload": "Test payload"})
    with pytest.raises(InvalidMappingForTask):
        TaskMapper.to_task({"id": 1})
