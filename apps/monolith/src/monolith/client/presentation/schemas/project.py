from datetime import datetime

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    """Схема для модели Проект"""
    id: int
    name: str
    description: str
    owner_id: int
    created_at: datetime
    updated_at: datetime


class CreateProjectSchema(BaseModel):
    """Схема для создания модели Проект"""
    name: str
    description: str
    owner_id: int


class UpdateProjectSchema(BaseModel):
    """Схема для создания модели Проект"""
    name: str
    description: str
    owner_id: int
