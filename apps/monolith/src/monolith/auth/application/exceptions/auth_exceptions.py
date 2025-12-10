from monolith.auth.domain.exceptions.base_exception import BaseAuthException


class AuthException(BaseAuthException):
    """Исключение для ошибок авторизации"""


class InvalidPasswordException(AuthException):
    """Исключение для неверного пароля"""


class InvalidLoginException(AuthException):
    """Исключение для неверно веденного логина (отсутствует в системе)"""


class InactiveUserException(AuthException):
    """Исключение для деактивированного пользователя"""


class InvalidSessionException(AuthException):
    """Исключение для несуществующей сессии пользователя"""


class InactiveSessionException(AuthException):
    """Исключение для деактивированной сессии пользователя"""

class InvalidRoleException(AuthException):
    """Исключение для несуществующей роли пользователя"""
