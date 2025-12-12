from monolith.auth.application.dtos.user import CreateUserCommand, CreateUserResponse
from monolith.auth.application.interfaces.factories.user_factory import IUserFactory
from monolith.auth.domain.interfaces.repositories.user_repository import IUserRepository
from monolith.auth.application.interfaces.security.hash_service import IHashService
from monolith.auth.application.interfaces.services.role_service import IRoleService
from monolith.auth.application.interfaces.services.user_service import IUserService
from monolith.auth.domain.model.user import User


class UserService(IUserService):
    """Сервис пользователей"""

    def __init__(
            self,
            factory: IUserFactory,
            repository: IUserRepository,
            role_service: IRoleService,
            hash_service: IHashService
    ):
        self.factory = factory
        self.repository = repository
        self.role_service = role_service
        self.hash_service = hash_service

    async def create_user(self, data: CreateUserCommand) -> CreateUserResponse:
        hashed_password = self.hash_service.hash(data.password.get_secret_value())
        default_role = await self.role_service.get_default_role_id()
        user = self.factory.create(data, hashed_password, default_role)
        user = await self.repository.add(user)
        return CreateUserResponse(id=user.id)

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self.repository.get_by_id(user_id)

    async def get_user_by_login(self, login: str) -> User | None:
        return await self.repository.get_by_login(login)

    async def deactivate_user(self, user_id: str) -> bool:
        raise NotImplementedError
