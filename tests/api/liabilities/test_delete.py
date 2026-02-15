from uuid import uuid4

from httpx import AsyncClient

from src.data.models import Liability


async def test_delete_liability_basic(
    auth_client: AsyncClient, liability: Liability
) -> None:
    response = await auth_client.delete(f"/liabilities/{liability.id}")
    assert response.status_code == 204
    assert response.content == b""


async def test_delete_liability_not_found(auth_client: AsyncClient) -> None:
    fake_id = uuid4()
    response = await auth_client.delete(f"/liabilities/{fake_id}")
    assert response.status_code == 404


async def test_delete_liability_other_user(
    auth_client: AsyncClient, liability_another_user: Liability
) -> None:
    response = await auth_client.delete(f"/liabilities/{liability_another_user.id}")
    assert response.status_code == 404


async def test_delete_liability_requires_auth(
    client: AsyncClient, liability: Liability
) -> None:
    response = await client.delete(f"/liabilities/{liability.id}")
    assert response.status_code == 401