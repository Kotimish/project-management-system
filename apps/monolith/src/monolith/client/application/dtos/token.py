from pydantic import BaseModel


class AccessTokenDTO(BaseModel):
    sub: int
    role_slug: str
    exp: int


class RefreshTokenDTO(BaseModel):
    sub: int
    role_slug: str
    session_id: int
    exp: int
