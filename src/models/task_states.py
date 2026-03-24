from enum import Enum


class TaskStates(str, Enum):
    BACKLOG = "Backlog"
    IN_PROGRESS = "In progress"
    IN_REVIEW = "In review"
    DONE = "Done"
