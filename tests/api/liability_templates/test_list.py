from httpx import AsyncClient

from src.data.models import LiabilityTemplate, User


async def test_list_liability_templates_empty(auth_client: AsyncClient) -> None:
    response = await auth_client.get("/liability_templates/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


async def test_list_liability_templates_returns_authored_only(
    auth_client: AsyncClient,
    liability_template: LiabilityTemplate,
    liability_template_another_user: LiabilityTemplate,
    default_user: User,
) -> None:
    response = await auth_client.get("/liability_templates/")
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) == 1
    assert templates[0]["id"] == str(liability_template.id)
    assert templates[0]["name"] == liability_template.name
    assert templates[0]["count"] == liability_template.count


async def test_list_liability_templates_excludes_deleted(
    auth_client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    delete_response = await auth_client.delete(
        f"/liability_templates/{liability_template.id}"
    )
    assert delete_response.status_code == 204

    response = await auth_client.get("/liability_templates/")
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) == 0


async def test_list_liability_templates_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/liability_templates/")
    assert response.status_code == 401
