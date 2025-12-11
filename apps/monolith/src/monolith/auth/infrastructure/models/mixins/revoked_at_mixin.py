from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class RevokedAtMixin:
    revoked_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
