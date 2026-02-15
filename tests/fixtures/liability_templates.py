import pytest

from src.data.models import LiabilityTemplate, User
from tests.factories.liability_templates import LiabilityTemplateFactory


@pytest.fixture
async def liability_template(default_user: User) -> LiabilityTemplate:
    return await LiabilityTemplateFactory.create_async(
        user_id=default_user.id, is_deleted=False
    )


@pytest.fixture
async def liability_template_another_user(user: User) -> LiabilityTemplate:
    return await LiabilityTemplateFactory.create_async(
        user_id=user.id, is_deleted=False
    )
