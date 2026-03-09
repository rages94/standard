from httpx import AsyncClient

from src.domain.achievements.dto.enums import MetaTier, RarityType
from tests.factories.achievements import AchievementFactory
from tests.factories.user_achievement_progress import (
    UserAchievementProgressFactory,
)


async def test_get_dashboard_with_nearest_achievement(
    auth_client: AsyncClient,
    standard,
    default_user,
) -> None:
    """Тест: получение dashboard с nearest_achievement"""
    achievement = await AchievementFactory.create_async(
        name="Тестовое достижение",
        target_value=100,
        rarity=RarityType.COMMON,
        condition_type="count",
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

    response = await auth_client.get("/users/dashboard/")
    assert response.status_code == 200

    json = response.json()
    assert "nearest_achievement" in json
    assert json["nearest_achievement"] is not None
    assert json["nearest_achievement"]["current_value"] == 50
    assert json["nearest_achievement"]["achievement"]["name"] == "Тестовое достижение"
    assert json["nearest_achievement"]["achievement"]["target_value"] == 100


async def test_get_dashboard_nearest_achievement_none(
    auth_client: AsyncClient,
    default_user,
) -> None:
    """Тест: nearest_achievement = None когда нет прогресса"""
    response = await auth_client.get("/users/dashboard/")
    assert response.status_code == 200

    json = response.json()
    assert "nearest_achievement" in json
    assert json["nearest_achievement"] is None


async def test_get_dashboard_nearest_achievement_structure(
    auth_client: AsyncClient,
    standard,
    default_user,
) -> None:
    """Тест: проверка структуры nearest_achievement с вложенным achievement"""
    achievement = await AchievementFactory.create_async(
        target_value=100,
        rarity=RarityType.RARE,
        condition_type="count",
        time_period="total",
        is_active=True,
        is_meta_group=False,
        standard_id=standard.id,
    )
    await UserAchievementProgressFactory.create_async(
        user_id=default_user.id,
        achievement_id=achievement.id,
        current_value=30,
        is_earned=False,
    )

    response = await auth_client.get("/users/dashboard/")
    assert response.status_code == 200

    json = response.json()
    nearest = json["nearest_achievement"]

    assert "id" in nearest
    assert "user_id" in nearest
    assert "achievement_id" in nearest
    assert "current_value" in nearest
    assert "is_earned" in nearest
    assert "updated_at" in nearest
    assert "achievement" in nearest

    achievement_data = nearest["achievement"]
    assert "id" in achievement_data
    assert "name" in achievement_data
    assert "rarity" in achievement_data
    assert "condition_type" in achievement_data
    assert "target_value" in achievement_data
    assert "time_period" in achievement_data


async def test_get_dashboard_requires_auth(client: AsyncClient) -> None:
    """Тест: получение dashboard требует авторизации"""
    response = await client.get("/users/dashboard/")
    assert response.status_code == 401
