import re

from monolith.client.application.dtos import user as dto
from monolith.client.application.dtos.token import TokenDTO
from monolith.client.application.exceptions import api_client_exception as api_exceptions
from monolith.client.application.exceptions import auth_exception as exceptions
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.auth_service import IAuthService


def is_valid_login(login: str) -> bool:
    """Простая проверка логина через регулярное выражение"""
    pattern = r"^[A-Za-z0-9_]+$"
    return bool(re.match(pattern, login))

def is_valid_email(email: str) -> bool:
    """Простая проверка email через регулярное выражение"""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.match(pattern, email))


class AuthService(IAuthService):
    """Интерфейс сервиса авторизации"""

    def __init__(self, auth_client: IApiClient):
        self.auth_client = auth_client

    async def register(self, data: dto.CreateUserCommand) -> dto.CreateUserResponse | None:
        if not is_valid_login(data.login):
            raise exceptions.InvalidAuthLoginException("Invalid login")
        if not is_valid_email(data.email):
            raise exceptions.InvalidAuthEmailException("Invalid email")
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

    async def login(self, data: dto.LoginUserCommand) -> dto.LoginUserResponse | None:
        json_data = {
            "login": data.login,
            "password": data.password.get_secret_value()
        }
        try:
            response = await self.auth_client.post(
                endpoint="/api/auth/login",
                json=json_data
            )
            tokens = dto.LoginUserResponse.model_validate(response)
            return tokens
        except api_exceptions.HTTPStatusError as exception:
            if exception.status_code in {401, 403}:
                raise exceptions.AuthUnauthorizedException(
                    "User do not have permission"
                )

    async def refresh(self, refresh_token: str) -> dto.TokenResponse | None:
        headers = {
            "Authorization": f"Bearer {refresh_token}"
        }
        try:
            response = await self.auth_client.post(
                endpoint="/api/auth/refresh",
                headers=headers
            )
            token = dto.TokenResponse.model_validate(response)
            return token
        except api_exceptions.HTTPStatusError as exception:
            if exception.status_code in {401, 403}:
                raise exceptions.AuthUnauthorizedException(
                    "User do not have permission"
                )

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
        except api_exceptions.HTTPStatusError:
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
        except api_exceptions.HTTPStatusError:
            return None
