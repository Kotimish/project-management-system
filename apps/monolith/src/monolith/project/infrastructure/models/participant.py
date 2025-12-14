from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from monolith.project.infrastructure.models import Base
from monolith.project.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin

if TYPE_CHECKING:
    from monolith.project.infrastructure.models import Project


class Participant(IdIntPkMixin, TimestampMixin, Base):
    """ORM-модель участника проекта"""
    auth_user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey('projects.id'),
        nullable=False,
    )
    project: Mapped['Project'] = relationship(
        back_populates='participants'
    )

    def __str__(self):
        return f"{self.__class__.__name__}(auth_user_id={self.id}, project_id={self.project_id!r})"

    def __repr__(self):
        return str(self)
