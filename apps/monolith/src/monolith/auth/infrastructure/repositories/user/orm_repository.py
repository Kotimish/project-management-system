from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.testing.suite.test_reflection import users

from monolith.auth.domain.interfaces.repositories.user_repository import IUserRepository
from monolith.auth.infrastructure.models import User as ORMUser
from monolith.auth.domain.model import User


class ORMUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> User:
        orm_user = ORMUser(
            login = user.login,
            email = user.email,
            hashed_password = user.hashed_password,
            role_id = user.role_id

        )
        self.session.add(orm_user)
        await self.session.commit()
        await self.session.refresh(orm_user)
        # Обновление полей доменной модели
        user.id = orm_user.id
        user.created_at = orm_user.created_at
        user.updated_at = orm_user.updated_at
        user.revoked_at = orm_user.revoked_at
        return user

    async def _get_by_id(self, user_id: int) -> ORMUser | None:
        return await self.session.get(ORMUser, user_id)

    async def get_by_id(self, user_id: int) -> User | None:
        orm_user = await self._get_by_id(user_id)
        if not orm_user:
            return None
        return User(
            user_id=orm_user.id,
            login=orm_user.login,
            email=orm_user.email,
            hashed_password=orm_user.hashed_password,
            role_id=orm_user.role_id,
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at,
            revoked_at=orm_user.revoked_at,
        )

    async def get_by_login(self, login: str) -> User | None:
        statement = select(ORMUser).where(ORMUser.login == login)
        result = await self.session.execute(statement)
        orm_user = result.scalar_one_or_none()
        if not orm_user:
            return None
        return User(
            user_id=orm_user.id,
            login = orm_user.login,
            email = orm_user.email,
            hashed_password= orm_user.hashed_password,
            role_id = orm_user.role_id,
            created_at = orm_user.created_at,
            updated_at = orm_user.updated_at,
            revoked_at = orm_user.revoked_at,
        )

    async def get_all(self) -> list[User]:
        statement = select(ORMUser).order_by(ORMUser.id)
        result = await self.session.scalars(statement)
        orm_users = result.all()
        return [
            User(
                user_id=orm_user.id,
                login=orm_user.login,
                email=orm_user.email,
                hashed_password=orm_user.hashed_password,
                role_id=orm_user.role_id,
                created_at=orm_user.created_at,
                updated_at=orm_user.updated_at,
                revoked_at=orm_user.revoked_at,
            )
            for orm_user in orm_users
        ]

    async def update(self, user_id: int, user: User) -> User | None:
        orm_user = await self._get_by_id(user_id)
        if not orm_user:
            return None
        # Обновляем поля ORM-модели полями доменной модели
        orm_user.login = user.login
        orm_user.email = user.email
        orm_user.hashed_password = user.hashed_password
        orm_user.role_id = user.role_id
        orm_user.updated_at = user.updated_at
        orm_user.revoked_at = user.revoked_at

        await self.session.commit()
        await self.session.refresh(orm_user)
        return User(
            user_id=orm_user.id,
            login=orm_user.login,
            email=orm_user.email,
            hashed_password=orm_user.hashed_password,
            role_id=orm_user.role_id,
            created_at=orm_user.created_at,
            updated_at=orm_user.updated_at,
            revoked_at=orm_user.revoked_at,
        )

    async def remove(self, user_id: int) -> bool:
        orm_user = await self._get_by_id(user_id)
        if not orm_user:
            return False
        await self.session.delete(orm_user)
        await self.session.commit()
        return True