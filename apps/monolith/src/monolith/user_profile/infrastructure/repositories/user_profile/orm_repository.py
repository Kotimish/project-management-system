from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from monolith.user_profile.domain.interfaces.repositories import IUserProfileRepository
from monolith.user_profile.domain.model import UserProfile
from monolith.user_profile.infrastructure.models import UserProfile as ORMUserProfile


class ORMUserProfileRepository(IUserProfileRepository):
    """Реализация репозитория для профилей пользователей."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, profile: UserProfile) -> UserProfile:
        orm_profile = ORMUserProfile(
            auth_user_id=profile.auth_user_id,
            display_name=profile.display_name,
            first_name=profile.first_name,
            middle_name=profile.middle_name,
            last_name=profile.last_name,
            description=profile.description,
            birthdate=profile.birthdate,
            phone=profile.phone
        )
        self.session.add(orm_profile)
        await self.session.commit()
        await self.session.refresh(orm_profile)
        # Обновление полей доменной модели
        profile.id = orm_profile.id
        profile.created_at = orm_profile.created_at
        profile.updated_at = orm_profile.updated_at
        return profile

    async def _get_by_id(self, profile_id: int) -> ORMUserProfile | None:
        return await self.session.get(ORMUserProfile, profile_id)

    async def get_by_id(self, profile_id: int) -> UserProfile | None:
        orm_profile = await self._get_by_id(profile_id)
        if not orm_profile:
            return None
        return UserProfile(
            auth_user_id=orm_profile.auth_user_id,
            display_name=orm_profile.display_name,
            first_name=orm_profile.first_name,
            middle_name=orm_profile.middle_name,
            last_name=orm_profile.last_name,
            description=orm_profile.description,
            birthdate=orm_profile.birthdate,
            phone=orm_profile.phone
        )

    async def get_by_auth_user_id(self, auth_user_id: int) -> UserProfile | None:
        statement = select(ORMUserProfile).where(ORMUserProfile.auth_user_id == auth_user_id)
        result = await self.session.execute(statement)
        orm_profile = result.scalar_one_or_none()
        if not orm_profile:
            return None
        return UserProfile(
            auth_user_id=orm_profile.auth_user_id,
            display_name=orm_profile.display_name,
            first_name=orm_profile.first_name,
            middle_name=orm_profile.middle_name,
            last_name=orm_profile.last_name,
            description=orm_profile.description,
            birthdate=orm_profile.birthdate,
            phone=orm_profile.phone
        )

    async def get_all(self) -> list[UserProfile]:
        statement = select(ORMUserProfile).order_by(ORMUserProfile.id)
        result = await self.session.scalars(statement)
        orm_profiles = result.all()
        return [
            UserProfile(
                auth_user_id=orm_profile.auth_user_id,
                display_name=orm_profile.display_name,
                first_name=orm_profile.first_name,
                middle_name=orm_profile.middle_name,
                last_name=orm_profile.last_name,
                description=orm_profile.description,
                birthdate=orm_profile.birthdate,
                phone=orm_profile.phone,
            )
            for orm_profile in orm_profiles
        ]

    async def update(self, profile_id: int, profile: UserProfile) -> UserProfile | None:
        orm_profile = await self._get_by_id(profile_id)
        if not orm_profile:
            return None
        # Обновляем поля ORM-модели полями доменной модели
        orm_profile.display_name = profile.display_name
        orm_profile.first_name = profile.first_name
        orm_profile.middle_name = profile.middle_name
        orm_profile.last_name = profile.last_name
        orm_profile.description = profile.description
        orm_profile.birthdate = profile.birthdate
        orm_profile.phone = profile.phone

        await self.session.commit()
        await self.session.refresh(orm_profile)
        return UserProfile(
            auth_user_id=orm_profile.auth_user_id,
            display_name=orm_profile.display_name,
            first_name=orm_profile.first_name,
            middle_name=orm_profile.middle_name,
            last_name=orm_profile.last_name,
            description=orm_profile.description,
            birthdate=orm_profile.birthdate,
            phone=orm_profile.phone
        )

    async def remove(self, profile_id: int) -> bool:
        orm_profile = await self._get_by_id(profile_id)
        if not orm_profile:
            return False
        await self.session.delete(orm_profile)
        await self.session.commit()
        return True
