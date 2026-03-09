import pytest

from src.data.models import Achievement, UserAchievementProgress
from tests.factories.achievements import AchievementFactory
from tests.factories.user_achievement_progress import (
    UserAchievementProgressFactory,
)
from tests.factories.users import UserFactory


@pytest.fixture
async def achievement(_container) -> Achievement:
    return await AchievementFactory.create_async()


@pytest.fixture
async def achievement_with_progress(_container, default_user) -> UserAchievementProgress:
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=False,
    )
    return await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=50,
        is_earned=False,
    )


@pytest.fixture
async def achievement_earned(_container, default_user) -> UserAchievementProgress:
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=False,
    )
    return await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=100,
        is_earned=True,
    )


@pytest.fixture
async def achievement_daily(_container, default_user) -> UserAchievementProgress:
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="daily",
        is_active=True,
        is_meta_group=False,
    )
    return await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=50,
        is_earned=False,
    )


@pytest.fixture
async def achievement_meta_group(_container, default_user) -> UserAchievementProgress:
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=True,
    )
    return await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=50,
        is_earned=False,
    )


@pytest.fixture
async def achievement_inactive(_container, default_user) -> UserAchievementProgress:
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=False,
        is_meta_group=False,
    )
    return await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=50,
        is_earned=False,
    )
