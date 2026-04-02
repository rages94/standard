import operator as op
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter

from src.common.repository.base import Repository
from src.data.models import UserRecord


class UserRecordFilterSet(BaseFilterSet):
    id = Filter(UserRecord.id)
    user_id = Filter(UserRecord.user_id)
    type = Filter(UserRecord.type)
    count_lt = Filter(UserRecord.count, lookup_expr=op.lt)


class UserRecordRepository(Repository[UserRecord, UserRecordFilterSet, AsyncSession]):
    model = UserRecord
    filter_set = UserRecordFilterSet
    query = select(UserRecord)

    async def get_records(self, user_id: UUID) -> dict[str, float]:
        query = (
            select(UserRecord.type, func.max(UserRecord.count))
            .where(UserRecord.user_id == user_id)
            .group_by(UserRecord.type)
        )
        result = await self.session.execute(query)
        return {row[0]: row[1] for row in result.all()}
