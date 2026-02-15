from uuid import uuid4

from httpx import AsyncClient

from src.data.models import Liability


async def test_update_liability_basic(
    auth_client: AsyncClient, liability: Liability
) -> None:
    update_data = {"count": 15.5}
    response = await auth_client.patch(
        f"/liabilities/{liability.id}",
        json=update_data,
    )
    assert response.status_code == 200
    json = response.json()
    assert json["count"] == update_data["count"]
    assert json["id"] == str(liability.id)


async def test_update_liability_partial(
    auth_client: AsyncClient, liability: Liability
) -> None:
    update_data = {"count": 25.5}
    response = await auth_client.patch(
        f"/liabilities/{liability.id}",
        json=update_data,
    )
    assert response.status_code == 200
    json = response.json()
    assert json["count"] == update_data["count"]


async def test_update_liability_not_found(auth_client: AsyncClient) -> None:
    fake_id = uuid4()
    response = await auth_client.patch(
        f"/liabilities/{fake_id}",
        json={"count": 50.0},
    )
    assert response.status_code == 404


async def test_update_liability_other_user(
    auth_client: AsyncClient, liability_another_user: Liability
) -> None:
    response = await auth_client.patch(
        f"/liabilities/{liability_another_user.id}",
        json={"count": 50.0},
    )
    assert response.status_code == 404


async def test_update_liability_requires_auth(
    client: AsyncClient, liability: Liability
) -> None:
    response = await client.patch(
        f"/liabilities/{liability.id}",
        json={"count": 50.0},
    )
    assert response.status_code == 401