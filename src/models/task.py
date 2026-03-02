from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    """
    Класс, который описывает задачу

    :param id: Индификатор задачи.
    :param payload: Произвольные данные задачи.
    """
    id: int
    payload: Any
