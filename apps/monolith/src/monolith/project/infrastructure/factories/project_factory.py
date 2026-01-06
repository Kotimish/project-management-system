from monolith.project.application.interfaces.factories.project_factory import IProjectFactory
from monolith.project.domain.model import Project


class ProjectFactory(IProjectFactory):
    """Фабрика проекта"""

    def create(self, name: str, owner_id: int, description: str = None) -> Project:
        if description is None:
            description = ""
        return Project(
            name=name,
            owner_id=owner_id,
            description=description,
        )
