from datetime import date, datetime

from pydantic import BaseModel

from src.data.models import Achievement
from src.data.models.completed_standard import CompletedStandardPublic
from src.domain.achievements.dto.schemas import AchievementProgressSchema


class Dataset(BaseModel):
    label: str
    data: list[float]


class GroupedCompletedStandard(BaseModel):
    labels: list[date]
    datasets: list[Dataset]


class UserCompletedStandard(BaseModel):
    username: str
    count: float
    standards: float


class RatingGroupedCompletedStandard(BaseModel):
    standard_name: str
    user_ratings: list[UserCompletedStandard]


class CompletedStandardListResponse(BaseModel):
    data: list[CompletedStandardPublic]
    count: int
    next_page: bool


class CompletedStandardWithAchievements(BaseModel):
    completed_standard: CompletedStandardPublic
    new_achievements: list[AchievementProgressSchema]


def achievements_to_progress_schemas(
    achievements: list[Achievement],
) -> list[AchievementProgressSchema]:
    return [
        AchievementProgressSchema(
            id=a.id,
            name=a.name,
            description=a.description,
            icon=a.icon,
            rarity=a.rarity,
            condition_type=a.condition_type,
            target_value=a.target_value,
            time_period=a.time_period,
            is_active=a.is_active,
            current_value=a.target_value,
            percentage=100.0,
            is_earned=True,
            earned_at=datetime.utcnow(),
            is_viewed=False,
        )
        for a in achievements
    ]
