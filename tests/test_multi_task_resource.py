from src.resources.api_resource import ApiTaskResource
from src.resources.generator_resource import GeneratorTaskResource
from src.resources.multi_task_resource import MultiTaskResource
from src.task_queue import TaskQueue


def test_multi_task_resource():
    tasks1 = GeneratorTaskResource(10)
    tasks2 = ApiTaskResource("google.com")
    tasks_list = [tasks1, tasks2]
    resource = MultiTaskResource(tasks_list).get_tasks()
    assert len(list(resource)) >= 10
