from monolith.user_profile.application.dtos import user_profile as dto
from monolith.user_profile.application.interfaces.factories import IUserProfileFactory
from monolith.user_profile.application.interfaces.services import IUserProfileService
from monolith.user_profile.domain.interfaces.repositories import IUserProfileRepository


class UserProfileService(IUserProfileService):
    """Реализация сервиса работы с профилем пользователей"""

    def __init__(self, factory: IUserProfileFactory, repository: IUserProfileRepository):
        self.factory = factory
        self.repository = repository

    async def create_profile(self, data: dto.CreateUserProfileCommand) -> dto.CreateUserProfileResponse:
        profile = self.factory.create(data)
        profile = await self.repository.add(profile)
        return dto.CreateUserProfileResponse(
            id=profile.id
        )

    async def get_profile_by_id(self, profile_id: int) -> dto.GetUserProfileResponse | None:
        profile = await self.repository.get_by_id(profile_id)
        if profile is None:
            return None
        return dto.GetUserProfileResponse(
            id=profile.id,
            auth_user_id=profile.auth_user_id,
            display_name=profile.display_name,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            first_name=profile.first_name,
            middle_name=profile.middle_name,
            last_name=profile.last_name,
            description=profile.description,
            birthdate=profile.birthdate,
            phone=profile.phone
        )

    async def get_profile_by_auth_user_id(self, auth_user_id: int) -> dto.GetUserProfileResponse | None:
        profile = await self.repository.get_by_auth_user_id(auth_user_id)
        if profile is None:
            return None
        return dto.GetUserProfileResponse(
            id=profile.id,
            auth_user_id=profile.auth_user_id,
            display_name=profile.display_name,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            first_name=profile.first_name,
            middle_name=profile.middle_name,
            last_name=profile.last_name,
            description=profile.description,
            birthdate=profile.birthdate,
            phone=profile.phone
        )

    async def get_profiles_by_auth_user_ids(self, auth_user_ids: list[int]) -> list[dto.GetUserProfileResponse]:
        if not auth_user_ids:
            return []
        profiles = await self.repository.get_by_auth_user_ids(auth_user_ids)
        return [
            dto.GetUserProfileResponse(
                id=profile.id,
                auth_user_id=profile.auth_user_id,
                display_name=profile.display_name,
                created_at=profile.created_at,
                updated_at=profile.updated_at,
                first_name=profile.first_name,
                middle_name=profile.middle_name,
                last_name=profile.last_name,
                description=profile.description,
                birthdate=profile.birthdate,
                phone=profile.phone
            )
            for profile in profiles
        ]

    async def update_profile(
            self,
            profile_id: int,
            data: dto.UpdateUserProfileCommand
    ) -> dto.UpdateUserProfileResponse | None:
        profile = await self.repository.get_by_id(profile_id)
        if profile is None:
            return None
        if data.display_name is not None:
            profile.update_display_name(data.display_name)
        if data.first_name is not None or data.middle_name is not None or data.last_name is not None:
            profile.update_personal_info(data.first_name, data.middle_name, data.last_name)
        if data.description is not None:
            profile.update_description(data.description)
        if data.phone is not None:
            profile.update_contact_info(data.phone)
        if data.birthdate is not None:
            profile.update_secondary_info(data.birthdate)
        await self.repository.update(profile_id, profile)
        return dto.UpdateUserProfileResponse(
            id=profile.id
        )
