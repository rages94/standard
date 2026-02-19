from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

from src.common.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from src.data.models import Achievement, User


class UserAchievement(SQLModel, TimestampMixin, table=True):
    """Полученные пользователем достижения"""

    __tablename__ = "user_achievement"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    achievement_id: UUID = Field(foreign_key="achievement.id", index=True)
    earned_at: datetime = Field(default_factory=datetime.utcnow)
    progress_at_earned: float = Field(
        default=0
    )  # Значение прогресса на момент получения

    # Отношения
    user: "User" = Relationship(back_populates="achievements")
    achievement: "Achievement" = Relationship(back_populates="user_achievements")


class UserAchievementProgress(SQLModel, table=True):
    """Текущий прогресс пользователя по достижениям"""

    __tablename__ = "user_achievement_progress"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    achievement_id: UUID = Field(foreign_key="achievement.id", index=True)
    current_value: float = Field(default=0)  # Текущее значение прогресса
    is_earned: bool = Field(default=False)  # Уже получено?
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Отношения
    user: "User" = Relationship(back_populates="achievement_progress")
    achievement: "Achievement" = Relationship(back_populates="progress_records")

    class Config:
        # Уникальная пара пользователь + достижение
        unique_together = [("user_id", "achievement_id")]


class UserAchievementPublic(SQLModel):
    """DTO для отображения полученного достижения"""

    id: UUID
    user_id: UUID
    achievement_id: UUID
    earned_at: datetime
    progress_at_earned: float


class UserAchievementProgressPublic(SQLModel):
    """DTO для отображения прогресса"""

    id: UUID
    user_id: UUID
    achievement_id: UUID
    current_value: float
    is_earned: bool
    updated_at: datetime


class AchievementWithProgress(SQLModel):
    """DTO для отображения достижения с прогрессом"""

    id: UUID
    name: str
    description: str
    icon: str | None
    category: str
    rarity: str
    condition_type: str
    target_value: float
    time_period: str | None
    current_value: float
    percentage: float
    is_earned: bool
    earned_at: datetime | None
