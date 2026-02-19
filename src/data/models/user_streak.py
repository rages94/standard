from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.data.models import User


class UserStreak(SQLModel, TimestampMixin, table=True):
    """Серии дней подряд с активностью"""

    __tablename__ = "user_streak"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", unique=True, index=True)
    current_streak: int = Field(default=0)  # Текущая серия
    longest_streak: int = Field(default=0)  # Максимальная серия
    last_activity_date: date | None = Field(
        default=None
    )  # Последний день с активностью

    # Отношения
    user: "User" = Relationship(back_populates="streak")


class UserStreakPublic(SQLModel):
    """DTO для отображения серии"""

    id: UUID
    user_id: UUID
    current_streak: int
    longest_streak: int
    last_activity_date: date | None
