from httpx import AsyncClient

from src.data.models import Standard


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
