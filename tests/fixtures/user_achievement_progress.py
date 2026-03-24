import pytest

from src.data.models import Achievement, UserAchievement, UserAchievementProgress
from tests.factories.achievements import AchievementFactory
from tests.factories.user_achievement import UserAchievementFactory
from tests.factories.user_achievement_progress import (
    UserAchievementProgressFactory,
)
from tests.factories.users import UserFactory


@pytest.fixture
async def achievement(_container) -> Achievement:
    return await AchievementFactory.create_async()


@pytest.fixture
async def achievement_with_progress(
    _container, default_user
) -> UserAchievementProgress:
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
        current_value=50,
        is_earned=False,
    )


@pytest.fixture
async def achievement_earned_not_viewed(_container, default_user) -> UserAchievement:
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=None,
        rarity="common",
        condition_type="count",
    )
    _progress = await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=100,
        is_earned=True,
    )
    return await UserAchievementFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        is_viewed=False,
        progress_at_earned=100,
    )


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
async def achievements_sorted_by_is_viewed(_container, default_user) -> dict:
    """Три ачивки: unviewed earned, viewed earned, не заработана"""
    a_unviewed = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=None,
        rarity="common",
        condition_type="count",
    )
    a_viewed = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=None,
        rarity="common",
        condition_type="count",
    )
    a_not_earned = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=None,
        rarity="common",
        condition_type="count",
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=a_unviewed.id,
        current_value=100,
        is_earned=True,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=a_viewed.id,
        current_value=100,
        is_earned=True,
    )
    await UserAchievementFactory.create_async(
        user_id=default_user.id,
        achievement_id=a_unviewed.id,
        is_viewed=False,
        progress_at_earned=100,
    )
    await UserAchievementFactory.create_async(
        user_id=default_user.id,
        achievement_id=a_viewed.id,
        is_viewed=True,
        progress_at_earned=100,
    )
    return {
        "unviewed_id": str(a_unviewed.id),
        "viewed_id": str(a_viewed.id),
        "not_earned_id": str(a_not_earned.id),
    }


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
