import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.common.exceptions import InvalidResourceType, TaskManagerException, InvalidTaskType
from src.models.task import Task
from src.models.task_states import TaskStates
from src.resources.file_resource import FileTaskResource
from src.resources.generator_resource import GeneratorTaskResource
from src.task_queue import TaskQueue


def test_task_manager(fs: FakeFilesystem):
    fs.create_file("test.json", contents='[{"id": "1", "payload": {}}, {"id": "2", "payload": {}}]')
    file_resource = FileTaskResource("test.json")
    task_manager = TaskQueue(file_resource)
    assert len(task_manager.to_list()) == 2
    assert task_manager.to_list()[0].id == "1"
    assert task_manager.to_list()[1].id == "2"
    first = next(iter(task_manager.filter(lambda t: t.id == "1")))
    assert first.description == ""

    tasks = TaskQueue(GeneratorTaskResource(1), stream=[Task("1", "", 0, TaskStates.BACKLOG)])
    assert len(tasks.to_list()) == 1
    assert tasks.to_list()[0].id == "1"
    filtered = tasks.filter_by_state(TaskStates.BACKLOG)
    assert len(filtered.to_list()) == 1


def test_task_view_same_iter():
    source = GeneratorTaskResource(10)
    task_manager = TaskQueue(source)
    task_view = task_manager.filter_by_priority(1, 5)
    first = []
    for task in task_view:
        first.append(task)
    second = []
    for task in task_view:
        second.append(task)
    assert first == second


def test_invalid_filter():
    source = GeneratorTaskResource(10)
    task_manager = TaskQueue(source)
    with pytest.raises(TaskManagerException):
        task_manager.filter_by_priority("a", "b")
    with pytest.raises(TaskManagerException):
        task_manager.filter_by_state("some_state")


def test_stop_iteration_exception():
    source = GeneratorTaskResource(1)
    task_manager = TaskQueue(source)
    tasks = task_manager.filter_by_priority(100, 200)
    with pytest.raises(StopIteration):
        next(iter(tasks))
