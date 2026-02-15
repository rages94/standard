from httpx import AsyncClient

from src.data.models import User
from tests.factories.users import UserCreateFactory


async def test_register_user_success(client: AsyncClient) -> None:
    data = UserCreateFactory.build()
    response = await client.post("/users/register/", json=data.model_dump())
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["username"] == data.username
    assert "id" in response_data
    assert "created_at" in response_data


async def test_register_user_duplicate_username(
    client: AsyncClient, default_user: User
) -> None:
    data = UserCreateFactory.build(username=default_user.username)
    response = await client.post("/users/register/", json=data.model_dump())
    assert response.status_code == 400
    assert "уже существует" in response.json()["detail"]


async def test_register_user_invalid_data(client: AsyncClient) -> None:
    # Missing password
    data = {"username": "testuser"}
    response = await client.post("/users/register/", json=data)
    assert response.status_code == 422

    # Missing username
    data = {"password": "password123"}
    response = await client.post("/users/register/", json=data)
    assert response.status_code == 422