import operator as op
from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_filterset import BaseFilterSet, Filter

from src.common.repository.base import Repository
from src.data.models import DailyStats, CompletedStandard


class DailyStatsFilterSet(BaseFilterSet):
    id = Filter(DailyStats.id)
    user_id = Filter(DailyStats.user_id)
    date = Filter(DailyStats.date)
    date_gte = Filter(DailyStats.date, lookup_expr=op.ge)
    date_lte = Filter(DailyStats.date, lookup_expr=op.le)


class DailyStatsRepository(Repository[DailyStats, DailyStatsFilterSet, AsyncSession]):
    model = DailyStats
    filter_set = DailyStatsFilterSet
    query = select(DailyStats)

    async def upsert_daily_stats(
        self, user_id: UUID, activity_date: date, total_norm: float
    ) -> DailyStats:
        stmt = (
            pg_insert(DailyStats.__table__)
            .values(user_id=user_id, date=activity_date, total_count=total_norm)
            .on_conflict_do_update(
                constraint="uq_daily_stats_user_date",
                set_={"total_count": DailyStats.__table__.c.total_count + total_norm},
            )
            .returning(DailyStats.__table__)
        )
        result = await self.session.execute(stmt)
        row = result.one()
        return DailyStats(
            id=row.id,
            user_id=row.user_id,
            date=row.date,
            total_count=row.total_count,
        )

    async def recalculate_daily_stats(
        self, user_id: UUID, activity_date: date
    ) -> float:
        query = (
            select(func.sum(CompletedStandard.total_norm))
            .where(CompletedStandard.user_id == user_id)
            .where(func.date(CompletedStandard.created_at) == activity_date)
        )
        result = await self.session.execute(query)
        total = float(result.scalar() or 0)

        stmt = (
            pg_insert(DailyStats.__table__)
            .values(user_id=user_id, date=activity_date, total_count=total)
            .on_conflict_do_update(
                constraint="uq_daily_stats_user_date",
                set_={"total_count": total},
            )
        )
        await self.session.execute(stmt)
        return total

    async def get_week_total(
        self, user_id: UUID, week_start: date, week_end: date
    ) -> float:
        query = (
            select(func.sum(DailyStats.total_count))
            .where(DailyStats.user_id == user_id)
            .where(DailyStats.date >= week_start)
            .where(DailyStats.date < week_end)
        )
        result = await self.session.execute(query)
        return float(result.scalar() or 0)
