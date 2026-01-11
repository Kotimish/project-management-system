from datetime import date

from pydantic import BaseModel


class CreateSprintRequest(BaseModel):
    name: str
    project_id: int
    start_date: date
    end_date: date


class SprintResponse(BaseModel):
    id: int
    name: str
    project_id: int
    start_date: date
    end_date: date


class UpdateSprintRequest(BaseModel):
    name: str
    start_date: date
    end_date: date
