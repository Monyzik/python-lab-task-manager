from src.models.task_states import TaskStates

TASK_TEXT_SAMPLE = (
    {"description": "Сделать матан", "priority": 3, "state": TaskStates.BACKLOG},
    {"description": "Закончить лабу по питону", "priority": 6, "state": TaskStates.IN_PROGRESS},
    {"description": "Написать тесты", "priority": 8, "state": TaskStates.IN_REVIEW},
    {"description": "Проверить обработку ошибок", "priority": 5, "state": TaskStates.BACKLOG},
    {"description": "Создать репозиторий", "priority": 2, "state": TaskStates.DONE},
)
