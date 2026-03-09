import logging
from uuid import UUID

from src.common.models.mixins import utcnow
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
            today_norm = await self.uow.completed_standard_repo.get_today_norm(user_id)
            month_norm = await self.uow.completed_standard_repo.get_month_norm(user_id)
            nearest_achievement = (
                await self.uow.user_achievement_progress_repo.get_nearest_achievement(
                    user_id
                )
            )

        return DashboardResponse(
            user=user,
            current_credit=current_credit,
            streak=streak,
            today_norm=today_norm,
            month_norm=month_norm,
            nearest_achievement=nearest_achievement,
        )
