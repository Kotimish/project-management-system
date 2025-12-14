from monolith.project.domain.exceptions.base_exception import BaseProjectException


class ApiClientException(BaseProjectException):
    """Базовое исключение для api-клиента"""


class HTTPStatusError(BaseProjectException):
    """Исключение при получении статуса 4xx или 5xx"""


class RequestError(BaseProjectException):
    """Базовый класс для всех исключений, которые могут возникнуть при выполнении метода `request`"""
