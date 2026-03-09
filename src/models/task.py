from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    id: str
    payload: Any
