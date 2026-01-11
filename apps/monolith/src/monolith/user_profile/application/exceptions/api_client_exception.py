from monolith.user_profile.application.exceptions.base_exception import BaseUserProfileException


class ApiClientException(BaseUserProfileException):
    """Базовое исключение для api-клиента"""


class HTTPStatusError(BaseUserProfileException):
    """Исключение при получении статуса 4xx или 5xx"""


class RequestError(BaseUserProfileException):
    """Базовый класс для всех исключений, которые могут возникнуть при выполнении метода `request`"""
