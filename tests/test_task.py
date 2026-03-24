from datetime import datetime

import pytest

from src.common.exceptions import ImmutableAttributeError, InvalidTaskFieldType, InvalidTaskPriority
from src.models.task import Task
from src.models.task_states import TaskStates


def test_task():
    task = Task("1", "abacaba", 1, TaskStates.IN_PROGRESS)
    assert task.id == "1"
    assert task.description == "abacaba"
    assert task.priority == 1
    assert task.state == TaskStates.IN_PROGRESS
    assert task.is_ready is False
    task.state = TaskStates.DONE
    assert task.is_ready is True
    assert task.is_important is False
    task.priority = 10
    assert task.is_ready is True
    assert task.state == TaskStates.DONE


def test_immutable_attribute_error():
    task = Task("1", "abacaba", 1, TaskStates.IN_PROGRESS)
    with pytest.raises(ImmutableAttributeError):
        task._id = "2"
    with pytest.raises(ImmutableAttributeError):
        task.id = "2"
    with pytest.raises(ImmutableAttributeError):
        task.created_at = datetime.now()
    with pytest.raises(ImmutableAttributeError):
        task._created_at = datetime.now()


def test_invalid_task_field_type():
    task = Task("1", "abacaba", 1, TaskStates.IN_PROGRESS)
    with pytest.raises(InvalidTaskFieldType):
        task.priority = "abacaba"
    with pytest.raises(InvalidTaskFieldType):
        task.state = "abacaba"
    with pytest.raises(InvalidTaskFieldType):
        task.description = 1


def test_invalid_task_priority():
    task = Task("1", "abacaba", 1, TaskStates.IN_PROGRESS)
    with pytest.raises(InvalidTaskPriority):
        task.priority = -1
    with pytest.raises(InvalidTaskPriority):
        task.priority = 11
