from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy_filterset import BaseFilterSet, Filter, LimitOffsetFilter, OrderingFilter, OrderingField

from src.common.repository.base import Repository
from src.data.models import Liability


class LiabilityFilterSet(BaseFilterSet):
    id = Filter(Liability.id)
    liability_template_id = Filter(Liability.liability_template_id)
    user_id = Filter(Liability.user_id)
    pagination = LimitOffsetFilter()
    order = OrderingFilter(
        created_at=OrderingField(Liability.created_at),
    )

class LiabilityRepository(
    Repository[
        Liability,
        LiabilityFilterSet,
        AsyncSession,
    ]
):
    model = Liability
    filter_set = LiabilityFilterSet
    query = select(Liability).options(joinedload(Liability.liability_template)).order_by(Liability.created_at.desc())
