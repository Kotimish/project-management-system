from monolith.client.application.dtos import user as user_models
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.client_service import IClientService
from monolith.client.application.exceptions import api_client_exception as exceptions


class ClientService(IClientService):
    """Реализация клиент сервиса"""

    def __init__(self, auth_client: IApiClient):
        self.auth_client = auth_client

    async def register(self, data: user_models.CreateUserCommand) -> user_models.CreateUserResponse:
        json_data = {
            "login": data.login,
            "email": data.email,
            "password": data.password.get_secret_value()
        }
        response = await self.auth_client.post(
            endpoint="/api/auth/register",
            json=json_data
        )
        user = user_models.CreateUserResponse.model_validate(response)
        return user

    async def login(self, data: user_models.LoginUserCommand) -> user_models.LoginUserResponse:
        json_data = {
            "login": data.login,
            "password": data.password.get_secret_value()
        }
        response = await self.auth_client.post(
            endpoint="/api/auth/login",
            json=json_data
        )
        tokens = user_models.LoginUserResponse.model_validate(response)
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
