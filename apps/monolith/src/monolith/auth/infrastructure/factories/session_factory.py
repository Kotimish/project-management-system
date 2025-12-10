from datetime import datetime

from monolith.auth.application.interfaces.factories.session_factory import ISessionFactory
from monolith.auth.domain.model.session import Session
from monolith.auth.domain.model.user import User


class SessionFactory(ISessionFactory):
    """Интерфейс фабрики сессии пользователя"""
    def create(self, user: User, expires_at: datetime) -> Session:
        return Session(
            user_id=user.id,
            expires_at=expires_at
        )
