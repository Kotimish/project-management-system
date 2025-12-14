
from monolith.client.application.dtos import user as dto
from monolith.client.application.dtos.token import TokenDTO
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.auth_service import IAuthService
from monolith.client.application.exceptions import api_client_exception as exceptions


class AuthService(IAuthService):
    """Интерфейс сервиса авторизации"""

    def __init__(self, auth_client: IApiClient):
        self.auth_client = auth_client

    async def register(self, data: dto.CreateUserCommand) -> dto.CreateUserResponse:
        json_data = {
            "login": data.login,
            "email": data.email,
            "password": data.password.get_secret_value()
        }
        response = await self.auth_client.post(
            endpoint="/api/auth/register",
            json=json_data
        )
        user = dto.CreateUserResponse.model_validate(response)
        return user

    async def login(self, data: dto.LoginUserCommand) -> dto.LoginUserResponse:
        json_data = {
            "login": data.login,
            "password": data.password.get_secret_value()
        }
        response = await self.auth_client.post(
            endpoint="/api/auth/login",
            json=json_data
        )
        tokens = dto.LoginUserResponse.model_validate(response)
        return tokens

    async def logout(self, refresh_token: str) -> bool:
        headers = {
            "Authorization": f"Bearer {refresh_token}"
        }
        try:
            await self.auth_client.post(
                endpoint="/api/auth/logout",
                headers=headers
            )
            return True
        except exceptions.HTTPStatusError:
            return False

    async def validate_token(self, access_token: str) -> TokenDTO | None:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            response = await self.auth_client.get(
                endpoint="/api/auth/validate",
                headers=headers
            )
            return TokenDTO.model_validate(response)
        except exceptions.HTTPStatusError:
            return None
