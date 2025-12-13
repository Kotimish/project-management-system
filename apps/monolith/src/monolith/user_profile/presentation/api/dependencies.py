from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import AsyncGenerator

from monolith.infrastructure.database import async_session
from monolith.user_profile.application.interfaces.services import IUserProfileService
from monolith.user_profile.application.services.user_profile_service import UserProfileService
from monolith.user_profile.domain.interfaces.repositories import IUserProfileRepository
from monolith.user_profile.infrastructure.factories.user_profile_factory import UserProfileFactory
from monolith.user_profile.infrastructure.repositories.user_profile.orm_repository import ORMUserProfileRepository


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


async def get_users_profile_repository(
        session: AsyncSession = Depends(get_async_session)
) -> IUserProfileRepository:
    return ORMUserProfileRepository(session)


def get_user_profile_service(
        repository=Depends(get_users_profile_repository),
) -> IUserProfileService:
    factory = UserProfileFactory()
    return UserProfileService(factory, repository)
