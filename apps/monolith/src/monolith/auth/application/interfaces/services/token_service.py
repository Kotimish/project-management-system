from abc import ABC, abstractmethod

from monolith.auth.domain.model import Role, User, Session


class ITokenService(ABC):
    """Интерфейс сервиса работы с токенами пользователей"""
    @abstractmethod
    def create_access_token(self, user: User, role: Role) -> str:
        """Создание короткоживущего токена для доступа в другие сервисы"""
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(self, user: User, role: Role, session: Session) -> str:
        """Создание долгоживущего токена для обновления короткоживущего токена"""
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """Декодирование токена"""
        raise NotImplementedError
