from httpx import AsyncClient

from src.data.models import User
from tests.factories.users import UserLoginFactory


async def test_login_success(client: AsyncClient, default_user: User) -> None:
    data = UserLoginFactory.build(username=default_user.username, password="password")
    response = await client.post("/users/login/", json=data.model_dump())
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert isinstance(response_data["access_token"], str)
    assert isinstance(response_data["refresh_token"], str)
    assert len(response_data["access_token"]) > 0
    assert len(response_data["refresh_token"]) > 0


async def test_login_invalid_password(client: AsyncClient, default_user: User) -> None:
    data = UserLoginFactory.build(
        username=default_user.username, password="wrongpassword"
    )
    response = await client.post("/users/login/", json=data.model_dump())
    assert response.status_code == 401
    assert "Неверный" in response.json()["detail"]


async def test_login_user_not_found(client: AsyncClient) -> None:
    data = UserLoginFactory.build()
    response = await client.post("/users/login/", json=data.model_dump())
    assert response.status_code == 401
    assert "Неверный" in response.json()["detail"]


async def test_login_missing_fields(client: AsyncClient) -> None:
    # Missing password
    data = {"username": "testuser"}
    response = await client.post("/users/login/", json=data)
    assert response.status_code == 422

    # Missing username
    data = {"password": "password123"}
    response = await client.post("/users/login/", json=data)
    assert response.status_code == 422
