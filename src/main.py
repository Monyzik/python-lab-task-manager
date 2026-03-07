import json
import tempfile
import uuid

from src.common.config import logger
from src.models.task_contract import TaskContract
from src.resources.file_resource import FileTaskResource
from src.resources.api_resource import ApiTaskResource
from src.resources.generator_resource import GeneratorTaskResource
from src.task_manager import TaskManager


def main() -> None:
    """
    Обязательная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        id1 = uuid.uuid4().int
        json.dump([{"id": id1, "payload": "Test1"},
                   {"id": uuid.uuid4().int, "t": []}], tmp, indent=4)
        path = tmp.name

    resources: list[TaskContract] = [FileTaskResource(path), GeneratorTaskResource(2), ApiTaskResource(path)]

    task_manager = TaskManager()
    for resource in resources:
        try:
            task_manager.add_tasks_from_resource(resource)
        except Exception as e:
            logger.error(f"Ошибка при добавлении задач из ресурса {resource.__class__.__name__}: {e}")
    task_manager.remove_task(id1)
    task_manager.pop(1)


if __name__ == "__main__":
    main()
