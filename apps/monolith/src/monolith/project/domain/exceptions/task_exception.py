from monolith.project.domain.exceptions.base_exception import BaseProjectException


class TaskException(BaseProjectException):
    """Базовое исключение для доменной модели Задача"""


class InvalidTaskTitleException(TaskException):
    """Исключение для некорректного или отсутствующего названия задачи"""


class InvalidProjectIdException(TaskException):
    """Исключение для некорректного или отсутствующего id проекта"""


class InvalidStatusIdException(TaskException):
    """Исключение для некорректного или отсутствующего id статуса проекта задачи"""


class InvalidAssigneeIdException(TaskException):
    """Исключение для некорректного или отсутствующего id ответственного"""


class InvalidSpringIdException(TaskException):
    """Исключение для некорректного или отсутствующего id спринта проекта"""


class TaskNotFoundError(TaskException):
    """Исключение для несуществующей Задачи"""


class TaskUnauthorizedError(TaskException):
    """Исключение при попытке получения доступа к Задаче без соответствующих прав"""


class TaskCannotBeDeletedException(TaskException):
    """Исключение при невозможности удалить задачу из-за связанных сущностей"""
