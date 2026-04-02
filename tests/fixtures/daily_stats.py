from datetime import date, timedelta

import pytest

from src.data.models import User
from tests.factories.daily_stats import DailyStatsFactory


@pytest.fixture
async def daily_stats_today(default_user: User):
    return await DailyStatsFactory.create_async(
        user_id=default_user.id,
        date=date.today(),
        total_count=50.0,
    )


@pytest.fixture
async def daily_stats_yesterday(default_user: User):
    return await DailyStatsFactory.create_async(
        user_id=default_user.id,
        date=date.today() - timedelta(days=1),
        total_count=100.0,
    )
