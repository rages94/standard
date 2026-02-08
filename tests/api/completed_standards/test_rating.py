from httpx import AsyncClient

from src.data.models import CompletedStandard


async def test_rating_list_empty(auth_client: AsyncClient):
    response = await auth_client.get("/completed_standards/rating/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["standard_name"] == "Все упражнения"


async def test_rating_list(
    auth_client: AsyncClient,
    completed_standard: CompletedStandard,
    completed_standard_weight: CompletedStandard,
):
    response = await auth_client.get("/completed_standards/rating/?period_days=0")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for standard in data:
        if standard["standard_name"] == "Все упражнения":
            assert (
                standard["user_ratings"][0]["standards"]
                == completed_standard.total_norm + completed_standard_weight.total_norm
            )
        else:
            assert (
                standard["user_ratings"][0]["count"]
                == completed_standard.count + completed_standard_weight.count
            )


async def test_rating_requires_auth(client: AsyncClient):
    response = await client.get("/completed_standards/rating/")
    assert response.status_code == 401
