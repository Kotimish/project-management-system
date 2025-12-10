from monolith.auth.application.exceptions import auth_exceptions as exceptions
from monolith.auth.application.interfaces.services.role_service import IRoleService
from monolith.auth.domain.interfaces.repositories.role_repository import IRoleRepository
from monolith.auth.domain.model.role import Role


class RoleService(IRoleService):
    def __init__(self, repository: IRoleRepository):
        self.repository = repository

    async def get_role_by_id(self, role_id) -> Role | None:
        return await self.repository.get_by_id(role_id)

    async def get_default_role_id(self) -> int:
        role = await self.repository.get_by_slug(slug='default')
        if not role:
            raise exceptions.InvalidRoleException("Default role not found")
        return role.id
