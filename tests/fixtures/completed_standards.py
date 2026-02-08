import pytest

from src.data.models import Standard, User
from src.domain.math.dto.enums import ExerciseEnum
from tests.factories.completed_standards import CompletedStandardFactory
from tests.factories.standards import StandardFactory


@pytest.fixture
async def completed_standard(default_user: User, standard: Standard):
    return await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        weight=None,
        standard_id=standard.id,
    )


@pytest.fixture
async def completed_standard_weight(default_user: User, standard: Standard):
    return await CompletedStandardFactory.create_async(
        user_id=default_user.id,
        standard_id=standard.id,
    )


@pytest.fixture
async def completed_standard_another_user(user: User, standard: Standard):
    return await CompletedStandardFactory.create_async(
        user_id=user.id,
        weight=None,
        standard_id=standard.id,
    )
