from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import AsyncIterable

from src.common.exceptions import InvalidJsonFormat
from src.models.task import Task
from src.models.task_mapper import TaskMapper


class FileTaskResource:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self._raw = None

    async def __aenter__(self) -> FileTaskResource:
        self._raw = await asyncio.to_thread(self.read_json)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self._raw = None

    def read_json(self) -> list[dict]:
        """
        Метод для чтения данных из JSON-файла.
        :return: Возвращает данные, прочитанные из JSON-файла.
        """
        if not self.file_path.is_file():
            raise FileNotFoundError
        with open(self.file_path, 'r') as file:
            data = json.loads(file.read())
        if isinstance(data, dict):
            data = [data]
        if not isinstance(data, list):
            raise InvalidJsonFormat("Неправильный формат Json. Ожидается словарь или список.")
        return data

    async def get_tasks(self) -> AsyncIterable[Task]:
        """
        Метод для получения задач из JSON-файла и преобразования их в объекты Task.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        if self._raw is None:
            self._raw = self.read_json()
        for item in self._raw:
            if not isinstance(item, dict):
                raise InvalidJsonFormat("Неправильный формат Json. Ожидается словари внутри списка.")
            yield TaskMapper.to_task(item)
