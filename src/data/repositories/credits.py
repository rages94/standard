import operator as op
from datetime import datetime
from uuid import UUID

from dateutil.relativedelta import relativedelta
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter, OrderingFilter, OrderingField, LimitOffsetFilter

from src.common.repository.base import Repository
from src.data.models import Credit


class CreditFilterSet(BaseFilterSet):
    id = Filter(Credit.id)
    user_id = Filter(Credit.user_id)
    completed = Filter(Credit.completed)
    order = OrderingFilter(
        created_at=OrderingField(Credit.created_at),
    )
    deadline_date_ge = Filter(Credit.deadline_date, lookup_expr=op.ge)
    deadline_date_lt = Filter(Credit.deadline_date, lookup_expr=op.lt)
    pagination = LimitOffsetFilter()


class CreditRepository(
    Repository[
        Credit,
        CreditFilterSet,
        AsyncSession,
    ]
):
    model = Credit
    filter_set = CreditFilterSet
    query = select(Credit).order_by(Credit.created_at.desc())

    async def update_completed_count(self, user_id: UUID, completed_count: int) -> None:
        params = dict(user_id=user_id, deadline_date_ge=datetime.now())
        credit = await self.get_one(params)
        credit.completed_count += completed_count
        if credit.completed_count >= credit.count and not credit.completed:
            credit.completed_at = datetime.now()
            credit.completed = True
        self.session.add(credit)
        await self.session.flush()

    async def mark_uncompleted(self) -> None:
        params = dict(deadline_date_lt=datetime.now(), completed=None)
        query = (
            update(Credit)
            .values({'completed': False})
        )
        filtered_query = self.filter_set(query).filter_query(params)  # noqa
        await self.session.execute(filtered_query)
        await self.session.flush()

    # TODO by user settings
    async def create_by_user(self, user_id: UUID, total_liabilities: int) -> None:
        params = dict(user_id=user_id, deadline_date_ge=datetime.now())
        try:
            await self.get_one(params)
            return
        except NoResultFound:
            pass

        now = datetime.now()
        count_credit_months = 13 - now.month
        credit = Credit(
            count=total_liabilities//count_credit_months,
            user_id=user_id,
            completed_count=0,
            deadline_date=now.date() + relativedelta(months=1),
        )
        self.session.add(credit)
        await self.session.flush()
