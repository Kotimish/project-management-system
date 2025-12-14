from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from monolith.project.domain.interfaces.repositories.task_status_repository import ITaskStatusRepository
from monolith.project.infrastructure.models import TaskStatus as ORMTaskStatus
from monolith.project.domain.model import TaskStatus


class TaskStatusRepository(ITaskStatusRepository):
    """Реализация репозитория для статусов задач."""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, task_status: TaskStatus) -> TaskStatus:
        orm_task_status = ORMTaskStatus(
            name = task_status.name,
            slug = task_status.slug,
            description = task_status.description,

        )
        self.session.add(orm_task_status)
        await self.session.commit()
        await self.session.refresh(orm_task_status)
        # Обновление полей доменной модели
        task_status.id = orm_task_status.id
        task_status.created_at = orm_task_status.created_at
        task_status.updated_at = orm_task_status.updated_at
        return task_status

    async def _get_by_id(self, task_status_id: int) -> ORMTaskStatus | None:
        return await self.session.get(ORMTaskStatus, task_status_id)

    async def get_by_id(self, task_status_id: int) -> TaskStatus | None:
        orm_task_status = await self._get_by_id(task_status_id)
        if not orm_task_status:
            return None
        return TaskStatus(
            name = orm_task_status.name,
            slug = orm_task_status.slug,
            description= orm_task_status.description,
            status_id=orm_task_status.id,
            created_at = orm_task_status.created_at,
            updated_at=orm_task_status.updated_at
        )

    async def get_by_slug(self, slug: str) -> TaskStatus | None:
        statement = select(ORMTaskStatus).where(ORMTaskStatus.slug == slug)
        result = await self.session.execute(statement)
        orm_task_status = result.scalar_one_or_none()
        if not orm_task_status:
            return None
        return TaskStatus(
            name = orm_task_status.name,
            slug = orm_task_status.slug,
            description= orm_task_status.description,
            status_id=orm_task_status.id,
            created_at = orm_task_status.created_at,
            updated_at=orm_task_status.updated_at
        )

    async def get_all(self) -> list[TaskStatus]:
        statement = select(ORMTaskStatus).order_by(ORMTaskStatus.id)
        result = await self.session.scalars(statement)
        all_orm_task_status = result.all()
        return [
            TaskStatus(
                name=orm_task_status.name,
                slug=orm_task_status.slug,
                description=orm_task_status.description,
                status_id=orm_task_status.id,
                created_at=orm_task_status.created_at,
                updated_at=orm_task_status.updated_at
            )
            for orm_task_status in all_orm_task_status
        ]

    async def update(self, task_status_id: int, task_status: TaskStatus) -> TaskStatus | None:
        orm_task_status = await self._get_by_id(task_status_id)
        if not orm_task_status:
            return None
        # Обновляем поля ORM-модели полями доменной модели
        orm_task_status.name = task_status.name
        orm_task_status.slug = task_status.slug
        orm_task_status.description = task_status.description
        orm_task_status.updated_at = task_status.updated_at

        await self.session.commit()
        await self.session.refresh(orm_task_status)
        return TaskStatus(
            name = orm_task_status.name,
            slug = orm_task_status.slug,
            description= orm_task_status.description,
            status_id=orm_task_status.id,
            created_at = orm_task_status.created_at,
            updated_at = orm_task_status.updated_at
        )

    async def remove(self, task_status_id: int) -> bool:
        orm_task_status = await self._get_by_id(task_status_id)
        if not orm_task_status:
            return False
        await self.session.delete(orm_task_status)
        await self.session.commit()
        return True
