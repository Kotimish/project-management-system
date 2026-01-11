from fastapi import Depends

from monolith.project.application.interfaces.services.participant_service import IParticipantService
from monolith.project.application.services.participant_service import ParticipantService
from monolith.project.infrastructure.factories.participant_factory import ParticipantFactory
from monolith.project.presentation.api.dependencies import get_participant_repository


def get_participant_service(
        repository=Depends(get_participant_repository)
) -> IParticipantService:
    factory = ParticipantFactory()
    return ParticipantService(
        repository=repository,
        factory=factory
    )
