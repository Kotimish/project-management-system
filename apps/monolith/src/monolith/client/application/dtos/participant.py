from pydantic import BaseModel


class ParticipantDTO(BaseModel):
    """DTO для модели Участники проекта"""
    id: int
    auth_user_id: int
    project_id: int
