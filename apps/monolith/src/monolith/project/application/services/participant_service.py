from monolith.project.application.dto import participant as dto
from monolith.project.application.interfaces.factories.participant_factory import IParticipantFactory
from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.domain.interfaces.repositories.participant import IParticipantRepository
from monolith.project.domain.model import Participant
from monolith.project.domain.exceptions import participant_exception as exceptions


class ParticipantService(IParticipantService):
    """Реализация сервиса участников проекта"""

    def __init__(
            self,
            factory: IParticipantFactory,
            repository: IParticipantRepository
    ):
        self.factory = factory
        self.repository = repository

    async def add_participant(self, project_id: int, user_id: int) -> dto.ParticipantDTO:
        participant = self.factory.create(project_id, user_id)
        participant = await self.repository.add(participant)
        return dto.ParticipantDTO(
            id=participant.id,
            auth_user_id=participant.auth_user_id,
            project_id=participant.project_id,
        )

    async def get_participants_by_project(self, project_id: int) -> list[dto.ParticipantDTO]:
        participants = await self.repository.get_all_by_project_id(project_id)
        return [
            dto.ParticipantDTO(
                id=participant.id,
                auth_user_id=participant.auth_user_id,
                project_id=participant.project_id,
            )
            for participant in participants
        ]

    async def remove_participant(self, project_id: int, user_id: int):
        status = await self.repository.remove_by_auth_user_and_project(user_id, project_id)
        if not status:
            raise exceptions.ParticipantNotFoundError(
                "Participant not found in the project"
            )
