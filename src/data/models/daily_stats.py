from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

from src.common.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.data.models import User


class DailyStats(SQLModel, TimestampMixin, table=True):
    __tablename__ = "daily_stats"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    date: date
    total_count: float = Field(default=0)

    user: "User" = Relationship(back_populates="daily_stats")

    __table_args__ = (
        UniqueConstraint("user_id", "date", name="uq_daily_stats_user_date"),
    )


class DailyStatsPublic(SQLModel):
    id: UUID
    user_id: UUID
    date: date
    total_count: float
