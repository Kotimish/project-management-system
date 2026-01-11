from monolith.client.application.exceptions.base_exception import BaseClientException


class ApiClientException(BaseClientException):
    """Базовое исключение для api-клиента"""


class HTTPStatusError(BaseClientException):
    """Исключение при получении статуса 4xx или 5xx"""


class RequestError(BaseClientException):
    """Базовый класс для всех исключений, которые могут возникнуть при выполнении метода `request`"""
