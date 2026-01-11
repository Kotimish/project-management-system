from monolith.client.application.dtos import participant as dto
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.participant_service import IParticipantService
from monolith.client.application.exceptions import api_client_exception as api_exceptions
from monolith.client.application.exceptions import participant_exception as exceptions


class ParticipantService(IParticipantService):
    """Реализация сервиса участников проекта"""

    def __init__(self, project_client: IApiClient):
        self.project_client = project_client

    async def get_participants_by_project(self, project_id: int) -> list[dto.ParticipantDTO]:
        try:
            raw_participants = await self.project_client.get(
                f"/api/projects/{project_id}/participants",
            )
            participants = [
                dto.ParticipantDTO.model_validate(raw_participant)
                for raw_participant in raw_participants
            ]
            return participants
        except api_exceptions.HTTPStatusError:
            return []


    async def add_participant_to_project(
            self,
            project_id: int,
            user_id: int,
            access_token: str
    ) -> dto.ParticipantDTO | None:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            raw_participant = await self.project_client.post(
                f"/api/projects/{project_id}/participants/{user_id}",
                headers=headers,
            )
            return dto.ParticipantDTO.model_validate(raw_participant)
        except api_exceptions.HTTPStatusError as exception:
            if exception.status_code == 403:
                raise exceptions.ParticipantForbiddenException(
                    "User do not have permission to modify this resource"
                )
            return None

    async def remove_participant_from_project(self, project_id: int, user_id: int, access_token: str) -> None:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        try:
            await self.project_client.delete(
                f"/api/projects/{project_id}/participants/{user_id}",
                headers=headers,
            )
        except api_exceptions.HTTPStatusError as exception:
            if exception.status_code == 409:
                raise exceptions.ParticipantCannotBeDeletedException(
                    "Participant has tasks in the project"
                )
            if exception.status_code == 404:
                raise exceptions.ParticipantNotFoundError(
                    "Participant not found in the project"
                )
            if exception.status_code == 403:
                raise exceptions.ParticipantForbiddenException(
                    "User do not have permission to modify this resource"
                )
