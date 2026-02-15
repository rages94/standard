from httpx import AsyncClient

from src.data.models import User


async def test_get_current_user_success(auth_client: AsyncClient, default_user: User) -> None:
    response = await auth_client.get("/users/me/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(default_user.id)
    assert data["username"] == default_user.username


async def test_get_current_user_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/users/me/")
    assert response.status_code == 401


async def test_update_user_success(auth_client: AsyncClient, default_user: User) -> None:
    update_data = {"weight": 75.5, "sex": "female"}
    response = await auth_client.patch("/users/me/", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(default_user.id)
    assert data["weight"] == update_data["weight"]
    assert data["sex"] == update_data["sex"]
    assert data["username"] == default_user.username  # unchanged


async def test_update_user_partial(auth_client: AsyncClient, default_user: User) -> None:
    # Update only weight
    update_data = {"weight": 80.0}
    response = await auth_client.patch("/users/me/", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["weight"] == update_data["weight"]
    assert data["username"] == default_user.username  # unchanged

    # Update only email
    update_data = {"email": "test@example.com"}
    response = await auth_client.patch("/users/me/", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == update_data["email"]


async def test_update_user_requires_auth(client: AsyncClient) -> None:
    update_data = {"weight": 75.0}
    response = await client.patch("/users/me/", json=update_data)
    assert response.status_code == 401