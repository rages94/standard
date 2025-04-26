from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter, LimitOffsetFilter, OrderingFilter, OrderingField

from src.common.repository.base import Repository
from src.data.models import Standard


class StandardFilterSet(BaseFilterSet):
    id = Filter(Standard.id)
    name = Filter(Standard.name)
    pagination = LimitOffsetFilter()
    order = OrderingFilter(
        created_at=OrderingField(Standard.created_at),
    )

class StandardRepository(
    Repository[
        Standard,
        StandardFilterSet,
        AsyncSession,
    ]
):
    model = Standard
    filter_set = StandardFilterSet
    query = select(Standard).where(Standard.is_deleted.is_(False))
