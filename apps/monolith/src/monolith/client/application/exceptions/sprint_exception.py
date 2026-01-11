from monolith.client.application.exceptions.base_exception import BaseClientException


class SprintException(BaseClientException):
    """Базовое исключение для доменной модели Спринт"""


class SprintNotFoundError(SprintException):
    """Исключение для несуществующего Спринта"""


class SprintCannotBeDeletedException(SprintException):
    """Исключение при невозможности удалить спринт из-за связанных сущностей"""
