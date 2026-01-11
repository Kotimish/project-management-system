from monolith.project.domain.exceptions.base_exception import BaseProjectException


class TaskException(BaseProjectException):
    """Базовое исключение для доменной модели Задача"""


class TaskNotFoundError(TaskException):
    """Исключение для несуществующей Задачи"""


class TaskUnauthorizedError(TaskException):
    """Исключение при попытке получения доступа к Задаче без соответствующих прав"""


class TaskCannotBeDeletedException(TaskException):
    """Исключение при невозможности удалить задачу из-за связанных сущностей"""
