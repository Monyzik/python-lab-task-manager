class TaskManagerException(Exception):
    ...


class InvalidConfigurationForResource(TaskManagerException):
    ...


class InvalidJsonFormat(TaskManagerException):
    ...


class InvalidApiResponseFormat(TaskManagerException):
    ...


class InvalidTaskId(TaskManagerException):
    ...


class InvalidTaskType(TaskManagerException):
    def __init__(self, expected_type: str) -> None:
        super().__init__(f"Неправильный тип задачи. Ожидается: {expected_type}.")


class InvalidMappingForTask(TaskManagerException):
    def __init__(self, name: str) -> None:
        super().__init__(f"Отсутствует обязательное поле {name}.")


class InvalidResourceType(TaskManagerException):
    def __init__(self, protocol: str) -> None:
        super().__init__(f"Ресурс не выполняет протокол: {protocol}.")
