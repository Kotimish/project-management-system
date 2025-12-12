from abc import ABC, abstractmethod


class IJWTService(ABC):
    """
    Абстрактный интерфейс сервиса работы с JWT-токенами
    """
    @abstractmethod
    def encode(self, payload: dict) -> str:
        """
        Кодирует данные в JWT-токен
        :param payload: Набор кодируемых данных.
        :return: Подписанный JWT-токен в виде строки.
        """
        raise NotImplementedError

    @abstractmethod
    def decode(self, token: str) -> dict:
        """
        Декодирует и верифицирует JWT-токен.
        :param token: Подписанный JWT-токен.
        :return: Полезная нагрузка токена.
        """
        raise NotImplementedError
