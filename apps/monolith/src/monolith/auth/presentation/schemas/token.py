from pydantic import BaseModel


class TokenResponse(BaseModel):
    token: str


class DecodeTokenResponse(BaseModel):
    sub: int
    role_slug: str
    exp: int
