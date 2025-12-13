from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from monolith.auth.domain.interfaces.repositories.role_repository import IRoleRepository
from monolith.auth.infrastructure.models import Role as ORMRole
from monolith.auth.domain.model import Role


class ORMRoleRepository(IRoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, role: Role) -> Role:
        orm_role = ORMRole(
            name = role.name,
            slug = role.slug,
            description = role.description,

        )
        self.session.add(orm_role)
        await self.session.commit()
        await self.session.refresh(orm_role)
        # Обновление полей доменной модели
        role.id = orm_role.id
        role.created_at = orm_role.created_at
        role.updated_at = orm_role.updated_at
        return role

    async def _get_by_id(self, role_id: int) -> ORMRole | None:
        return await self.session.get(ORMRole, role_id)

    async def get_by_id(self, role_id: int) -> Role | None:
        orm_role = await self._get_by_id(role_id)
        if not orm_role:
            return None
        return Role(
            name = orm_role.name,
            slug = orm_role.slug,
            description= orm_role.description,
            role_id=orm_role.id,
            created_at = orm_role.created_at,
            updated_at=orm_role.updated_at
        )

    async def get_by_slug(self, slug: str) -> Role | None:
        statement = select(ORMRole).where(ORMRole.slug == slug)
        result = await self.session.execute(statement)
        orm_role = result.scalar_one_or_none()
        if not orm_role:
            return None
        return Role(
            name = orm_role.name,
            slug = orm_role.slug,
            description= orm_role.description,
            role_id=orm_role.id,
            created_at = orm_role.created_at,
            updated_at=orm_role.updated_at
        )


    async def get_all(self) -> list[Role]:
        statement = select(ORMRole).order_by(ORMRole.id)
        result = await self.session.scalars(statement)
        orm_roles = result.all()
        return [
            Role(
                name=orm_role.name,
                slug=orm_role.slug,
                description=orm_role.description,
                role_id=orm_role.id,
                created_at=orm_role.created_at,
                updated_at=orm_role.updated_at
            )
            for orm_role in orm_roles
        ]

    async def update(self, role_id: int, role: Role) -> Role | None:
        orm_role = await self._get_by_id(role_id)
        if not orm_role:
            return None
        # Обновляем поля ORM-модели полями доменной модели
        orm_role.name = role.name
        orm_role.slug = role.slug
        orm_role.description = role.description
        orm_role.updated_at = role.updated_at

        await self.session.commit()
        await self.session.refresh(orm_role)
        return Role(
            name = orm_role.name,
            slug = orm_role.slug,
            description= orm_role.description,
            role_id=orm_role.id,
            created_at = orm_role.created_at,
            updated_at = orm_role.updated_at
        )

    async def remove(self, role_id: int) -> bool:
        orm_role = await self._get_by_id(role_id)
        if not orm_role:
            return False
        await self.session.delete(orm_role)
        await self.session.commit()
        return True