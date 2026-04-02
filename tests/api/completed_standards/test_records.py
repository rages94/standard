from datetime import date, timedelta

import pytest
from httpx import AsyncClient

from src.data.models import Standard, User
from tests.factories.completed_standards import CompletedStandardCreateFactory


async def test_create_completed_standard_updates_daily_stats(
    auth_client: AsyncClient,
    standard: Standard,
    default_user: User,
):
    data = CompletedStandardCreateFactory.build(
        standard_id=standard.id,
        weight=None,
        count=10.0,
    )
    response = await auth_client.post(
        "/completed_standards/", content=data.model_dump_json()
    )
    assert response.status_code == 201


async def test_create_completed_standard_sets_daily_record(
    auth_client: AsyncClient,
    standard: Standard,
    default_user: User,
):
    data = CompletedStandardCreateFactory.build(
        standard_id=standard.id,
        weight=None,
        count=50.0,
    )
    response = await auth_client.post(
        "/completed_standards/", content=data.model_dump_json()
    )
    assert response.status_code == 201

    dashboard_response = await auth_client.get("/users/dashboard/")
    assert dashboard_response.status_code == 200
    dashboard = dashboard_response.json()
    assert dashboard["daily_record"] > 0


async def test_delete_completed_standard_recalculates_records(
    auth_client: AsyncClient,
    standard: Standard,
    default_user: User,
):
    data = CompletedStandardCreateFactory.build(
        standard_id=standard.id,
        weight=None,
        count=100.0,
    )
    create_response = await auth_client.post(
        "/completed_standards/", content=data.model_dump_json()
    )
    assert create_response.status_code == 201
    cs_id = create_response.json()["completed_standard"]["id"]

    delete_response = await auth_client.delete(f"/completed_standards/{cs_id}")
    assert delete_response.status_code == 204

    dashboard_response = await auth_client.get("/users/dashboard/")
    assert dashboard_response.status_code == 200
    dashboard = dashboard_response.json()
    assert dashboard["daily_record"] == 0


async def test_dashboard_returns_records(
    auth_client: AsyncClient,
    default_user: User,
):
    response = await auth_client.get("/users/dashboard/")
    assert response.status_code == 200
    data = response.json()
    assert "daily_record" in data
    assert "weekly_record" in data
    assert isinstance(data["daily_record"], (int, float))
    assert isinstance(data["weekly_record"], (int, float))
