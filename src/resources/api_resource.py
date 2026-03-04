import uuid
from random import choice, randint
from typing import Iterable, Any

from src.common.exceptions import InvalidApiResponseFormat
from src.models.task import Task
from src.models.task_mapper import TaskMapper


class ApiTaskResource:
    def __init__(self, path: str):
        self.task_count = randint(1, 10)
        self.path = path
        self.payload_samples = [f"Sample payload {i} from {path}" for i in range(1, 6)]

    def get_tasks_from_api(self) -> list[dict[str, Any]]:
        """
        Метод для получения задач из API.
        :return: Возвращает список словарей.
        """
        response = []
        for _ in range(self.task_count):
            response.append({"id": uuid.uuid4().int, "payload": choice(self.payload_samples)})
        return response

    def get_tasks(self) -> Iterable[Task]:
        """
        Метод для получения задач из API и преобразования их в объекты Task.
        :return: Возвращает итератор, который предоставляет объекты Task.
        """
        response = self.get_tasks_from_api()
        if not isinstance(response, list):
            raise InvalidApiResponseFormat("Неправильный формат ответа от API. Ожидается список словарей")
        for task in response:
            yield TaskMapper.to_task(task)
