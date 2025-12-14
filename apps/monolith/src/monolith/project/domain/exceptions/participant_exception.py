from monolith.project.domain.exceptions.base_exception import BaseProjectException


class ParticipantException(BaseProjectException):
    """Базовое исключение для доменной модели Участники"""


class InvalidProjectAuthUserIdException(BaseProjectException):
    """Исключение для некорректного или отсутствующего id участника"""


class InvalidProjectProjectIdException(BaseProjectException):
    """Исключение для некорректного или отсутствующего id проекта"""
