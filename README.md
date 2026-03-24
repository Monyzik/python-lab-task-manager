# Лабораторная работа №2

### Запуск

Для запуска проекта необходимо выполнить следующую команду в терминале
(Так как в лабораторной работе не предусмотрено CLI, то взаимодействие с пользователем не производиться):

```shell
python -m src.main
```

**Все логи сохраняются в файл ```.log```, который будет находиться в корневой папке проекта,
а также выводятся в консоль**

### Архитектура проекта:

```
.
├── common/
│   ├── config.py             # Логирование
│   ├── constants.py          # Наборы payload-примеров
│   └── exceptions.py         # Кастомные исключения проекта
├── models/
│   ├── descriptors.py        # Data/non-data дескрипторы
│   ├── task.py               # Доменная модель Task
│   ├── task_contract.py      # Протокол источника задач
│   ├── task_mapper.py        # Маппинг dict -> Task
│   └── task_states.py        # Статусы задачи
├── resources/
│   ├── api_resource.py       # Источник задач (API-заглушка)
│   ├── file_resource.py      # Источник задач из JSON
│   └── generator_resource.py # Источник задач-генератор
├── main.py                   # Точка входа
└── task_manager.py           # Коллекция и операции над Task
```

### Документация

#### Модель `Task`

Задача имеет следующие поля:

- id — уникальный идентификатор (неизменяемый)
- description — описание задачи (строка)
- priority — важность (целое число от 0 до 10)
- state — статус задачи (TaskState enum)
- created_at — дата создания (неизменяемый)

#### Дескрипторы

- `TypedFieldDescriptor` - **data descriptor** (`__get__` + `__set__`), проверяет тип поля.
- `PriorityFieldDescriptor` - **data descriptor**, наследуется от `TypedFieldDescriptor` и добавляет проверку диапазона.
- `CreatedAtFieldDescriptor` - **non-data descriptor** (`__get__` без `__set__`), возвращает время создания.


Все источники задач используют единый интерфейс:

```python
@runtime_checkable
class TaskContract(Protocol):
    def get_tasks(self) -> Iterable[Task]:
        ...
```

Реализованные источники:

- `FileTaskResource` - читает JSON (один объект или список объектов).
- `GeneratorTaskResource` - генерирует задачи на основе `TASK_TEXT_SAMPLE`.
- `ApiTaskResource` - имитирует API-ответ и возвращает задачи.

Преобразование словарей задач в объекты **Task** происходит с помощью **TaskMapper** и метода **to_task**.

Также реализован **TaskManager**, который производит обработку задач
(добавление из источников и удаление) (наследуется от **UserList**)
