from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from monolith.project.domain.interfaces.repositories.project_repository import IProjectRepository
from monolith.project.infrastructure.models import Project as ORMProject
from monolith.project.domain.model import Project


class ProjectRepository(IProjectRepository):
    """Реализация репозитория для модели Проект."""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, project: Project) -> Project:
        orm_project = ORMProject(
            name = project.name,
            description = project.description,
            owner_id = project.owner_id,

        )
        self.session.add(orm_project)
        await self.session.commit()
        await self.session.refresh(orm_project)
        # Обновление полей доменной модели
        project.id = orm_project.id
        project.created_at = orm_project.created_at
        project.updated_at = orm_project.updated_at
        return project

    async def _get_by_id(self, project_id: int) -> ORMProject | None:
        return await self.session.get(ORMProject, project_id)

    async def get_by_id(self, project_id: int) -> Project | None:
        orm_project = await self._get_by_id(project_id)
        if not orm_project:
            return None
        return Project(
            name = orm_project.name,
            description= orm_project.description,
            owner_id=orm_project.owner_id,
            project_id=orm_project.id,
            created_at = orm_project.created_at,
            updated_at=orm_project.updated_at
        )

    async def get_by_owner_id(self, owner_id: int) -> list[Project]:
        statement = (
            select(ORMProject)
            .where(ORMProject.owner_id==owner_id)
            .order_by(ORMProject.id)
        )
        result = await self.session.scalars(statement)
        orm_projects = result.all()
        return [
            Project(
                name=orm_project.name,
                description=orm_project.description,
                owner_id=orm_project.owner_id,
                project_id=orm_project.id,
                created_at=orm_project.created_at,
                updated_at=orm_project.updated_at
            )
            for orm_project in orm_projects
        ]

    async def get_all(self) -> list[Project]:
        statement = select(ORMProject).order_by(ORMProject.id)
        result = await self.session.scalars(statement)
        orm_projects = result.all()
        return [
            Project(
                name=orm_project.name,
                description=orm_project.description,
                owner_id=orm_project.owner_id,
                project_id=orm_project.id,
                created_at=orm_project.created_at,
                updated_at=orm_project.updated_at
            )
            for orm_project in orm_projects
        ]

    async def update(self, project_id: int, project: Project) -> Project | None:
        orm_project = await self._get_by_id(project_id)
        if not orm_project:
            return None
        # Обновляем поля ORM-модели полями доменной модели
        orm_project.name = project.name
        orm_project.description = project.description

        await self.session.commit()
        await self.session.refresh(orm_project)
        return Project(
            name = orm_project.name,
            description= orm_project.description,
            owner_id=orm_project.owner_id,
            project_id=orm_project.id,
            created_at = orm_project.created_at,
            updated_at=orm_project.updated_at
        )


    async def remove(self, project_id: int) -> bool:
        orm_project = await self._get_by_id(project_id)
        if not orm_project:
            return False
        await self.session.delete(orm_project)
        await self.session.commit()
        return True
