from datetime import date, datetime

from pydantic import BaseModel, Field


class CreateUserProfileRequest(BaseModel):
    """Данные для запроса создания профиля пользователя"""
    auth_user_id: int
    display_name: str


class CreateUserProfileResponse(BaseModel):
    """Данные для ответа на запрос создания профиля пользователя"""
    id: int


class GetUserProfileResponse(BaseModel):
    """Данные для ответа на запрос получения профиля пользователя"""
    id: int
    auth_user_id: int
    display_name: str
    created_at: datetime
    updated_at: datetime
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    description: str | None
    birthdate: date | None
    phone: str | None


class UpdateUserProfileRequest(BaseModel):
    """Данные для запроса обновления профиля пользователя"""
    display_name: str | None
    first_name: str | None
    middle_name: str | None
    last_name: str | None
    description: str | None
    birthdate: date | None
    phone: str | None


class UpdateUserProfileResponse(BaseModel):
    """Данные для ответа на запрос обновления профиля пользователя"""
    id: int


class UserProfilesRequest(BaseModel):
    """Данные для запроса множества профилей пользователей"""
    ids: list[int] = Field(
        min_length=1,
        max_length=100,
    )
