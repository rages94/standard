import pytest

from src.domain.math.dto.enums import ExerciseEnum
from tests.factories.standards import StandardFactory


@pytest.fixture
async def standard():
    return await StandardFactory.create_async(
        name=ExerciseEnum.deadlift, is_deleted=False
    )
