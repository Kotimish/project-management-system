from monolith.project.domain.exceptions.base_exception import BaseProjectException


class ParticipantException(BaseProjectException):
    """Базовое исключение для доменной модели Участники проекта"""


class InvalidProjectAuthUserIdException(BaseProjectException):
    """Исключение для некорректного или отсутствующего id участника"""


class InvalidProjectProjectIdException(BaseProjectException):
    """Исключение для некорректного или отсутствующего id проекта"""


class ParticipantNotFoundError(ParticipantException):
    """Исключение для несуществующего Участника проекта"""


class ParticipantCannotBeDeletedException(ParticipantException):
    """Исключение при невозможности удалить Участника проекта из-за связанных сущностей"""
