from datetime import datetime

from pydantic import BaseModel


class UpdateProjectCommand(BaseModel):
    """Данные для запроса обновления проекта"""
    name: str | None
    description: str | None


class ProjectDTO(BaseModel):
    """Данные для ответа на запрос о получение проекта"""
    id: int
    name: str | None
    description: str | None
    owner_id: int
    created_at: datetime
    updated_at: datetime