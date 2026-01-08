
from monolith.client.application.dtos import user_profile as dto
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService
from monolith.client.application.exceptions import api_client_exception as exceptions


class UserProfileService(IUserProfileService):
    """Реализация сервиса профиля пользователя"""
    def __init__(self, user_profile_client: IApiClient):
        self.user_profile_client = user_profile_client

    async def create_profile(
            self,
            data: dto.CreateUserProfileCommand
    ) -> dto.CreateUserProfileResponse | None:
        try:
            response = await self.user_profile_client.post(
                "/api/user_profile/",
                json=data.model_dump(mode='json')
            )
            return dto.CreateUserProfileResponse.model_validate(response)
        except exceptions.HTTPStatusError:
            return None

    async def get_profile_by_id(self, profile_id: int) -> dto.UserProfileDTO | None:
        try:
            response = await self.user_profile_client.get(
                f"/api/user_profile/{profile_id}"
            )
            return dto.UserProfileDTO.model_validate(response)
        except exceptions.HTTPStatusError:
            return None

    async def get_profiles_by_auth_user_ids(self, auth_user_ids: list[int]) -> list[dto.UserProfileDTO]:
        if not auth_user_ids:
            return []
        data = dto.UserProfilesRequest(
            ids=auth_user_ids
        )
        try:
            raw_profiles = await self.user_profile_client.post(
                f"/api/user_profile/by_auth_user_id",
                json=data.model_dump(mode='json')
            )
            return [
                dto.UserProfileDTO.model_validate(raw_profile)
                for raw_profile in raw_profiles
            ]
        except exceptions.HTTPStatusError:
            return []

    async def get_profile_by_auth_user_id(self, auth_user_id: int) -> dto.UserProfileDTO | None:
        try:
            response = await self.user_profile_client.get(
                f"/api/user_profile/by_auth_user_id/{auth_user_id}"
            )
            return dto.UserProfileDTO.model_validate(response)
        except exceptions.HTTPStatusError:
            return None

    async def update_profile(
            self,
            profile_id: int,
            data: dto.UpdateUserProfileCommand,
            access_token: str
    ) -> dto.UpdateUserProfileResponse | None:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            response = await self.user_profile_client.patch(
                f"/api/user_profile/{profile_id}",
                headers=headers,
                json=data.model_dump(mode='json')
            )
            return dto.UpdateUserProfileResponse.model_validate(response)
        except exceptions.HTTPStatusError:
            return None
