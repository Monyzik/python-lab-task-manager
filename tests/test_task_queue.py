import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.common.exceptions import InvalidResourceType, TaskManagerException, InvalidTaskType
from src.models.task import Task
from src.models.task_states import TaskStates
from src.resources.file_resource import FileTaskResource
from src.resources.generator_resource import GeneratorTaskResource
from src.task_queue import TaskQueue


def test_task_manager(fs: FakeFilesystem):
    task_manager = TaskQueue()
    fs.create_file("test.json", contents='[{"id": "1", "payload": {}}, {"id": "2", "payload": {}}]')
    file_resource = FileTaskResource("test.json")
    task_manager.add_tasks_from_resource(file_resource)
    assert len(task_manager) == 2
    assert task_manager[0].id == "1"
    assert task_manager[1].id == "2"
    first = next(iter(task_manager.filter(lambda t: t.id == "1")))
    assert first.description == ""

    tasks = TaskQueue([Task("1", "", 0, TaskStates.BACKLOG)])
    tasks.enqueue(Task("2", "", 0, TaskStates.BACKLOG))
    tasks.dequeue()
    assert len(tasks) == 1
    assert tasks[0].id == "2"
    filtered = tasks.filter_by_state(TaskStates.BACKLOG)
    assert len(list(filtered)) == 1


def test_task_view_same_iter():
    task_manager = TaskQueue()
    task_manager.add_tasks_from_resource(GeneratorTaskResource(10))
    task_view = task_manager.filter_by_priority(1, 5)
    first = []
    for task in task_view:
        first.append(task)
    second = []
    for task in task_view:
        second.append(task)
    assert first == second


def test_dequeue_from_empty_queue():
    task_manager = TaskQueue()
    with pytest.raises(TaskManagerException):
        task_manager.dequeue()


def test_invalid_filter():
    task_manager = TaskQueue()
    with pytest.raises(TaskManagerException):
        task_manager.filter_by_priority("a", "b")
    with pytest.raises(TaskManagerException):
        task_manager.filter_by_state("some_state")



def test_stop_iteration_exception():
    task_manager = TaskQueue()
    tasks = task_manager.filter_by_priority(1, 5)
    with pytest.raises(StopIteration):
        next(iter(tasks))


def test_invalid_resource_type():
    task_manager = TaskQueue()
    with pytest.raises(InvalidResourceType):
        task_manager.add_tasks_from_resource("invalid_resource")
    with pytest.raises(InvalidResourceType):
        task_manager.add_tasks_from_resource(123)


def test_invalid_element_type():
    class Test:
        def get_tasks(self):
            yield 123

    task_manager = TaskQueue()
    with pytest.raises(TaskManagerException):
        task_manager.add_tasks_from_resource(Test())
    with pytest.raises(TaskManagerException):
        TaskQueue([123])
    with pytest.raises(InvalidTaskType):
        task_manager.enqueue("invalid_task")
