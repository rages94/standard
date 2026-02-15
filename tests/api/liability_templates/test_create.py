from httpx import AsyncClient

from src.data.models import User
from tests.factories.liability_templates import LiabilityTemplateCreateFactory


async def test_create_liability_template_basic(
    auth_client: AsyncClient, default_user: User
) -> None:
    data = LiabilityTemplateCreateFactory.build()
    response = await auth_client.post(
        "/liability_templates/", content=data.model_dump_json()
    )
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == data.name
    assert response_data["count"] == data.count
    assert response_data["normal_form"] is None
    assert "is_deleted" not in response_data


async def test_create_liability_template_requires_auth(client: AsyncClient) -> None:
    data = LiabilityTemplateCreateFactory.build()
    response = await client.post(
        "/liability_templates/", content=data.model_dump_json()
    )
    assert response.status_code == 401


async def test_create_liability_template_invalid_data(auth_client: AsyncClient) -> None:
    invalid_data = {"name": "", "count": -5.0}
    response = await auth_client.post("/liability_templates/", json=invalid_data)
    assert response.status_code == 422
