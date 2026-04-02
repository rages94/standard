from datetime import date, timedelta
from uuid import UUID

from loguru import logger

from src.common.models.mixins import moscow_now
from src.data.uow import UnitOfWork


class UpdateRecords:
    async def __call__(
        self, uow: UnitOfWork, user_id: UUID, activity_date: date, total_norm: float
    ) -> None:
        await uow.daily_stats_repo.upsert_daily_stats(
            user_id, activity_date, total_norm
        )
        await uow.flush()

        daily_total = await uow.daily_stats_repo.recalculate_daily_stats(
            user_id, activity_date
        )
        await self._update_daily_record(uow, user_id, daily_total)

        now = moscow_now()
        week_start = (now - timedelta(days=now.weekday())).date()
        week_end = week_start + timedelta(days=7)
        week_total = await uow.daily_stats_repo.get_week_total(
            user_id, week_start, week_end
        )
        await self._update_weekly_record(uow, user_id, week_total)

    async def recalculate_after_delete(
        self, uow: UnitOfWork, user_id: UUID, activity_date: date
    ) -> None:
        daily_total = await uow.daily_stats_repo.recalculate_daily_stats(
            user_id, activity_date
        )
        await uow.flush()

        records = await uow.user_record_repo.get_records(user_id)
        current_daily = records.get("daily", 0)
        if daily_total < current_daily:
            await self._find_and_set_best_daily(uow, user_id)

        now = moscow_now()
        week_start = (now - timedelta(days=now.weekday())).date()
        week_end = week_start + timedelta(days=7)
        week_total = await uow.daily_stats_repo.get_week_total(
            user_id, week_start, week_end
        )
        current_weekly = records.get("weekly", 0)
        if week_total < current_weekly:
            await self._find_and_set_best_weekly(uow, user_id)

    async def _update_daily_record(
        self, uow: UnitOfWork, user_id: UUID, daily_total: float
    ) -> None:
        records = await uow.user_record_repo.get_records(user_id)
        current_daily = records.get("daily", 0)

        if daily_total > current_daily:
            existing = await uow.user_record_repo.filter(
                {"user_id": user_id, "type": "daily"}
            )
            for rec in existing:
                await uow.user_record_repo.delete(rec.id)

            await uow.user_record_repo.create(
                {
                    "user_id": user_id,
                    "type": "daily",
                    "count": daily_total,
                }
            )
            logger.info(f"Daily record updated for user {user_id}: {daily_total}")

    async def _update_weekly_record(
        self, uow: UnitOfWork, user_id: UUID, week_total: float
    ) -> None:
        records = await uow.user_record_repo.get_records(user_id)
        current_weekly = records.get("weekly", 0)

        if week_total > current_weekly:
            existing = await uow.user_record_repo.filter(
                {"user_id": user_id, "type": "weekly"}
            )
            for rec in existing:
                await uow.user_record_repo.delete(rec.id)

            await uow.user_record_repo.create(
                {
                    "user_id": user_id,
                    "type": "weekly",
                    "count": week_total,
                }
            )
            logger.info(f"Weekly record updated for user {user_id}: {week_total}")

    async def _find_and_set_best_daily(self, uow: UnitOfWork, user_id: UUID) -> None:
        daily_stats = await uow.daily_stats_repo.filter({"user_id": user_id})
        if not daily_stats:
            existing = await uow.user_record_repo.filter(
                {"user_id": user_id, "type": "daily"}
            )
            for rec in existing:
                await uow.user_record_repo.delete(rec.id)
            return

        best = max(daily_stats, key=lambda s: s.total_count)

        existing = await uow.user_record_repo.filter(
            {"user_id": user_id, "type": "daily"}
        )
        for rec in existing:
            await uow.user_record_repo.delete(rec.id)

        await uow.user_record_repo.create(
            {
                "user_id": user_id,
                "type": "daily",
                "count": best.total_count,
            }
        )
        logger.info(f"Daily record recalculated for user {user_id}: {best.total_count}")

    async def _find_and_set_best_weekly(self, uow: UnitOfWork, user_id: UUID) -> None:
        daily_stats = await uow.daily_stats_repo.filter({"user_id": user_id})
        if not daily_stats:
            existing = await uow.user_record_repo.filter(
                {"user_id": user_id, "type": "weekly"}
            )
            for rec in existing:
                await uow.user_record_repo.delete(rec.id)
            return

        week_totals: dict[date, float] = {}
        for stat in daily_stats:
            week_start = stat.date - timedelta(days=stat.date.weekday())
            week_totals[week_start] = week_totals.get(week_start, 0) + stat.total_count

        if not week_totals:
            return

        best_week = max(week_totals.values())

        existing = await uow.user_record_repo.filter(
            {"user_id": user_id, "type": "weekly"}
        )
        for rec in existing:
            await uow.user_record_repo.delete(rec.id)

        await uow.user_record_repo.create(
            {
                "user_id": user_id,
                "type": "weekly",
                "count": best_week,
            }
        )
        logger.info(f"Weekly record recalculated for user {user_id}: {best_week}")
