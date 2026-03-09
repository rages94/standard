import pytest

from src.data.models import Achievement, UserAchievementProgress
from src.domain.achievements.dto.enums import RarityType
from tests.factories.achievements import AchievementFactory
from tests.factories.user_achievement_progress import (
    UserAchievementProgressFactory,
)


async def test_get_nearest_achievement_common(
    default_user, standard, _container
) -> None:
    achievement = await AchievementFactory.create_async(
        target_value=100,
        current_value=50,
        rarity=RarityType.COMMON,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=50,
        is_earned=False,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is not None
    assert result.achievement_id == achievement.id
    assert result.achievement.rarity == RarityType.COMMON


async def test_get_nearest_achievement_rare(default_user, standard, _container) -> None:
    """Тест: ближайшая награда - rare rarity (COEF=1000)"""
    achievement = await AchievementFactory.create_async(
        target_value=1000,
        rarity=RarityType.RARE,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=500,
        is_earned=False,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is not None
    assert result.achievement.rarity == RarityType.RARE


async def test_get_nearest_achievement_epic(default_user, standard, _container) -> None:
    """Тест: ближайшая награда - epic rarity (COEF=10000)"""
    achievement = await AchievementFactory.create_async(
        target_value=10000,
        rarity=RarityType.EPIC,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=5000,
        is_earned=False,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is not None
    assert result.achievement.rarity == RarityType.EPIC


async def test_get_nearest_achievement_no_progress(default_user, _container) -> None:
    """Тест: нет прогресса - возвращает None"""
    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is None


async def test_get_nearest_achievement_all_earned(
    default_user, standard, _container
) -> None:
    """Тест: все достижения получены - возвращает None"""
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=100,
        is_earned=True,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is None


async def test_get_nearest_achievement_filters_daily(
    default_user, standard, _container
) -> None:
    """Тест: исключает daily time_period"""
    achievement_daily = await AchievementFactory.create_async(
        target_value=100,
        time_period="daily",
        is_active=True,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement_daily.id,
        current_value=50,
        is_earned=False,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is None


async def test_get_nearest_achievement_filters_meta_group(
    default_user, standard, _container
) -> None:
    """Тест: исключает meta_group достижения"""
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=True,
        is_meta_group=True,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=50,
        is_earned=False,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is None


async def test_get_nearest_achievement_filters_inactive(
    default_user, standard, _container
) -> None:
    """Тест: исключает неактивные достижения"""
    achievement = await AchievementFactory.create_async(
        target_value=100,
        time_period="total",
        is_active=False,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=50,
        is_earned=False,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is None


async def test_get_nearest_achievement_sorts_by_amount(
    default_user, standard, _container
) -> None:
    """Тест: выбирает достижение с минимальным amount"""
    achievement_common = await AchievementFactory.create_async(
        target_value=1000,
        rarity=RarityType.COMMON,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement_common.id,
        current_value=900,
        is_earned=False,
    )

    achievement_rare = await AchievementFactory.create_async(
        target_value=10000,
        rarity=RarityType.RARE,
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement_rare.id,
        current_value=1000,
        is_earned=False,
    )

    uow = _container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_progress_repo.get_nearest_achievement(
            default_user.id
        )

    assert result is not None
    assert result.achievement_id == achievement_common.id
