import json
import tempfile

from models.task_contract import TaskContract
from resources.file_resource import FileTaskResource


def main() -> None:
    """
    Обязательнная составляющая программ, которые сдаются. Является точкой входа в приложение
    :return: Данная функция ничего не возвращает
    """

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        json.dump([{"id": 1, "name": "Test1"},
                   {"id": 2, "name": "Test2"}], tmp)
        path = tmp.name

    resources: list[TaskContract] = [FileTaskResource(path)]

    for item in resources:
        print(list(item.get_tasks()))


if __name__ == "__main__":
    main()
