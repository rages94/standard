from httpx import AsyncClient

from src.data.models import CompletedStandard, User


async def test_list_completed_standards_empty(auth_client: AsyncClient):
    response = await auth_client.get("/completed_standards/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["data"] == []
    assert data["next_page"] is False


async def test_list_completed_standards_returns_authored_only(
    auth_client: AsyncClient,
    default_user: User,
    completed_standard: CompletedStandard,
    completed_standard_weight: CompletedStandard,
    completed_standard_another_user: CompletedStandard,
):
    response = await auth_client.get("/completed_standards/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["data"]) == 2
    assert all(cs["user_id"] == str(default_user.id) for cs in data["data"])


async def test_list_completed_standard_requires_auth(client: AsyncClient):
    response = await client.get("/completed_standards/")
    assert response.status_code == 401
