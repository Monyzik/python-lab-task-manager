from typing import Any, override

from src.common.exceptions import InvalidTaskFieldType, InvalidTaskPriority


class TypedFieldDescriptor:
    """
    Дескриптор, который проверяет тип поля (expected_type).
    """

    def __init__(self, expected_type: type):
        self._expected_type = expected_type

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance: Any, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise InvalidTaskFieldType(f"Значение {self.name} должно быть {self._expected_type}")
        object.__setattr__(instance, self.name, value)


class PriorityFieldDescriptor(TypedFieldDescriptor):
    """
    Дескриптор для поля приоритета, который проверяет, что значение является целым числом в диапазоне от 0 до 10.
    """

    def __init__(self, min_value: int = 0, max_value: int = 10):
        super().__init__(int)
        self.min_value = min_value
        self.max_value = max_value

    @override
    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            raise InvalidTaskFieldType(f"Значение {self.name} должно быть {self._expected_type}")
        if not (self.min_value <= value <= self.max_value):
            raise InvalidTaskPriority("Приоритет должен быть целым числом от 0 до 10.")
        object.__setattr__(instance, self.name, value)


class CreatedAtFieldDescriptor:
    """
    Non-data дескриптор для поля времени создания,
    который возвращает время создания задачи и
    не позволяет изменять это значение после его установки.
    """

    def __set_name__(self, owner, name: str) -> None:
        self.name = f"_{name}"

    def __get__(self, instance: Any, owner):
        if instance is None:
            return self
        return getattr(instance, self.name)
