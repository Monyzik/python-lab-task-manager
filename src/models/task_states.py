from enum import Enum


class TaskStates(str, Enum):
    """
    Enum, который описывает возможные состояния задачи.
    """
    BACKLOG = "Backlog"
    IN_PROGRESS = "In progress"
    IN_REVIEW = "In review"
    DONE = "Done"
