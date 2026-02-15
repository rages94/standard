from uuid import uuid4

from httpx import AsyncClient

from src.data.models import LiabilityTemplate
from tests.factories.liabilities import LiabilityCreateFactory


async def test_create_liability_basic(
    auth_client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    data = LiabilityCreateFactory.build(liability_template_id=liability_template.id)
    response = await auth_client.post("/liabilities/", content=data.model_dump_json())
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["count"] == data.count
    assert response_data["liability_template_id"] == str(liability_template.id)


async def test_create_liability_requires_auth(client: AsyncClient) -> None:
    data = LiabilityCreateFactory.build()
    response = await client.post("/liabilities/", content=data.model_dump_json())
    assert response.status_code == 401


async def test_create_liability_invalid_data(
    auth_client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    invalid_data = {"liability_template_id": str(liability_template.id), "count": -5.0}
    response = await auth_client.post("/liabilities/", json=invalid_data)
    assert response.status_code == 422


async def test_create_liability_missing_template(auth_client: AsyncClient) -> None:
    data = LiabilityCreateFactory.build(liability_template_id=uuid4())
    response = await auth_client.post("/liabilities/", content=data.model_dump_json())
    assert response.status_code == 404
