from monolith.client.application.dtos import user as user_models
from monolith.client.application.dtos import user_profile as profile_models
from monolith.client.application.dtos.user_profile import GetUserProfileResponse
from monolith.client.application.interfaces.services.auth_service import IAuthService
from monolith.client.application.interfaces.services.client_service import IClientService
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService


class ClientService(IClientService):
    """Реализация клиент сервиса"""

    def __init__(self, auth_service: IAuthService, user_profile_service: IUserProfileService):
        self.auth_service = auth_service
        self.user_profile_service = user_profile_service

    async def register(self, data: user_models.CreateUserCommand) -> user_models.CreateUserResponse:
        auth_user = await self.auth_service.register(data)
        profile_data = profile_models.CreateUserProfileCommand(
            auth_user_id=auth_user.id,
            display_name=auth_user.login
        )
        user_profile = await self.user_profile_service.create_profile(profile_data)
        return auth_user

    async def login(self, data: user_models.LoginUserCommand) -> user_models.LoginUserResponse:
        return await self.auth_service.login(data)

    async def logout(self, refresh_token: str) -> bool:
        return await self.auth_service.logout(refresh_token)

    async def get_current_user(self, access_token: str) -> GetUserProfileResponse | None:
        token = await self.auth_service.validate_token(access_token)
        if token is None:
            return None
        user_profile = await self.user_profile_service.get_profile_by_auth_user_id(token.sub)
        return user_profile

