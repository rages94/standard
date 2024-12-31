from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter, LimitOffsetFilter, OrderingFilter, OrderingField

from src.common.repository.base import Repository
from src.data.models import LiabilityTemplate


class LiabilityTemplateFilterSet(BaseFilterSet):
    id = Filter(LiabilityTemplate.id)
    user_id = Filter(LiabilityTemplate.user_id)
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
    query = select(LiabilityTemplate)
