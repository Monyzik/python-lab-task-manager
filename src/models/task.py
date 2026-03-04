from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    id: int
    payload: Any
