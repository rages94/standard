from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials

from src.config import Settings
from src.domain.achievements.dto.schemas import (
    AchievementProgressSchema,
    EarnedAchievementSchema,
    UserStreakSchema,
)
from src.domain.achievements.use_cases.get_user_earned import GetUserEarnedAchievements
from src.domain.achievements.use_cases.get_user_streak import GetUserStreak
from src.domain.achievements.use_cases.list import (
    ListAchievements,
)
from src.domain.achievements.use_cases.list_by_category import (
    ListAchievementsByStandardId,
)

settings = Settings()
achievement_router = APIRouter()
access_bearer = JwtAccessBearer(secret_key=settings.jwt.secret_key)


@achievement_router.get("/", response_model=list[AchievementProgressSchema])
@inject
async def list_achievements(
    list_achievements_use_case: ListAchievements = Depends(
        Provide["use_cases.list_achievements"]
    ),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> list[AchievementProgressSchema]:
    """Получить все активные достижения с прогрессом текущего пользователя"""
    user_id = UUID(credentials["id"])
    return await list_achievements_use_case(user_id)


@achievement_router.get(
    "/standard/{standard_id}/", response_model=list[AchievementProgressSchema]
)
@inject
async def list_achievements_by_standard_id(
    standard_id: UUID,
    list_by_standard: ListAchievementsByStandardId = Depends(
        Provide["use_cases.list_achievements_by_standard_id"]
    ),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> list[AchievementProgressSchema]:
    """Получить достижения по standard_id с прогрессом"""
    user_id = UUID(credentials["id"])
    return await list_by_standard(user_id, standard_id)


@achievement_router.get("/earned/", response_model=list[EarnedAchievementSchema])
@inject
async def list_earned_achievements(
    get_earned: GetUserEarnedAchievements = Depends(
        Provide["use_cases.get_user_earned_achievements"]
    ),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> list[EarnedAchievementSchema]:
    """Получить полученные достижения текущего пользователя"""
    user_id = UUID(credentials["id"])
    return await get_earned(user_id)


@achievement_router.get("/streak/", response_model=UserStreakSchema | None)
@inject
async def get_user_streak(
    get_streak: GetUserStreak = Depends(Provide["use_cases.get_user_streak"]),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> UserStreakSchema | None:
    """Получить текущую серию дней пользователя"""
    user_id = UUID(credentials["id"])
    return await get_streak(user_id)
