from pydantic import BaseModel


class ProjectTeamDTO(BaseModel):
    """Агрегат данные для отображения информации об участниках проекта"""
    profile_id: int
    participant_id: int
    auth_user_id: int
    display_name: str
    first_name: str | None
    middle_name: str | None
    last_name: str | None
