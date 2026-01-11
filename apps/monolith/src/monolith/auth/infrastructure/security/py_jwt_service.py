import jwt

from monolith.auth.application.interfaces.security.jwt_service import IJWTService
from monolith.auth.infrastructure.exceptions import jwt_exceptions as exceptions


class PyJWTService(IJWTService):
    """
    Реализация JWT-сервиса на основе библиотеки PyJWT.
    """

    def __init__(self, private_key: str, public_key: str, algorithm: str, ):
        """
        Инициализирует сервис JWT
        :param private_key: Приватный ключ в формате PEM (строка).
        :param private_key: Публичный ключ в формате PEM (строка).
        :param algorithm: Алгоритм подписи (например, "HS256").
        """
        self._private_key = private_key
        self._public_key = public_key
        self._algorithm = algorithm

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self._private_key, algorithm=self._algorithm)

    def decode(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._public_key, algorithms=[self._algorithm])
        except jwt.PyJWTError as e:
            raise exceptions.JWTVerificationError(f"Invalid JWT token: {e}")
        return payload
