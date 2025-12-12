from monolith.auth.domain.exceptions.base_exception import BaseAuthException


class UserException(BaseAuthException):
    """Базовое исключение для модели пользователь"""


class InvalidUserLoginException(UserException):
    """Исключение для некорректного логина пользователя"""


class InvalidUserEmailException(UserException):
    """Исключение для некорректной почты пользователя"""


class InvalidUserPasswordException(UserException):
    """Исключение для некорректного пароля пользователя"""
