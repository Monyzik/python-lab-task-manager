import json
from pathlib import Path
from typing import Iterable

from src.common.exceptions import InvalidJsonFormat
from src.models.task import Task
from src.models.task_mapper import TaskMapper


class FileTaskResource:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        if not self.file_path.is_file():
            raise FileNotFoundError

    def get_tasks(self) -> Iterable[Task]:
        with open(self.file_path, 'r') as file:
            data = json.loads(file.read())
        if not isinstance(data, dict) and not isinstance(data, list):
            raise InvalidJsonFormat("Неправильный формат Json. Ожидается словарь или список.")
        if isinstance(data, dict):
            yield TaskMapper.to_task(data)
        else:
            for item in data:
                if not isinstance(item, dict):
                    raise InvalidJsonFormat("Неправильный формат Json. Ожидается словари внутри списка.")
                yield TaskMapper.to_task(item)
