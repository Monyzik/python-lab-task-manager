# Лабораторная работа №3

### Запуск

Для запуска проекта необходимо выполнить следующую команду в терминале
(Так как в лабораторной работе не предусмотрено CLI, то взаимодействие с пользователем не производиться):

```shell
python -m src.main
```

**Все логи сохраняются в файл `.log`, который будет находиться в корневой папке проекта,
а также выводятся в консоль**

### Архитектура проекта:

```
.
├── common/
│   ├── config.py             # Логирование
│   ├── constants.py          # Наборы payload-примеров
│   └── exceptions.py         # Кастомные исключения
├── models/
│   ├── descriptors.py        # Data/non-data дескрипторы
│   ├── task.py               # Доменная модель Task
│   ├── task_contract.py      # Протокол источника задач
│   ├── task_mapper.py        # Маппинг dict -> Task
│   ├── task_states.py        # Статусы задачи
│   └── task_stream.py        # Повторно итерируемый поток задач
├── resources/
│   ├── api_resource.py       # Источник задач (API-заглушка)
│   ├── file_resource.py      # Источник задач из JSON
│   ├── generator_resource.py # Источник задач-генератор
│   └── multi_task_resource.py# Композитный источник задач
├── task_queue.py             # Ленивая коллекция задач
└── main.py                   # Точка входа
```

### Документация

#### Модель Task

Задача имеет следующие поля:

- id - уникальный идентификатор (неизменяемый)
- description - описание задачи (строка)
- priority - важность (целое число от 0 до 10)
- state - статус задачи (TaskState enum)
- created_at - дата создания (неизменяемый)

#### Дескрипторы

- TypedFieldDescriptor - data descriptor, проверяет тип поля.
- PriorityFieldDescriptor - data descriptor, наследуется от TypedFieldDescriptor и добавляет проверку диапазона.
- CreatedAtFieldDescriptor - non-data descriptor, возвращает время создания.

#### TaskQueue

`TaskQueue` — это лениво итерируемая коллекция задач, которая позволяет строить цепочки фильтров. Она использует
`TaskStream` для получения данных.

**Фильтрация**: Методы `filter()`, `filter_by_state()` и `filter_by_priority()` возвращают новый экземпляр `TaskQueue`
с добавленным условием, не выполняя реальной фильтрации до начала итерации.

#### Источники задач

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
- `MultiTaskResource` - источник, который объединяет несколько других источников в один.

Преобразование словарей задач в объекты **Task** происходит с помощью **TaskMapper** и метода **to_task**.