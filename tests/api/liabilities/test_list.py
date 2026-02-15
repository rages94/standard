from httpx import AsyncClient

from src.data.models import Liability


async def test_list_liabilities_empty(auth_client: AsyncClient) -> None:
    response = await auth_client.get("/liabilities/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["data"] == []
    assert data["next_page"] is False


async def test_list_liabilities_returns_authored_only(
    auth_client: AsyncClient,
    liability: Liability,
    liability_another_user: Liability,
) -> None:
    response = await auth_client.get("/liabilities/")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["data"]) == 1
    assert data["data"][0]["id"] == str(liability.id)
    assert data["data"][0]["count"] == liability.count


async def test_list_liabilities_pagination(
    auth_client: AsyncClient, liability: Liability
) -> None:
    response = await auth_client.get("/liabilities/?limit=1&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert len(data["data"]) == 1
    assert data["next_page"] is False


async def test_list_liabilities_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/liabilities/")
    assert response.status_code == 401