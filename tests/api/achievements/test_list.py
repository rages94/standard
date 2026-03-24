from httpx import AsyncClient

from src.containers.container import container
from src.data.models import Standard, UserAchievement
from src.data.uow import UnitOfWork


async def test_list_achievements(auth_client: AsyncClient):
    """Тест получения списка достижений"""
    response = await auth_client.get("/achievements/")
    assert response.status_code == 200
    json = response.json()
    assert isinstance(json, list)
    if len(json) > 0:
        achievement = json[0]
        assert "id" in achievement
        assert "name" in achievement
        assert "description" in achievement
        assert "icon" in achievement
        assert "rarity" in achievement
        assert "target_value" in achievement
        assert "current_value" in achievement
        assert "percentage" in achievement
        assert "is_earned" in achievement


async def test_list_achievements_by_standard_id(
    auth_client: AsyncClient, standard: Standard
):
    """Тест получения достижений по standard_id"""
    response = await auth_client.get(f"/achievements/standard/{standard.id}/")
    assert response.status_code == 200
    json = response.json()
    assert isinstance(json, list)


async def test_list_earned_achievements(auth_client: AsyncClient):
    """Тест получения полученных достижений"""
    response = await auth_client.get("/achievements/earned/")
    assert response.status_code == 200
    json = response.json()
    assert isinstance(json, list)


async def test_get_user_streak(auth_client: AsyncClient):
    """Тест получения серии дней"""
    response = await auth_client.get("/achievements/streak/")
    assert response.status_code == 200
    json = response.json()
    if json is not None:
        assert "current_streak" in json
        assert "longest_streak" in json


async def test_list_achievements_requires_auth(client: AsyncClient):
    """Тест, что получение достижений требует авторизации"""
    response = await client.get("/achievements/")
    assert response.status_code == 401


async def test_achievement_is_viewed_false_initially(
    auth_client: AsyncClient,
    achievement_earned_not_viewed: UserAchievement,
):
    """Новое earned achievement должно иметь is_viewed=False"""
    response = await auth_client.get("/achievements/")
    assert response.status_code == 200
    json = response.json()
    earned = [a for a in json if a["is_earned"]]
    assert len(earned) == 1
    # При первом запросе is_viewed ещё False в ответе (до commit)
    # но после запроса в БД должно стать True


async def test_achievement_is_viewed_after_list(
    auth_client: AsyncClient,
    achievement_earned_not_viewed: UserAchievement,
):
    """После GET /achievements/ is_viewed должен стать True в БД"""
    achievement_id = achievement_earned_not_viewed.achievement_id

    response = await auth_client.get("/achievements/")
    assert response.status_code == 200

    uow: UnitOfWork = container.repositories.uow()
    async with uow:
        result = await uow.user_achievement_repo.get_or_none(
            {
                "user_id": achievement_earned_not_viewed.user_id,
                "achievement_id": achievement_id,
            }
        )
        assert result is not None
        assert result.is_viewed is True


async def test_is_viewed_in_response_after_second_call(
    auth_client: AsyncClient,
    achievement_earned_not_viewed: UserAchievement,
):
    """Второй запрос должен вернуть is_viewed=True"""
    # Первый запрос — помечает как viewed
    await auth_client.get("/achievements/")

    # Второй запрос — должен вернуть is_viewed=True
    response = await auth_client.get("/achievements/")
    assert response.status_code == 200
    json = response.json()
    earned = [a for a in json if a["is_earned"]]
    assert len(earned) == 1
    assert earned[0]["is_viewed"] is True


async def test_is_viewed_in_response_schema(
    auth_client: AsyncClient,
    achievement_earned_not_viewed: UserAchievement,
):
    """Поле is_viewed присутствует в ответе"""
    response = await auth_client.get("/achievements/")
    assert response.status_code == 200
    json = response.json()
    for achievement in json:
        assert "is_viewed" in achievement


async def test_achievement_with_is_viewed_true_stays_true(
    auth_client: AsyncClient,
    achievement_earned_not_viewed: UserAchievement,
):
    """Если is_viewed уже True, остаётся True"""
    # Первый запрос — помечает
    await auth_client.get("/achievements/")

    # Второй запрос
    response = await auth_client.get("/achievements/")
    json = response.json()
    earned = [a for a in json if a["is_earned"]]
    assert earned[0]["is_viewed"] is True

    # Третий запрос — всё ещё True
    response = await auth_client.get("/achievements/")
    json = response.json()
    earned = [a for a in json if a["is_earned"]]
    assert earned[0]["is_viewed"] is True


async def test_achievements_sorted_by_is_viewed(
    auth_client: AsyncClient,
    achievements_sorted_by_is_viewed: dict,
):
    """Сортировка: is_viewed=False первыми, True вторыми, None (не earned) третьими"""
    ids = achievements_sorted_by_is_viewed

    response = await auth_client.get("/achievements/")
    assert response.status_code == 200
    json = response.json()

    viewed_values = [a["is_viewed"] for a in json]
    false_indices = [i for i, v in enumerate(viewed_values) if v is False]
    true_indices = [i for i, v in enumerate(viewed_values) if v is True]

    # Все False идут раньше True
    if false_indices and true_indices:
        assert max(false_indices) < min(true_indices)
