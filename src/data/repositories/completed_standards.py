from collections import defaultdict
from datetime import timedelta, datetime
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy_filterset import BaseFilterSet, Filter, LimitOffsetFilter, OrderingFilter, OrderingField

from src.common.repository.base import Repository
from src.data.models import CompletedStandard, Standard, User
from src.domain.completed_standards.dto.output import (
    GroupedCompletedStandard,
    Dataset,
    RatingGroupedCompletedStandard,
    UserCompletedStandard,
)


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
    query = select(CompletedStandard).options(joinedload(CompletedStandard.standard)).order_by(CompletedStandard.created_at.desc())

    async def grouped_list(self, user_id: UUID, as_standard: bool = False) -> GroupedCompletedStandard:
        query = select(
            Standard.name,
            func.date_trunc("day", CompletedStandard.created_at).label('date_created'),
            func.sum(CompletedStandard.count) if not as_standard else func.sum(CompletedStandard.count) / Standard.count,
        ).join(CompletedStandard.standard).group_by(
            Standard.name,
            Standard.count,
            'date_created',
        ).where(CompletedStandard.user_id == user_id).order_by("date_created")
        results = (await self.session.execute(query)).all()
        data = defaultdict(dict)
        names = set()
        for name, date_created, count in results:
            names.add(name)
            data[date_created][name] = round(count)
        result = GroupedCompletedStandard(labels=data.keys(), datasets=[])
        for name in names:
            values = []
            for date_created, v in data.items():
                values.append(v.get(name, 0))
            result.datasets.append(Dataset(label=name, data=values))
        return result

    async def rating_list(self, days: int | None = None) -> list[RatingGroupedCompletedStandard]:
        query = select(
            User.username,
            Standard.name,
            func.sum(CompletedStandard.count),
            func.sum(CompletedStandard.count) / Standard.count,
        ).join(CompletedStandard.standard).join(CompletedStandard.user).group_by(
            User.username,
            Standard.name,
            Standard.count,
        ).where(Standard.is_deleted == False).order_by(func.sum(CompletedStandard.count).desc())
        if days:
            query = query.filter(CompletedStandard.created_at >= datetime.now() - timedelta(days=days))
        results = (await self.session.execute(query)).all()
        data = defaultdict(list)
        all_standards = defaultdict(int)
        for username, standard_name, count, standards in results:
            data[standard_name].append(UserCompletedStandard(username=username, count=count, standards=round(standards)))
            all_standards[username] += round(standards)
        data["Все упражнения"] = sorted(
            [UserCompletedStandard(username=u, count=0, standards=s) for u, s in all_standards.items()],
            key=lambda x: x.standards,
            reverse=True,
        )
        return [
            RatingGroupedCompletedStandard(standard_name=standard_name, user_ratings=ratings)
            for standard_name, ratings in data.items()
        ]
