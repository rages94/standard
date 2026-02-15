from httpx import AsyncClient


async def test_refresh_tokens_success(refresh_client: AsyncClient) -> None:
    response = await refresh_client.post("/tokens/refresh")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert isinstance(data["access_token"], str)
    assert isinstance(data["refresh_token"], str)
    assert len(data["access_token"]) > 0
    assert len(data["refresh_token"]) > 0


async def test_refresh_tokens_without_token(client: AsyncClient) -> None:
    response = await client.post("/tokens/refresh")
    assert response.status_code == 401


async def test_refresh_tokens_with_invalid_token(client: AsyncClient) -> None:
    headers = {"Authorization": "Bearer invalid_token"}
    response = await client.post("/tokens/refresh", headers=headers)
    assert response.status_code == 401


async def test_refresh_tokens_with_access_token(auth_client: AsyncClient) -> None:
    # auth_client uses access token, not refresh token
    response = await auth_client.post("/tokens/refresh")
    assert response.status_code == 401