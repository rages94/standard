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

        await self._update_daily_record(uow, user_id, daily_total)

        now = moscow_now()
        week_start = (now - timedelta(days=now.weekday())).date()
        week_end = week_start + timedelta(days=7)
        week_total = await uow.daily_stats_repo.get_week_total(
            user_id, week_start, week_end
        )
        await self._update_weekly_record(uow, user_id, week_total)

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
        elif daily_total < current_daily:
            await self._find_and_set_best_daily(uow, user_id)

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
        elif week_total < current_weekly:
            await self._find_and_set_best_weekly(uow, user_id)

    async def _find_and_set_best_daily(self, uow: UnitOfWork, user_id: UUID) -> None:
        best_daily = await uow.daily_stats_repo.get_max_daily(user_id)
        if best_daily == 0:
            existing = await uow.user_record_repo.filter(
                {"user_id": user_id, "type": "daily"}
            )
            for rec in existing:
                await uow.user_record_repo.delete(rec.id)
            return

        existing = await uow.user_record_repo.filter(
            {"user_id": user_id, "type": "daily"}
        )
        for rec in existing:
            await uow.user_record_repo.delete(rec.id)

        await uow.user_record_repo.create(
            {
                "user_id": user_id,
                "type": "daily",
                "count": best_daily,
            }
        )
        logger.info(f"Daily record recalculated for user {user_id}: {best_daily}")

    async def _find_and_set_best_weekly(self, uow: UnitOfWork, user_id: UUID) -> None:
        best_weekly = await uow.daily_stats_repo.get_max_weekly(user_id)
        if best_weekly == 0:
            existing = await uow.user_record_repo.filter(
                {"user_id": user_id, "type": "weekly"}
            )
            for rec in existing:
                await uow.user_record_repo.delete(rec.id)
            return

        existing = await uow.user_record_repo.filter(
            {"user_id": user_id, "type": "weekly"}
        )
        for rec in existing:
            await uow.user_record_repo.delete(rec.id)

        await uow.user_record_repo.create(
            {
                "user_id": user_id,
                "type": "weekly",
                "count": best_weekly,
            }
        )
        logger.info(f"Weekly record recalculated for user {user_id}: {best_weekly}")
