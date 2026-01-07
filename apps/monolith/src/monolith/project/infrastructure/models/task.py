from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from monolith.project.infrastructure.models import Base
from monolith.project.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin

if TYPE_CHECKING:
    from monolith.project.infrastructure.models import Project, TaskStatus, Sprint, Participant


class Task(IdIntPkMixin, TimestampMixin, Base):
    """ORM-модель Задачи"""
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        default='',
        server_default='',
    )
    # Задача может быть без ответственного
    assignee_id: Mapped[int] = mapped_column(
        ForeignKey('participants.id'),
        nullable=True,
    )
    assignee: Mapped['Participant'] = relationship(
        back_populates='tasks'
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey('projects.id'),
        nullable=False,
    )
    project: Mapped['Project'] = relationship(
        back_populates='tasks'
    )
    status_id: Mapped[int] = mapped_column(
        ForeignKey('task_status.id'),
        nullable=False,
    )
    status: Mapped['TaskStatus'] = relationship(
        back_populates='tasks'
    )
    # Задача может быть без спринта
    sprint_id: Mapped[int] = mapped_column(
        ForeignKey('sprints.id'),
        nullable=True,
    )
    sprint: Mapped['Sprint'] = relationship(
        back_populates='tasks'
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.title!r}, description={self.description!r})"

    def __repr__(self):
        return str(self)
