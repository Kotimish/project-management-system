from datetime import datetime

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    """Схема модели Проект слоя представления"""
    id: int
    name: str
    description: str
    owner_id: int
    created_at: datetime
    updated_at: datetime


class CreateProjectSchema(BaseModel):
    """Схема для создания модели Проект"""
    name: str
    owner_id: int
    description: str | None = None


class UpdateProjectSchema(BaseModel):
    """Схема для создания модели Проект"""
    name: str | None = None
    description: str | None = None
