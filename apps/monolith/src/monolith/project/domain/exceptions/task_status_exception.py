from monolith.project.domain.exceptions.base_exception import BaseProjectException


class TaskStatusException(BaseProjectException):
    """Базовое исключение для доменной модели статус задачи"""


class InvalidTaskStatusNameException(TaskStatusException):
    """Исключение для некорректного или отсутствующего названия статуса задачи"""


class InvalidTaskStatusSlugException(TaskStatusException):
    """Исключение для некорректного или отсутствующего сокращенного названия статуса задачи"""


class TaskStatusNotFoundError(TaskStatusException):
    """Исключение для несуществующего Статус Задачи"""
