from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.achievements.dto.enums import (
    AchievementCategory,
    ConditionType,
    RarityType,
    TimePeriod,
)

__all__ = [
    "AchievementCategorySchema",
    "AchievementProgressSchema",
    "UserStreakSchema",
    "AchievementWithProgressSchema",
    "EarnedAchievementSchema",
]


class AchievementCategorySchema(BaseModel):
    """Схема категории достижения"""

    value: str
    label: str


class AchievementProgressSchema(BaseModel):
    """Схема достижения с прогрессом пользователя"""

    id: UUID
    name: str
    description: str
    icon: str | None
    category: AchievementCategory
    rarity: RarityType
    condition_type: ConditionType
    target_value: float
    time_period: TimePeriod | None
    is_active: bool
    current_value: float = Field(default=0.0)
    percentage: float = Field(default=0.0)
    is_earned: bool = Field(default=False)
    earned_at: datetime | None = None


class EarnedAchievementSchema(BaseModel):
    """Схема полученного достижения"""

    id: UUID
    name: str
    description: str
    icon: str | None
    category: AchievementCategory
    rarity: RarityType
    earned_at: datetime
    progress_at_earned: float


class UserStreakSchema(BaseModel):
    """Схема серии дней пользователя"""

    current_streak: int
    longest_streak: int
    last_activity_date: datetime | None


class AchievementWithProgressSchema(BaseModel):
    """Схема достижения с прогрессом (для внутреннего использования)"""

    achievement: AchievementProgressSchema
    is_earned: bool
    earned_at: datetime | None
    current_value: float
