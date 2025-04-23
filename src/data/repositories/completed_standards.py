from collections import defaultdict
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter, LimitOffsetFilter, OrderingFilter, OrderingField

from src.common.repository.base import Repository
from src.data.models import CompletedStandard, Standard
from src.domain.completed_standards.dto.output import GroupedCompletedStandard, Dataset


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

    async def grouped_list(self, user_id: UUID) -> GroupedCompletedStandard:
        query = select(
            Standard.name,
            func.date_trunc("day", CompletedStandard.created_at).label('date_created'),
            func.sum(CompletedStandard.count),
        ).join(CompletedStandard.standard).group_by(
            Standard.name,
            'date_created',
        ).where(CompletedStandard.user_id == user_id).order_by("date_created")
        results = (await self.session.execute(query)).all()
        data = defaultdict(dict)
        names = set()
        for name, date_created, count in results:
            names.add(name)
            data[date_created][name] = count
        result = GroupedCompletedStandard(labels=data.keys(), datasets=[])
        for name in names:
            values = []
            for date_created, v in data.items():
                values.append(v.get(name, 0))
            result.datasets.append(Dataset(label=name, data=values))
        return result
