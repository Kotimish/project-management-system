from datetime import timezone, datetime, timedelta

from monolith.auth.application.interfaces.factories.session_factory import ISessionFactory
from monolith.auth.application.interfaces.services.session_service import ISessionService
from monolith.auth.domain.interfaces.repositories.session_repository import ISessionRepository
from monolith.auth.domain.model.session import Session
from monolith.auth.domain.model.user import User
from monolith.config.auth_config import AuthConfig


class SessionService(ISessionService):
    """Сервис работы с сессиями пользователей"""

    def __init__(
            self,
            factory: ISessionFactory,
            repository: ISessionRepository,
            config: AuthConfig
    ):
        self.factory = factory
        self.repository = repository
        self.config = config

    async def create_session(self, user: User) -> Session:
        expire_at = datetime.now() + timedelta(minutes=self.config.refresh_token_expire_minutes)
        session = self.factory.create(user, expire_at)
        session = await self.repository.add(session)
        return session

    async def get_session_by_id(self, session_id: int) -> Session | None:
        return await self.repository.get_by_id(session_id)

    async def revoke_session(self, session_id: int) -> bool:
        session = await self.get_session_by_id(session_id)
        if not session:
            return False
        session.revoked_at = datetime.now()
        await self.repository.update(session.id, session)
        return True

    async def delete_session(self, session_id: int) -> bool:
        raise await self.repository.remove(session_id)
