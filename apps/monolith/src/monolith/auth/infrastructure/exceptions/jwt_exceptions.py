from monolith.auth.domain.exceptions.base_exception import BaseAuthException


class JWTException(BaseAuthException):
    """Базовое исключение для JWS."""


class JWTVerificationError(JWTException):
    """Ошибка верификации JWT-токена."""
