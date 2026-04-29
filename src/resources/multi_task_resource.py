from typing import AsyncIterable

from src.models.task import Task
from src.models.task_contract import AsyncTaskContract


class MultiTaskResource:
    def __init__(self, resources: list[AsyncTaskContract]):
        self._resources = resources

    async def __aenter__(self):
        for resource in self._resources:
            await resource.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        for resource in self._resources:
            await resource.__aexit__(exc_type, exc_val, exc_tb)

    async def get_tasks(self) -> AsyncIterable[Task]:
        for resource in self._resources:
            async for task in resource.get_tasks():
                yield task
