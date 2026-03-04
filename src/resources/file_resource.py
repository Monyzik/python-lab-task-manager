import json
from pathlib import Path
from typing import Iterable, Any

from src.common.exceptions import InvalidJsonFormat
from src.models.task import Task
from src.models.task_mapper import TaskMapper


class FileTaskResource:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)

    def read_json(self) -> Any:
        """
        Метод для чтения данных из JSON-файла.
        :return: Возвращает данные, прочитанные из JSON-файла.
        """
        if not self.file_path.is_file():
            raise FileNotFoundError
        with open(self.file_path, 'r') as file:
            return json.loads(file.read())

    def get_tasks(self) -> Iterable[Task]:
        """
        Метод для получения задач из JSON-файла и преобразования их в объекты Task.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        data = self.read_json()
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            raise InvalidJsonFormat("Неправильный формат Json. Ожидается словарь или список.")
        for item in data:
            if not isinstance(item, dict):
                raise InvalidJsonFormat("Неправильный формат Json. Ожидается словари внутри списка.")
            yield TaskMapper.to_task(item)
