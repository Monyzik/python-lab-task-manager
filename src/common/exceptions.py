class TaskManagerException(Exception):
    ...


class ImmutableAttributeError(TaskManagerException):
    ...


class InvalidConfigurationForResource(TaskManagerException):
    ...


class InvalidJsonFormat(TaskManagerException):
    ...


class InvalidApiResponseFormat(TaskManagerException):
    ...


class InvalidTaskId(TaskManagerException):
    ...


class InvalidTaskPriority(TaskManagerException):
    ...


class InvalidTaskFieldType(TaskManagerException):
    ...


class InvalidTaskType(TaskManagerException):
    def __init__(self, expected_type: str) -> None:
        super().__init__(f"Неправильный тип задачи. Ожидается: {expected_type}.")


class InvalidMappingType(TaskManagerException):
    ...


class InvalidMappingForTask(TaskManagerException):
    def __init__(self, name: str) -> None:
        super().__init__(f"Отсутствует обязательное поле {name}.")


class InvalidResourceType(TaskManagerException):
    def __init__(self, protocol: str) -> None:
        super().__init__(f"Ресурс не выполняет протокол: {protocol}.")
