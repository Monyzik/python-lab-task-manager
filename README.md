# Лабораторная работа №4

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
│   ├── config.py             # Логирование и конфигурация
│   ├── constants.py          # Константы и примеры payload'ов
│   └── exceptions.py         # Кастомные исключения
├── models/
│   ├── descriptors.py        # Data/non-data дескрипторы
│   ├── task.py               # Доменная модель Task
│   ├── task_contract.py      # Протоколы источников (TaskContract, AsyncTaskContract)
│   ├── task_handler.py       # Протокол обработчика задач (TaskHandlerProtocol)
│   ├── task_mapper.py        # Маппинг dict -> Task
│   ├── task_states.py        # Статусы задачи (Enum)
│   └── task_stream.py        # Повторно итерируемый поток задач
├── handlers/
│   ├── task_handler.py       # Конкретная реализация обработчика задач
│   └── task_handler_protocol.py  # Протокол обработчика
├── resources/
│   ├── api_resource.py       # Асинхронный источник (API-заглушка)
│   ├── file_resource.py      # Асинхронный источник из JSON
│   ├── generator_resource.py # Асинхронный генератор задач
│   └── multi_task_resource.py# Композитный асинхронный источник
├── task_queue.py             # Асинхронный исполнитель с пулом воркеров
└── main.py                   # Точка входа (async)
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

#### TaskHandlerProtocol

```python
class TaskHandlerProtocol(Protocol):
    async def handle(self, task: Task) -> None:
        """Обрабатывает одну задачу асинхронно"""
        ...
```

#### TaskQueue

`TaskQueue` — это лениво итерируемая коллекция задач, которая позволяет строить цепочки фильтров. Она использует
`TaskStream` для получения данных.

`TaskQueue` имеет асинхронную итерацию, а также может асинхронно обрабатывать задачи используя класс поддерживающий
`TaskHandlerProtocol`.

**Фильтрация**: Методы `filter()`, `filter_by_state()` и `filter_by_priority()` возвращают новый экземпляр `TaskQueue`
с добавленным условием, не выполняя реальной фильтрации до начала итерации.

#### Источники задач

Все источники задач используют единый асинхронный интерфейс (также есть синхронный):

```python
@runtime_checkable
class AsyncTaskContract(Protocol):
    async def __aenter__(self) -> "AsyncTaskContract":
        """Открывает ресурс (инициализация, подключение и т.д.)"""
        ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Закрывает ресурс (очистка, отключение и т.д.)"""
        ...

    async def get_tasks(self) -> AsyncGenerator[Task, None]:
        """Возвращает асинхронный генератор задач"""
        ...
```

Реализованные источники:

- `FileTaskResource` - читает JSON (один объект или список объектов).
- `GeneratorTaskResource` - генерирует задачи на основе `TASK_TEXT_SAMPLE`.
- `ApiTaskResource` - имитирует API-ответ и возвращает задачи.
- `MultiTaskResource` - источник, который объединяет несколько других источников в один.

Преобразование словарей задач в объекты **Task** происходит с помощью **TaskMapper** и метода **to_task**.
