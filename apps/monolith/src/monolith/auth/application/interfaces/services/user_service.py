from abc import ABC, abstractmethod

from monolith.auth.domain.model.user import User
from monolith.auth.application.dtos.user import CreateUserCommand, CreateUserResponse


class IUserService(ABC):
    @abstractmethod
    async def create_user(self, data: CreateUserCommand) -> CreateUserResponse:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_login(self, login: str) -> User | None:
        raise NotImplementedError
