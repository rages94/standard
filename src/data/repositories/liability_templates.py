from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import (
    BaseFilterSet,
    Filter,
    LimitOffsetFilter,
    OrderingField,
    OrderingFilter,
)

from src.common.repository.base import Repository
from src.data.models import LiabilityTemplate


class LiabilityTemplateFilterSet(BaseFilterSet):
    id = Filter(LiabilityTemplate.id)
    user_id = Filter(LiabilityTemplate.user_id)
    is_deleted = Filter(LiabilityTemplate.is_deleted)
    pagination = LimitOffsetFilter()
    order = OrderingFilter(
        created_at=OrderingField(LiabilityTemplate.created_at),
    )

class LiabilityTemplateRepository(
    Repository[
        LiabilityTemplate,
        LiabilityTemplateFilterSet,
        AsyncSession,
    ]
):
    model = LiabilityTemplate
    filter_set = LiabilityTemplateFilterSet
    query = select(LiabilityTemplate).where(LiabilityTemplate.is_deleted == False)  # type: ignore
