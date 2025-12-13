from monolith.user_profile.domain.exceptions.base_exception import BaseProfileException


class UserProfileException(BaseProfileException):
    """Базовое исключение для модели профиль пользователя"""


class InvalidDisplayNameException(BaseProfileException):
    """Исключение для некорректного или отсутствующего отображаемого имени пользователя"""


class InvalidExternalIdException(BaseProfileException):
    """
    Исключение для некорректного или отсутствующего внешнего id пользователя из сервиса авторизации
    """
