import pytest

from src.data.models import Liability, LiabilityTemplate, User
from tests.factories.liabilities import LiabilityFactory


@pytest.fixture
async def liability(default_user: User, liability_template: LiabilityTemplate) -> Liability:
    return await LiabilityFactory.create_async(
        user_id=default_user.id,
        liability_template_id=liability_template.id,
    )


@pytest.fixture
async def liability_another_user(user: User, liability_template: LiabilityTemplate) -> Liability:
    return await LiabilityFactory.create_async(
        user_id=user.id,
        liability_template_id=liability_template.id,
    )