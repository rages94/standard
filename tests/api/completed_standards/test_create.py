from uuid import uuid4

import pytest
from httpx import AsyncClient

from src.config import Settings
from src.data.models import Standard
from src.domain.math.services.normalization import ExerciseNormalizationService
from src.domain.user.dto.enums import CompletedType
from tests.factories.completed_standards import CompletedStandardCreateFactory
from tests.factories.standards import StandardCreateFactory

settings = Settings()


async def test_create_completed_standard_basic(
    auth_client: AsyncClient,
    standard: Standard,
):
    data = CompletedStandardCreateFactory.build(
        standard_id=standard.id,
        weight=None,
    )
    response = await auth_client.post(
        "/completed_standards/", content=data.model_dump_json()
    )
    assert response.status_code == 201
    json = response.json()
    assert json["standard_id"] == str(standard.id)
    assert json["count"] == data.count
    assert json["user_weight"] == data.user_weight
    assert json["weight"] is None
    assert json["total_norm"] == data.count / float(standard.count)


async def test_create_standard_duplicate_name(
    auth_client: AsyncClient, standard: Standard
):
    data = StandardCreateFactory.build(name=standard.name)
    response = await auth_client.post("/standards/", content=data.model_dump_json())
    assert response.status_code == 409


async def test_create_completed_standard_with_weight_and_normalization(
    auth_client: AsyncClient,
    standard: Standard,
    monkeypatch,
):
    normalization_count = 2.5

    def mock_normalization(*args, **kwargs):
        return normalization_count

    monkeypatch.setattr(
        ExerciseNormalizationService, "normalization", staticmethod(mock_normalization)
    )

    data = CompletedStandardCreateFactory.build(
        standard_id=standard.id,
        completed_type="count",
    )
    response = await auth_client.post(
        "/completed_standards/", content=data.model_dump_json()
    )
    assert response.status_code == 201
    json = response.json()
    assert json["total_norm"] == normalization_count * data.count


async def test_create_completed_standard_missing_standard(auth_client: AsyncClient):
    fake_std_id = uuid4()
    data = CompletedStandardCreateFactory.build(standard_id=fake_std_id)
    response = await auth_client.post(
        "/completed_standards/", content=data.model_dump_json()
    )
    assert response.status_code == 404


async def test_create_completed_standard_requires_auth(client: AsyncClient):
    data = CompletedStandardCreateFactory.build()
    response = await client.post(
        "/completed_standards/", content=data.model_dump_json()
    )
    assert response.status_code == 401
