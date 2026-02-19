from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Security
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials

from src.config import Settings
from src.domain.achievements.dto.schemas import (
    AchievementCategorySchema,
    AchievementProgressSchema,
    EarnedAchievementSchema,
    UserStreakSchema,
)
from src.domain.achievements.use_cases.get_user_earned import GetUserEarnedAchievements
from src.domain.achievements.use_cases.get_user_streak import GetUserStreak
from src.domain.achievements.use_cases.list import (
    ListAchievements,
)
from src.domain.achievements.use_cases.get_achievement_categories import GetAchievementCategories
from src.domain.achievements.use_cases.list_by_category import (
    ListAchievementsByCategory,
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


@achievement_router.get("/categories/", response_model=list[AchievementCategorySchema])
@inject
async def list_achievement_categories(
    get_categories: GetAchievementCategories = Depends(
        Provide["use_cases.get_achievement_categories"]
    ),
) -> list[AchievementCategorySchema]:
    """Получить список всех категорий достижений"""
    return await get_categories()


@achievement_router.get(
    "/category/{category}/", response_model=list[AchievementProgressSchema]
)
@inject
async def list_achievements_by_category(
    category: str,
    list_by_category: ListAchievementsByCategory = Depends(
        Provide["use_cases.list_achievements_by_category"]
    ),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> list[AchievementProgressSchema]:
    """Получить достижения по категории с прогрессом"""
    user_id = UUID(credentials["id"])
    return await list_by_category(user_id, category)


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
    get_streak: GetUserStreak = Depends(
        Provide["use_cases.get_user_streak"]
    ),
    credentials: JwtAuthorizationCredentials = Security(access_bearer),
) -> UserStreakSchema | None:
    """Получить текущую серию дней пользователя"""
    user_id = UUID(credentials["id"])
    return await get_streak(user_id)
