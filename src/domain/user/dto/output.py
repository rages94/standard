from sqlmodel import SQLModel

from src.data.models.credit import CreditPublic
from src.data.models.completed_standard import CompletedStandardPublic
from src.data.models.user import UserPublic
from src.data.models.user_streak import UserStreakPublic


class DashboardResponse(SQLModel):
    user: UserPublic
    current_credit: CreditPublic | None
    recent_activity: list[CompletedStandardPublic]
    streak: UserStreakPublic
    today_norm: float
    month_norm: float
