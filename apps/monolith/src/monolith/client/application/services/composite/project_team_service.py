from monolith.client.application.dtos.composite import project_team as dto
from monolith.client.application.interfaces.services.composite import IProjectTeamService
from monolith.client.application.interfaces.services.participant_service import IParticipantService
from monolith.client.application.interfaces.services.user_profile_service import IUserProfileService


class ProjectTeamService(IProjectTeamService):
    """Реализация агрегат сервиса участников проекта и их профилей"""

    def __init__(self, participant_service: IParticipantService, profile_service: IUserProfileService):
        self.participant_service = participant_service
        self.profile_service = profile_service

    async def get_participants_by_project(self, project_id: int) -> list[dto.ProjectTeamDTO]:
        # Запрос участников проекта
        participants = await self.participant_service.get_participants_by_project(project_id)
        # Запрос профилей участников проекта
        auth_user_ids = [
            participant.auth_user_id
            for participant in participants
        ]
        profiles = await self.profile_service.get_profiles_by_auth_user_ids(auth_user_ids)
        # Объединение информации
        result = []
        profiles_by_auth_user_id = {
            profile.auth_user_id: profile
            for profile in profiles
        }
        for participant in participants:
            profile = profiles_by_auth_user_id.get(participant.auth_user_id)
            if profile is not None:
                result.append(
                    dto.ProjectTeamDTO(
                        profile_id=profile.id,
                        participant_id=participant.id,
                        auth_user_id=profile.auth_user_id,
                        display_name=profile.display_name,
                        first_name=profile.first_name,
                        middle_name=profile.middle_name,
                        last_name=profile.last_name,
                    )
                )
        return result
