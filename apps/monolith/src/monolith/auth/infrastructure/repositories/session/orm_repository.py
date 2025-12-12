from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from monolith.auth.domain.interfaces.repositories.session_repository import ISessionRepository
from monolith.auth.infrastructure.models import Session as ORMSession
from monolith.auth.domain.model import Session


class ORMSessionRepository(ISessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, session: Session) -> Session:
        orm_session = ORMSession(
            user_id = session.user_id,
            expires_at = session.expires_at
        )
        self.session.add(orm_session)
        await self.session.commit()
        await self.session.refresh(orm_session)
        # Обновление полей доменной модели
        session.id = orm_session.id
        session.created_at = orm_session.created_at
        session.updated_at = orm_session.updated_at
        session.revoked_at = orm_session.revoked_at
        return session

    async def _get_by_id(self, session_id: int) -> ORMSession | None:
        return await self.session.get(ORMSession, session_id)

    async def get_by_id(self, session_id: int) -> Session | None:
        orm_session = await self._get_by_id(session_id)
        if not orm_session:
            return None
        return Session(
            session_id = orm_session.id,
            user_id = orm_session.user_id,
            created_at = orm_session.created_at,
            updated_at=orm_session.updated_at,
            expires_at = orm_session.expires_at,
            revoked_at=orm_session.revoked_at
        )

    async def get_all(self) -> list[Session]:
        statement = select(ORMSession).order_by(ORMSession.id)
        result = await self.session.scalars(statement)
        orm_sessions = result.all()
        return [
            Session(
                session_id=orm_session.id,
                user_id=orm_session.user_id,
                created_at=orm_session.created_at,
                updated_at=orm_session.updated_at,
                expires_at=orm_session.expires_at,
                revoked_at=orm_session.revoked_at
            )
            for orm_session in orm_sessions
        ]

    async def update(self, session_id: int, session: Session) -> Session | None:
        orm_session = await self._get_by_id(session_id)
        if not orm_session:
            return None
        # Обновляем поля ORM-модели полями доменной модели
        orm_session.updated_at = session.updated_at
        orm_session.expires_at = session.expires_at
        orm_session.revoked_at = session.revoked_at

        await self.session.commit()
        await self.session.refresh(orm_session)
        return Session(
            session_id=orm_session.id,
            user_id=orm_session.user_id,
            created_at=orm_session.created_at,
            updated_at=orm_session.updated_at,
            expires_at=orm_session.expires_at,
            revoked_at=orm_session.revoked_at
        )

    async def remove(self, session_id: int) -> bool:
        orm_session = await self._get_by_id(session_id)
        if not orm_session:
            return False
        await self.session.delete(orm_session)
        await self.session.commit()
        return True
