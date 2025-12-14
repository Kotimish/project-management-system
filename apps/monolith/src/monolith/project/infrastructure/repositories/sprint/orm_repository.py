from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from monolith.project.domain.interfaces.repositories.sprint_repository import ISprintRepository
from monolith.project.domain.model import Sprint
from monolith.project.infrastructure.models import Sprint as ORMSprint


class SprintRepository(ISprintRepository):
    """Реализация репозитория для Спринта."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, sprint: Sprint) -> Sprint:
        orm_sprint = ORMSprint(
            name=sprint.name,
            project_id=sprint.project_id,
            start_date=sprint.start_date,
            end_date=sprint.end_date,

        )
        self.session.add(orm_sprint)
        await self.session.commit()
        await self.session.refresh(orm_sprint)
        # Обновление полей доменной модели
        sprint.id = orm_sprint.id
        sprint.created_at = orm_sprint.created_at
        sprint.updated_at = orm_sprint.updated_at
        return sprint

    async def _get_by_id(self, sprint_id: int) -> ORMSprint | None:
        return await self.session.get(ORMSprint, sprint_id)

    async def get_by_id(self, sprint_id: int) -> Sprint | None:
        orm_sprint = await self._get_by_id(sprint_id)
        if not orm_sprint:
            return None
        return Sprint(
            name=orm_sprint.name,
            project_id=orm_sprint.project_id,
            start_date=orm_sprint.start_date,
            end_date=orm_sprint.end_date,
            sprint_id=orm_sprint.id,
            created_at=orm_sprint.created_at,
            updated_at=orm_sprint.updated_at
        )

    async def get_all(self) -> list[Sprint]:
        statement = select(ORMSprint).order_by(ORMSprint.id)
        result = await self.session.scalars(statement)
        orm_sprints = result.all()
        return [
            Sprint(
                name=orm_sprint.name,
                project_id=orm_sprint.project_id,
                start_date=orm_sprint.start_date,
                end_date=orm_sprint.end_date,
                sprint_id=orm_sprint.id,
                created_at=orm_sprint.created_at,
                updated_at=orm_sprint.updated_at
            )
            for orm_sprint in orm_sprints
        ]

    async def get_all_by_project_id(self, project_id: int) -> list[Sprint]:
        statement = (
            select(ORMSprint)
            .where(ORMSprint.project_id == project_id)
            .order_by(ORMSprint.id)
        )
        result = await self.session.scalars(statement)
        orm_sprints = result.all()
        return [
            Sprint(
                name=orm_sprint.name,
                project_id=orm_sprint.project_id,
                start_date=orm_sprint.start_date,
                end_date=orm_sprint.end_date,
                sprint_id=orm_sprint.id,
                created_at=orm_sprint.created_at,
                updated_at=orm_sprint.updated_at
            )
            for orm_sprint in orm_sprints
        ]

    async def update(self, sprint_id: int, sprint: Sprint) -> Sprint | None:
        orm_sprint = await self._get_by_id(sprint_id)
        if not orm_sprint:
            return None
        # Обновляем поля ORM-модели полями доменной модели
        orm_sprint.name = sprint.name
        orm_sprint.project_id = sprint.project_id
        orm_sprint.start_date = sprint.start_date
        orm_sprint.end_date = sprint.end_date

        await self.session.commit()
        await self.session.refresh(orm_sprint)
        return Sprint(
            name=orm_sprint.name,
            project_id=orm_sprint.project_id,
            start_date=orm_sprint.start_date,
            end_date=orm_sprint.end_date,
            sprint_id=orm_sprint.id,
            created_at=orm_sprint.created_at,
            updated_at=orm_sprint.updated_at
        )

    async def remove(self, sprint_id: int) -> bool:
        orm_sprint = await self._get_by_id(sprint_id)
        if not orm_sprint:
            return False
        await self.session.delete(orm_sprint)
        await self.session.commit()
        return True
