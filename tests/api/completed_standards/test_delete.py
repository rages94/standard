from uuid import uuid4

from httpx import AsyncClient

from src.data.models import CompletedStandard


async def test_delete_completed_standard(
    auth_client: AsyncClient,
    completed_standard: CompletedStandard,
):
    response = await auth_client.delete(f"/completed_standards/{completed_standard.id}")
    assert response.status_code == 204

    response = await auth_client.get("/completed_standards/")
    assert response.status_code == 200
    assert response.json()["count"] == 0


async def test_delete_nonexistent_standard(auth_client: AsyncClient):
    fake_id = uuid4()
    response = await auth_client.delete(f"/completed_standards/{fake_id}")
    assert response.status_code == 404
