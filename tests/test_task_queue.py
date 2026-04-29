import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from src.common.exceptions import InvalidResourceType, TaskManagerException, InvalidTaskType
from src.handlers.task_handler import TaskHandler
from src.models.task import Task
from src.models.task_states import TaskStates
from src.models.task_stream import TaskStream
from src.resources.file_resource import FileTaskResource
from src.resources.generator_resource import GeneratorTaskResource
from src.task_queue import TaskQueue


@pytest.mark.asyncio
async def test_task_manager(fs: FakeFilesystem):
    fs.create_file("test.json", contents='[{"id": "1", "payload": {}}, {"id": "2", "payload": {}}]')
    file_resource = FileTaskResource("test.json")
    task_manager = TaskQueue(file_resource, TaskHandler)
    tasks = [task async for task in task_manager]
    assert len(tasks) == 2
    assert tasks[0].id == "1"
    assert tasks[1].id == "2"
    tasks = [task async for task in task_manager.filter(lambda t: t.id == "1")]
    first = next(iter(tasks))
    assert first.description == ""

    stream = TaskStream(GeneratorTaskResource(1))
    stream._tasks = [Task("1", "", 0, TaskStates.BACKLOG)]
    tasks = TaskQueue(GeneratorTaskResource(1), TaskHandler, stream=stream)
    tasks = [task async for task in tasks]
    assert len(tasks) == 2
    assert tasks[0].id == "1"

    file_resource = FileTaskResource("test.json")
    task_manager = TaskQueue(file_resource, TaskHandler())
    print(task_manager)
    await task_manager.run(file_resource.get_tasks())
    print(task_manager)


@pytest.mark.asyncio
async def test_task_view_same_iter():
    source = GeneratorTaskResource(10)
    task_manager = TaskQueue(source, TaskHandler)
    task_view = [task async for task in task_manager.filter_by_priority(1, 5)]
    first = []
    for task in task_view:
        first.append(task)
    second = []
    for task in task_view:
        second.append(task)
    assert first == second


@pytest.mark.asyncio
async def test_invalid_filter():
    source = GeneratorTaskResource(10)
    task_manager = TaskQueue(source, TaskHandler)
    tasks = [task async for task in task_manager]
    with pytest.raises(TaskManagerException):
        task_manager.filter_by_priority("a", "b")
    with pytest.raises(TaskManagerException):
        task_manager.filter_by_state("some_state")


@pytest.mark.asyncio
async def test_stop_iteration_exception():
    source = GeneratorTaskResource(1)
    task_manager = TaskQueue(source, TaskHandler)
    tasks = task_manager.filter_by_priority(100, 200)
    tasks = [task async for task in tasks]
    with pytest.raises(StopIteration):
        next(iter(tasks))
