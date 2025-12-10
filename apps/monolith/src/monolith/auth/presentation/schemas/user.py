from pydantic import BaseModel, SecretStr


class RegistrateUserRequest(BaseModel):
    login: str
    email: str
    password: SecretStr


class RegistrateUserResponse(BaseModel):
    id: int
