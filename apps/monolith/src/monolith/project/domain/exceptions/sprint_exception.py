from monolith.project.domain.exceptions.base_exception import BaseProjectException


class SprintException(BaseProjectException):
    """Базовое исключение для доменной модели Спринт"""


class InvalidSprintNameException(SprintException):
    """"Исключение для некорректного или отсутствующего имени спринта"""


class InvalidProjectIdException(SprintException):
    """"Исключение для некорректного или отсутствующего id проекта"""


class InvalidSpingDateException(SprintException):
    """"Исключение для некорректных или отсутствующих дат спринта"""


class SprintNotFoundError(SprintException):
    """Исключение для несуществующего Спринта"""


class SprintUnauthorizedError(SprintException):
    """Исключение при попытке получения доступа к Спринту без соответствующих прав"""

