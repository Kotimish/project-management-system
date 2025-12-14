from monolith.project.application.interfaces.factories.participant_factory import IParticipantFactory
from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.domain.interfaces.repositories.participant import IParticipantRepository
from monolith.project.domain.model import Participant


class ParticipantService(IParticipantService):
    """Реализация сервиса участников проекта"""

    def __init__(
            self,
            factory: IParticipantFactory,
            repository: IParticipantRepository
    ):
        self.factory = factory
        self.repository = repository

    async def add_participant(self, project_id: int, user_id: int) -> Participant:
        participant = self.factory.create(project_id, user_id)
        return await self.repository.add(participant)

    async def remove_participant(self, project_id: int, user_id: int) -> bool:
        return await self.repository.remove_by_auth_user_and_project(user_id, project_id)

    async def get_participants_by_project(self, project_id: int) -> list[Participant]:
        return await self.repository.get_all_by_project_id(project_id)
