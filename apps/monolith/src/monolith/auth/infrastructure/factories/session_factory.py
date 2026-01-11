from datetime import datetime

from monolith.auth.application.interfaces.factories.session_factory import ISessionFactory
from monolith.auth.domain.model.session import Session
from monolith.auth.domain.model.user import User


class SessionFactory(ISessionFactory):
    """Интерфейс фабрики сессии пользователя"""
    def create(self, user: User, expires_at: datetime) -> Session:
        # Конвертация в формат для БД
        # if expires_at.tzinfo is not None and expires_at.tzinfo.utcoffset(expires_at) is not None:
        #     expires_at = expires_at.replace(tzinfo=None)
        return Session(
            user_id=user.id,
            expires_at=expires_at
        )
