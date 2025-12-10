from abc import ABC, abstractmethod
from datetime import datetime

from monolith.auth.domain.model.session import Session
from monolith.auth.domain.model.user import User


class ISessionFactory(ABC):
    """Интерфейс фабрики сессии пользователя"""
    @abstractmethod
    def create(self, user: User, expires_at: datetime) -> Session:
        raise NotImplementedError
