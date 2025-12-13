from fastapi import Depends
from fastapi.requests import Request

from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.client_service import IClientService
from monolith.client.application.services.client_service import ClientService
from monolith.client.infrastructure.clients.http_client import HttpxApiClient


def get_auth_service_url() -> str:
    return "http://127.0.0.1:8000/"


def get_auth_api_client() -> IApiClient:
    url = get_auth_service_url()
    return HttpxApiClient(
        url=url
    )


def get_client_service() -> IClientService:
    auth_api_client = get_auth_api_client()
    return ClientService(
        auth_client=auth_api_client
    )


async def get_current_user(
        request: Request,
        client_service: IClientService = Depends(get_client_service)
) -> dict | None:
    access_token = request.cookies.get("access_token")
    if not access_token:
        return None
    user_info = {
        "sub": "Тестовый пользователь"
    }
    return user_info
