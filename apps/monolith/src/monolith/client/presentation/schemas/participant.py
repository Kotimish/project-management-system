from pydantic import BaseModel


class ParticipantSchema(BaseModel):
    """Схема модели Участник слоя представления"""
    id: int
    auth_user_id: int
    project_id: int
