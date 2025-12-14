from pydantic import BaseModel


class TokenDTO(BaseModel):
    sub: int
    role_slug: str
    exp: int
