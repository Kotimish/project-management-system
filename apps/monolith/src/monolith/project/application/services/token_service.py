from monolith.project.application.dto.token import TokenDTO
from monolith.project.application.exceptions import api_client_exception as exceptions
from monolith.project.application.interfaces.client import IApiClient
from monolith.project.application.interfaces.services.token_service import ITokenService


class TokenService(ITokenService):
    """Реализация сервиса проверки токена"""

    def __init__(self, auth_client: IApiClient):
        self.auth_client = auth_client

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
