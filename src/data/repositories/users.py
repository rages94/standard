from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy_filterset import BaseFilterSet, Filter, LimitOffsetFilter, OrderingFilter, OrderingField

from src.common.repository.base import Repository
from src.data.models import User, Liability, CompletedStandard


class UserFilterSet(BaseFilterSet):
    id = Filter(User.id)
    username = Filter(User.username)
    pagination = LimitOffsetFilter()
    order = OrderingFilter(
        created_at=OrderingField(User.created_at),
    )

class UserRepository(
    Repository[
        User,
        UserFilterSet,
        AsyncSession,
    ]
):
    model = User
    filter_set = UserFilterSet
    query = select(User)

    async def update_total_liabilities(self, user_id: UUID) -> None:
        liability_query = (
            select(Liability)
            .where(Liability.user_id == user_id)
            .options(joinedload(Liability.liability_template))
        )
        completed_standard_query = (
            select(CompletedStandard)
            .where(CompletedStandard.user_id == user_id)
            .options(joinedload(CompletedStandard.standard))
        )
        liabilities = (await self.session.execute(liability_query)).unique().scalars().all()
        completed_standards = (await self.session.execute(completed_standard_query)).unique().scalars().all()
        total = 0
        for liability in liabilities:
            total += liability.count * (liability.liability_template.count if liability.liability_template else 1)

        for completed_standard in completed_standards:
            total -= completed_standard.count // completed_standard.standard.count

        query = (
            update(User)
            .values({'total_liabilities': total})
            .where(User.id == user_id)
        )
        result = await self.session.execute(query)
        if result.rowcount != 1:
            raise NoResultFound
