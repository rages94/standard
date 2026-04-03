import logging
from datetime import timedelta
from uuid import UUID

from src.common.models.mixins import moscow_now, utcnow
from src.data.uow import UnitOfWork
from src.domain.user.dto.output import DashboardResponse

logger = logging.getLogger(__name__)


class GetDashboard:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: UUID) -> DashboardResponse:
        async with self.uow:
            user = await self.uow.user_repo.get_one(dict(id=user_id))
            current_credit = await self.uow.credit_repo.get_or_none(
                dict(user_id=user_id, deadline_date_ge=utcnow())
            )
            streak = await self.uow.user_streak_repo.get_or_none(dict(user_id=user_id))

            now = moscow_now()
            day_total = await self.uow.daily_stats_repo.get_or_none(
                dict(user_id=user_id, date=now.date())
            )
            week_start = (now - timedelta(days=now.weekday())).date()
            week_end = week_start + timedelta(days=7)
            week_total = await self.uow.daily_stats_repo.get_week_total(
                user_id, week_start, week_end
            )

            nearest_achievement = (
                await self.uow.user_achievement_progress_repo.get_nearest_achievement(
                    user_id
                )
            )

            records = await self.uow.user_record_repo.get_records(user_id)
            daily_record = records.get("daily", 0)
            weekly_record = records.get("weekly", 0)

        return DashboardResponse(
            user=user,
            current_credit=current_credit,
            streak=streak,
            today_norm=day_total.total_count if day_total else 0,
            week_norm=week_total or 0,
            daily_record=daily_record,
            weekly_record=weekly_record,
            nearest_achievement=nearest_achievement,
        )
