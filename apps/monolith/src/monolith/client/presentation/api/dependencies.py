from fastapi import Depends
from fastapi.requests import Request

from monolith.client.application.dtos import user_profile as dto
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.auth_service import IAuthService
from monolith.client.application.interfaces.services.client_service import IClientService
from monolith.client.application.interfaces.services.composite import IProjectTeamService
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService
from monolith.client.application.services.auth_service import AuthService
from monolith.client.application.services.client_service import ClientService
from monolith.client.application.services.composite import ProjectTeamService
from monolith.client.application.services.user_profile_service import UserProfileService
from monolith.client.infrastructure.clients.http_client import HttpxApiClient
from monolith.client.presentation.api.project.dependencies import get_participant_service
from monolith.config.settings import settings


def get_auth_api_client() -> IApiClient:
    return HttpxApiClient(
        url=str(settings.urls.auth_service)
    )


def get_user_profile_api_client() -> IApiClient:
    return HttpxApiClient(
        url=str(settings.urls.user_profile_service)
    )


def get_user_profile_service() -> IUserProfileService:
    user_profile_client = get_user_profile_api_client()
    return UserProfileService(user_profile_client)


def get_auth_service() -> IAuthService:
    auth_api_client = get_auth_api_client()
    return AuthService(auth_api_client)


def get_client_service() -> IClientService:
    auth_service = get_auth_service()
    user_profile_service = get_user_profile_service()
    return ClientService(
        auth_service=auth_service,
        user_profile_service=user_profile_service
    )


def get_participant_with_profile_service() -> IProjectTeamService:
    participant_service = get_participant_service()
    profile_service = get_user_profile_service()
    return ProjectTeamService(
        participant_service=participant_service,
        profile_service=profile_service,
    )


async def get_current_user(
        request: Request,
        client_service: IClientService = Depends(get_client_service)
) -> dto.UserProfileDTO | None:
    """
    Возвращает информацию о текущем пользователе из токена.
    При необходимости обновляет токен.
    """
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None
    user = await client_service.get_current_user(access_token)
    if not user:
        # TODO в случае отсутствия пользователя в access token обновить его через refresh token
        return None
    return user
