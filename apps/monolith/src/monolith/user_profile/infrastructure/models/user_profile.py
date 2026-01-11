from datetime import date

from sqlalchemy import String, Text, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column

from monolith.user_profile.infrastructure.models import Base
from monolith.user_profile.infrastructure.models.mixins import IdIntPkMixin, TimestampMixin


class UserProfile(IdIntPkMixin, TimestampMixin, Base):
    """ORM-модель профиля пользователя"""
    # Явное указание таблицы
    __tablename__ = "user_profiles"

    auth_user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True
    )
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        default=None,
        server_default=None,

    )
    middle_name: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        default=None,
        server_default=None,
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        default=None,
        server_default=None,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None,
        server_default=None,
    )
    birthdate: Mapped[date] = mapped_column(
        Date,
        nullable=True,
        default=None,
        server_default=None,
    )
    phone: Mapped[str]  = mapped_column(
        String(20),
        nullable=True,
        default=None,
        server_default=None,
    )
