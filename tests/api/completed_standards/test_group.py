from httpx import AsyncClient

from src.data.models import CompletedStandard, Standard


async def test_grouped_list(
    auth_client: AsyncClient,
    standard: Standard,
    completed_standard: CompletedStandard,
    completed_standard_weight: CompletedStandard,
):
    response = await auth_client.get("/completed_standards/grouped/")
    assert response.status_code == 200
    data = response.json()
    assert "labels" in data
    assert "datasets" in data
    assert len(data["labels"]) == 2
    assert len(data["datasets"]) == 1
    assert data["datasets"][0]["label"] == standard.name
    assert (
        sum(data["datasets"][0]["data"])
        == completed_standard.total_norm + completed_standard_weight.total_norm
    )
