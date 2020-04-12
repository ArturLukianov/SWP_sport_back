from datetime import datetime, timezone

from .base import Base


class Semester(Base):
    id: int
    name: str
    start: datetime
    end: datetime
    choice_deadline: datetime

    @property
    def is_enroll_open(self):
        # db stores timestamps in the UTC format, so we need to use UTC timezone here
        return datetime.now(timezone.utc) < self.choice_deadline
