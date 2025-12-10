from datetime import datetime, timezone


class TimestampMixin:
    def __init__(self, created_at: datetime | None = None, updated_at: datetime | None = None):
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or self.created_at

    def touch(self):
        self.updated_at = datetime.now(timezone.utc)