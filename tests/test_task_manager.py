import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.common.exceptions import InvalidResourceType, TaskManagerException
from src.models.task import Task
from src.resources.file_resource import FileTaskResource
from src.task_manager import TaskManager


def test_task_manager(fs: FakeFilesystem):
    task_manager = TaskManager()
    fs.create_file("test.json", contents='[{"id": 1, "payload": "Test1"}, {"id": 2, "payload": []}]')
    file_resource = FileTaskResource("test.json")
    task_manager.add_tasks_from_resource(file_resource)
    assert len(task_manager.data) == 2
    assert task_manager.data[0].id == 1
    removed_task = task_manager.remove_task(task_manager.data[0].id)
    assert removed_task.payload == "Test1"
    assert len(task_manager.data) == 1
    popped_task = task_manager.pop(0)
    assert popped_task.id == 2
    assert len(task_manager.data) == 0
    task_manager = TaskManager([Task(id=1, payload="Test1")])
    assert len(task_manager.data) == 1
    assert task_manager.data[0].id == 1


def test_invalid_resource_type():
    task_manager = TaskManager()
    with pytest.raises(InvalidResourceType):
        task_manager.add_tasks_from_resource("invalid_resource")
    with pytest.raises(InvalidResourceType):
        task_manager.add_tasks_from_resource(123)


def test_invalid_element_type():
    class Test:
        def get_tasks(self):
            yield 123

    task_manager = TaskManager()
    with pytest.raises(TaskManagerException):
        task_manager.add_tasks_from_resource(Test())
    with pytest.raises(TaskManagerException):
        TaskManager([123])


def test_remove_non_existent_task():
    task_manager = TaskManager([Task(id=1, payload="Test1")])
    removed_task = task_manager.remove_task(999)
    assert removed_task is None
