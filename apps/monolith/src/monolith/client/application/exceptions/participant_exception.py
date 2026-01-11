from monolith.client.application.exceptions.base_exception import BaseClientException


class ParticipantException(BaseClientException):
    """Базовое исключение для модели Участники проекта"""


class ParticipantNotFoundError(ParticipantException):
    """Исключение для несуществующего Участника проекта"""


class ParticipantForbiddenException(ParticipantException):
    """Исключение при попытке получения доступа к участникам без соответствующих прав"""


class ParticipantCannotBeDeletedException(ParticipantException):
    """Исключение при невозможности удалить Участника проекта из-за связанных сущностей"""
