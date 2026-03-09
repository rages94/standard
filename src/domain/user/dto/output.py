from sqlmodel import SQLModel

from src.data.models.completed_standard import CompletedStandardPublic
from src.data.models.credit import CreditPublic
from src.data.models.user import UserPublic
from src.data.models.user_streak import UserStreakPublic
from src.domain.user.dto.nearest_achievement import (
    UserAchievementProgressWithAchievement,
)


class DashboardResponse(SQLModel):
    user: UserPublic
    current_credit: CreditPublic | None
    streak: UserStreakPublic | None
    today_norm: float
    month_norm: float
    nearest_achievement: UserAchievementProgressWithAchievement | None = None
