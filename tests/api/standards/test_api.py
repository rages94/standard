from httpx import AsyncClient

from src.config import Settings
from src.data.models import Standard
from tests.factories.standards import StandardCreateFactory, StandardUpdateFactory

settings = Settings()


async def test_create_standard(auth_client: AsyncClient):
    data = StandardCreateFactory.build()
    response = await auth_client.post("/standards/", content=data.model_dump_json())
    response_data = response.json()
    assert response.status_code == 201
    assert "created_at" in response_data and response_data["created_at"] is not None


async def test_update_standard(auth_client: AsyncClient, standard: Standard):
    data = StandardUpdateFactory.build()
    response = await auth_client.patch(
        f"/standards/{standard.id}", content=data.model_dump_json()
    )
    assert response.status_code == 200


async def test_list_standards(auth_client: AsyncClient, standard: Standard):
    response = await auth_client.get("/standards/")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_delete_standard(auth_client: AsyncClient, standard: Standard):
    response = await auth_client.delete(f"/standards/{standard.id}")
    assert response.status_code == 204


async def test_list_does_not_include_deleted_standards(
    auth_client: AsyncClient, standard: Standard
):
    response = await auth_client.get("/standards/")
    assert response.status_code == 200
    ids_before = [item["id"] for item in response.json()]
    assert str(standard.id) in ids_before

    response = await auth_client.delete(f"/standards/{standard.id}")
    assert response.status_code == 204

    response = await auth_client.get("/standards/")
    assert response.status_code == 200
    ids_after = [item["id"] for item in response.json()]
    assert str(standard.id) not in ids_after


async def test_update_standard_partial(auth_client: AsyncClient, standard: Standard):
    response = await auth_client.patch(f"/standards/{standard.id}", json={"count": 999})
    assert response.status_code == 200
    updated = response.json()
    assert updated["count"] == "999"
    assert updated["name"] == standard.name


async def test_update_nonexistent_standard(auth_client: AsyncClient):
    fake_id = "00000000-0000-0000-0000-000000000000"
    data = StandardUpdateFactory.build()
    response = await auth_client.patch(
        f"/standards/{fake_id}", content=data.model_dump_json()
    )
    assert response.status_code == 404


async def test_cannot_override_is_deleted_via_patch(
    auth_client: AsyncClient, standard: Standard
):
    assert standard.is_deleted is False
    response = await auth_client.patch(
        f"/standards/{standard.id}", json={"is_deleted": True}
    )
    assert response.status_code == 200

    response = await auth_client.get("/standards/")
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_list_standard_requires_auth(client: AsyncClient):
    response = await client.get("/standards/")
    assert response.status_code == 401
