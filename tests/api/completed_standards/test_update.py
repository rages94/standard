
from httpx import AsyncClient

from src.data.models.completed_standard import (
    CompletedStandard,
    CompletedStandardUpdate,
)


async def test_update_completed_standard(
    auth_client: AsyncClient,
    completed_standard: CompletedStandard,
):
    new_count = 99.0
    data = CompletedStandardUpdate(count=new_count)
    response = await auth_client.patch(
        f"/completed_standards/{completed_standard.id}",
        content=data.model_dump_json(),
    )
    assert response.status_code == 200
    json = response.json()
    assert json["count"] == new_count


async def test_update_completed_standard_not_owned(
    auth_client: AsyncClient,
    completed_standard_another_user: CompletedStandard,
):
    data = CompletedStandardUpdate(count=1.0)
    response = await auth_client.patch(
        f"/completed_standards/{completed_standard_another_user.id}",
        content=data.model_dump_json(),
    )
    assert response.status_code == 404


async def test_create_completed_standard_requires_auth(
    client: AsyncClient,
    completed_standard: CompletedStandard,
):
    data = CompletedStandardUpdate()
    response = await client.patch(
        f"/completed_standards/{completed_standard.id}",
        content=data.model_dump_json(),
    )
    assert response.status_code == 401
