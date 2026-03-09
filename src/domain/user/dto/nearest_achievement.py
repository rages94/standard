from sqlmodel import SQLModel

from src.data.models.achievement import AchievementPublic
from src.data.models.user_achievement import UserAchievementProgressPublic


class UserAchievementProgressWithAchievement(UserAchievementProgressPublic):
    """DTO для прогресса достижения с вложенным achievement"""
    achievement: AchievementPublic
