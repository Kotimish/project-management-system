from monolith.project.application.interfaces.factories.participant_factory import IParticipantFactory
from monolith.project.domain.model import Participant


class ParticipantFactory(IParticipantFactory):
    """Фабрика участников проекта"""

    def create(self, project_id: int, user_id: int) -> Participant:
        return Participant(
            auth_user_id=user_id,
            project_id=project_id,
        )
