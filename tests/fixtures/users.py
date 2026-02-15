import pytest

from src.data.models import User
from tests.factories.users import UserFactory


@pytest.fixture
async def default_user(_container) -> User:
    return await UserFactory.create_async(username="testuser")


@pytest.fixture
async def user(_container) -> User:
    return await UserFactory.create_async()
