from uuid import uuid4

from httpx import AsyncClient

from src.data.models import LiabilityTemplate


async def test_delete_liability_template_basic(
    auth_client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    response = await auth_client.delete(f"/liability_templates/{liability_template.id}")
    assert response.status_code == 204
    assert response.content == b""


async def test_delete_liability_template_not_found(auth_client: AsyncClient) -> None:
    fake_id = uuid4()
    response = await auth_client.delete(f"/liability_templates/{fake_id}")
    assert response.status_code == 404


async def test_delete_liability_template_other_user(
    auth_client: AsyncClient,
    liability_template_another_user: LiabilityTemplate,
) -> None:
    response = await auth_client.delete(
        f"/liability_templates/{liability_template_another_user.id}"
    )
    assert response.status_code == 404


async def test_delete_liability_template_requires_auth(
    client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    response = await client.delete(f"/liability_templates/{liability_template.id}")
    assert response.status_code == 401


async def test_delete_already_deleted_template(
    auth_client: AsyncClient, liability_template: LiabilityTemplate
) -> None:
    # Первое удаление
    first_response = await auth_client.delete(
        f"/liability_templates/{liability_template.id}"
    )
    assert first_response.status_code == 204

    # Повторное удаление того же шаблона
    second_response = await auth_client.delete(
        f"/liability_templates/{liability_template.id}"
    )
    # После первого удаления шаблон помечен как is_deleted=True,
    # поэтому при поиске по user_id + id он не будет найден (404)
    assert second_response.status_code == 404
