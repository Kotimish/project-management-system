from monolith.project.application.interfaces.factories.task_factory import ITaskFactory
from monolith.project.domain.model import Task


class TaskFactory(ITaskFactory):
    """Интерфейс фабрики задач проекта"""

    def create(
            self,
            title: str,
            project_id: int,
            status_id: int,
            assignee_id: int | None = None,
            sprint_id: int | None = None,
            description: str | None = None,
    ) -> Task:
        return Task(
            title=title,
            description=description,
            project_id=project_id,
            status_id=status_id,
            assignee_id=assignee_id,
            sprint_id=sprint_id,
        )
