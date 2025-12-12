from monolith.auth.domain.exceptions.base_exception import BaseAuthException


class RoleException(BaseAuthException):
    """Базовое исключение для модели роль пользователя"""


class InvalidRoleNameException(RoleException):
    """Исключение для некорректного имени роли пользователя"""


class InvalidRoleSlugException(RoleException):
    """Исключение для некорректного сокращенного имени роли пользователя"""
