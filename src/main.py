import json
import tempfile
import uuid
from random import choice

from src.common.constants import TASK_TEXT_SAMPLE
from src.models.task_contract import TaskContract
from src.resources.api_resource import ApiTaskResource
from src.resources.file_resource import FileTaskResource
from src.resources.generator_resource import GeneratorTaskResource
from src.resources.multi_task_resource import MultiTaskResource
from src.task_queue import TaskQueue


def main() -> None:
    """
    Функция, которая является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        id1 = uuid.uuid4().hex
        json.dump([{"id": id1, "payload": choice(TASK_TEXT_SAMPLE)},
                   {"id": uuid.uuid4().hex, "payload": {"state": "Done"}}], tmp, indent=4)
        path = tmp.name

    resources: list[TaskContract] = [FileTaskResource(path), GeneratorTaskResource(2), ApiTaskResource("google.com")]

    task_manager = TaskQueue(MultiTaskResource(resources))
    print(task_manager.to_list())
    print(*task_manager.filter(lambda t: t.is_important))
    filtered = task_manager.filter_by_priority(1, 4)
    print(filtered.to_list())


if __name__ == "__main__":
    main()
