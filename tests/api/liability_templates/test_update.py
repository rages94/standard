from uuid import uuid4

from httpx import AsyncClient

from src.data.models import LiabilityTemplate


async def test_update_liability_template_basic(
    auth_client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    update_data = {"name": "Updated Name", "count": 99.9}
    response = await auth_client.patch(
        f"/liability_templates/{liability_template.id}",
        json=update_data,
    )
    assert response.status_code == 200
    json = response.json()
    assert json["name"] == update_data["name"]
    assert json["count"] == update_data["count"]
    assert json["id"] == str(liability_template.id)


async def test_update_liability_template_partial(
    auth_client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    update_data = {"count": 50.5}
    response = await auth_client.patch(
        f"/liability_templates/{liability_template.id}",
        json=update_data,
    )
    assert response.status_code == 200
    json = response.json()
    assert json["count"] == update_data["count"]
    assert json["name"] == liability_template.name  # Имя не изменилось


async def test_update_liability_template_not_found(auth_client: AsyncClient) -> None:
    fake_id = uuid4()
    response = await auth_client.patch(
        f"/liability_templates/{fake_id}",
        json={"name": "Hacker Attempt"},
    )
    assert response.status_code == 404


async def test_update_liability_template_other_user(
    auth_client: AsyncClient,
    liability_template_another_user: LiabilityTemplate,
) -> None:
    # Попытка обновить шаблон другого пользователя
    response = await auth_client.patch(
        f"/liability_templates/{liability_template_another_user.id}",
        json={"name": "Stolen Template"},
    )
    assert response.status_code == 404


async def test_update_liability_template_requires_auth(
    client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    response = await client.patch(
        f"/liability_templates/{liability_template.id}",
        json={"name": "Unauthorized"},
    )
    assert response.status_code == 401
