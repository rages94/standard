from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter, LimitOffsetFilter, OrderingFilter, OrderingField

from src.common.repository.base import Repository
from src.data.models import CompletedStandard


class CompletedStandardFilterSet(BaseFilterSet):
    id = Filter(CompletedStandard.id)
    standard_id = Filter(CompletedStandard.standard_id)
    user_id = Filter(CompletedStandard.user_id)
    pagination = LimitOffsetFilter()
    order = OrderingFilter(
        created_at=OrderingField(CompletedStandard.created_at),
    )

class CompletedStandardRepository(
    Repository[
        CompletedStandard,
        CompletedStandardFilterSet,
        AsyncSession,
    ]
):
    model = CompletedStandard
    filter_set = CompletedStandardFilterSet
    query = select(CompletedStandard)
