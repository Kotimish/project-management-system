from datetime import date

from pydantic import BaseModel


class SprintDTO(BaseModel):
    """DTO для модели спринт проекта"""
    id: int
    name: str
    start_date: date
    end_date: date


class CreateSprintCommand(BaseModel):
    """DTO для создания модели спринт проекта"""
    name: str
    start_date: date
    end_date: date


class UpdateSprintCommand(BaseModel):
    """DTO для обновления модели спринт проекта"""
    name: str
    start_date: date
    end_date: date
