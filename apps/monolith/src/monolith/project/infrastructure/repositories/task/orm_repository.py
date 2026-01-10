from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from monolith.project.domain.interfaces.repositories.task_repository import ITaskRepository
from monolith.project.domain.model import Task, TaskView, TaskStatus
from monolith.project.infrastructure.models import Participant as ORMParticipant
from monolith.project.infrastructure.models import Task as ORMTask


class TaskRepository(ITaskRepository):
    """Реализация репозитория для задач."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, task: Task) -> Task:
        orm_task = ORMTask(
            title=task.title,
            description=task.description,
            project_id=task.project_id,
            status_id=task.status_id,
            assignee_id=task.assignee_id,
            sprint_id=task.sprint_id,

        )
        self.session.add(orm_task)
        await self.session.commit()
        await self.session.refresh(orm_task)
        # Обновление полей доменной модели
        task.id = orm_task.id
        task.created_at = orm_task.created_at
        task.updated_at = orm_task.updated_at
        return task

    async def _get_by_id(self, task_id: int) -> ORMTask | None:
        return await self.session.get(ORMTask, task_id)

    async def get_by_id(self, task_id: int) -> Task | None:
        orm_task = await self._get_by_id(task_id)
        if not orm_task:
            return None
        return Task(
            task_id=orm_task.id,
            title=orm_task.title,
            description=orm_task.description,
            project_id=orm_task.project_id,
            status_id=orm_task.status_id,
            assignee_id=orm_task.assignee_id,
            sprint_id=orm_task.sprint_id,
            created_at=orm_task.created_at,
            updated_at=orm_task.updated_at,
        )

    async def get_all(self) -> list[Task]:
        statement = select(ORMTask).order_by(ORMTask.id)
        result = await self.session.scalars(statement)
        orm_tasks = result.all()
        return [
            Task(
                task_id=orm_task.id,
                title=orm_task.title,
                description=orm_task.description,
                project_id=orm_task.project_id,
                status_id=orm_task.status_id,
                assignee_id=orm_task.assignee_id,
                sprint_id=orm_task.sprint_id,
                created_at=orm_task.created_at,
                updated_at=orm_task.updated_at,
            )
            for orm_task in orm_tasks
        ]

    async def get_list_tasks_by_auth_user_id(self, auth_user_id: int) -> list[TaskView]:
        statement = (
            select(ORMTask)
            .join(ORMTask.assignee)
            .where(ORMParticipant.auth_user_id == auth_user_id)
            .options(
                # Добавление связанной модели статуса задачи
                selectinload(ORMTask.status),
                # Добавление связанного участника проекта
                selectinload(ORMTask.assignee),
            )
            .order_by(ORMTask.id)
        )
        result = await self.session.scalars(statement)
        orm_tasks = result.all()

        tasks = []
        for orm_task in orm_tasks:
            status = TaskStatus(
                status_id=orm_task.status.id,
                name=orm_task.status.name,
                slug=orm_task.status.slug,
                description=orm_task.status.description,
                created_at=orm_task.status.created_at,
                updated_at=orm_task.status.updated_at
            )
            task = TaskView(
                task_id=orm_task.id,
                title=orm_task.title,
                description=orm_task.description,
                project_id=orm_task.project_id,
                status_id=orm_task.status_id,
                status=status,
                assignee_id=orm_task.assignee_id,
                sprint_id=orm_task.sprint_id,
                created_at=orm_task.created_at,
                updated_at=orm_task.updated_at,
            )
            tasks.append(task)

        return tasks

    async def get_list_tasks_by_project(self, project_id: int) -> list[Task]:
        statement = (
            select(ORMTask)
            .where(ORMTask.project_id == project_id)
            .order_by(ORMTask.id)
        )
        result = await self.session.scalars(statement)
        orm_tasks = result.all()
        return [
            Task(
                task_id=orm_task.id,
                title=orm_task.title,
                description=orm_task.description,
                project_id=orm_task.project_id,
                status_id=orm_task.status_id,
                assignee_id=orm_task.assignee_id,
                sprint_id=orm_task.sprint_id,
                created_at=orm_task.created_at,
                updated_at=orm_task.updated_at,
            )
            for orm_task in orm_tasks
        ]

    async def get_list_tasks_by_auth_user_id_in_project(self, project_id: int, auth_user_id: int) -> list[Task]:
        statement = (
            select(ORMTask)
            .join(ORMTask.assignee)
            .where(
                ORMTask.project_id == project_id,
                ORMParticipant.auth_user_id == auth_user_id
            )
            .order_by(ORMTask.id)
        )
        result = await self.session.scalars(statement)
        orm_tasks = result.all()
        return [
            Task(
                task_id=orm_task.id,
                title=orm_task.title,
                description=orm_task.description,
                project_id=orm_task.project_id,
                status_id=orm_task.status_id,
                assignee_id=orm_task.assignee_id,
                sprint_id=orm_task.sprint_id,
                created_at=orm_task.created_at,
                updated_at=orm_task.updated_at,
            )
            for orm_task in orm_tasks
        ]

    async def get_list_tasks_by_sprint(self, sprint_id: int) -> list[TaskView]:
        statement = (
            select(ORMTask)
            # Добавление связанной модели статуса задачи
            .options(selectinload(ORMTask.status))
            .where(ORMTask.sprint_id == sprint_id)
        )
        result = await self.session.scalars(statement)
        orm_tasks = result.all()

        tasks = []
        for orm_task in orm_tasks:
            status = TaskStatus(
                status_id=orm_task.status.id,
                name=orm_task.status.name,
                slug=orm_task.status.slug,
                description=orm_task.status.description,
                created_at=orm_task.status.created_at,
                updated_at=orm_task.status.updated_at
            )
            task = TaskView(
                task_id=orm_task.id,
                title=orm_task.title,
                description=orm_task.description,
                project_id=orm_task.project_id,
                status_id=orm_task.status_id,
                status=status,
                assignee_id=orm_task.assignee_id,
                sprint_id=orm_task.sprint_id,
                created_at=orm_task.created_at,
                updated_at=orm_task.updated_at,
            )
            tasks.append(task)

        return tasks

    async def update(self, task_id: int, task: Task) -> Task | None:
        orm_task = await self._get_by_id(task_id)
        if not orm_task:
            return None
        # Обновляем поля ORM-модели полями доменной модели
        orm_task.title = task.title
        orm_task.description = task.description
        orm_task.status_id = task.status_id
        orm_task.assignee_id = task.assignee_id
        orm_task.sprint_id = task.sprint_id

        await self.session.commit()
        await self.session.refresh(orm_task)
        return Task(
            task_id=orm_task.id,
            title=orm_task.title,
            description=orm_task.description,
            project_id=orm_task.project_id,
            status_id=orm_task.status_id,
            assignee_id=orm_task.assignee_id,
            sprint_id=orm_task.sprint_id,
            created_at=orm_task.created_at,
            updated_at=orm_task.updated_at,
        )

    async def remove(self, task_id: int) -> bool:
        orm_task = await self._get_by_id(task_id)
        if not orm_task:
            return False
        await self.session.delete(orm_task)
        await self.session.commit()
        return True
