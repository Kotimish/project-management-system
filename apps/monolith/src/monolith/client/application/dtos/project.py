from datetime import datetime

from pydantic import BaseModel


class ProjectDTO(BaseModel):
    """DTO для модели Проект"""
    id: int
    name: str
    description: str
    owner_id: int
    created_at: datetime
    updated_at: datetime


class CreateProjectDTO(BaseModel):
    """DTO для создания модели Проект"""
    name: str
    owner_id: int
    description: str | None = None


class UpdateProjectDTO(BaseModel):
    """DTO для обновления модели Проект"""
    name: str | None
    description: str | None
