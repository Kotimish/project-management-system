from monolith.client.application.dtos import participant as dto
from monolith.client.application.interfaces.client import IApiClient
from monolith.client.application.interfaces.services.participant_service import IParticipantService
from monolith.client.application.exceptions import api_client_exception as exceptions


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
        except exceptions.HTTPStatusError:
            return []
