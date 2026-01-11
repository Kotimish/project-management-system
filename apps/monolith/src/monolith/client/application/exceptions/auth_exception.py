from monolith.client.application.exceptions.base_exception import BaseClientException


class AuthException(BaseClientException):
    """Базовое исключение для авторизации и аутентификации"""


class InvalidAuthLoginException(BaseClientException):
    """Исключение для некорректно формата логина при регистрации"""


class InvalidAuthEmailException(BaseClientException):
    """Исключение для некорректно формата почты при регистрации"""


class AuthUnauthorizedException(BaseClientException):
    """Исключение для некорректно веденной комбинации логина и пароля при входе"""
