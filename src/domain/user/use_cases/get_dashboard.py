import logging
from uuid import UUID

from src.common.models.mixins import utcnow
from src.data.models.completed_standard import CompletedStandardPublic
from src.data.models.credit import CreditPublic
from src.data.models.user import UserPublic
from src.data.models.user_streak import UserStreakPublic
from src.data.uow import UnitOfWork
from src.domain.user.dto.output import DashboardResponse

logger = logging.getLogger(__name__)


class GetDashboard:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: UUID) -> DashboardResponse:
        async with self.uow:
            user = await self.uow.user_repo.get_one(dict(id=user_id))
            current_credit_raw = await self.uow.credit_repo.get_or_none(
                dict(user_id=user_id, deadline_date_ge=utcnow())
            )
            recent_activity_raw = await self.uow.completed_standard_repo.get_recent(
                user_id, 5
            )
            streak = await self.uow.user_streak_repo.get_one(dict(user_id=user_id))
            today_norm = await self.uow.completed_standard_repo.get_today_norm(user_id)
            month_norm = await self.uow.completed_standard_repo.get_month_norm(user_id)

        user_public = UserPublic(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            weight=user.weight,
            sex=user.sex,
            birthday=user.birthday,
            total_liabilities=user.total_liabilities,
            completed_type=user.completed_type,
        )

        current_credit_public: CreditPublic | None = None
        if current_credit_raw:
            current_credit_public = CreditPublic(
                id=current_credit_raw.id,
                count=current_credit_raw.count,
                completed_count=current_credit_raw.completed_count,
                created_at=current_credit_raw.created_at,
                deadline_date=current_credit_raw.deadline_date,
                completed_at=current_credit_raw.completed_at,
                completed=current_credit_raw.completed,
            )

        recent_activity: list[CompletedStandardPublic] = []
        for cs in recent_activity_raw:
            standard_public = None
            if cs.standard:
                from src.data.models.standard import StandardPublic

                standard_public = StandardPublic(
                    id=cs.standard.id,
                    name=cs.standard.name,
                    normal_form=cs.standard.normal_form,
                    count=cs.standard.count,
                    category=cs.standard.category,
                )
            recent_activity.append(
                CompletedStandardPublic(
                    id=cs.id,
                    count=cs.count,
                    weight=cs.weight,
                    user_weight=cs.user_weight,
                    total_norm=cs.total_norm,
                    created_at=cs.created_at,
                    standard=standard_public,
                    user_id=cs.user_id,
                )
            )

        streak_public = UserStreakPublic(
            id=user_id,
            user_id=user_id,
            current_streak=streak.current_streak if streak else 0,
            longest_streak=streak.longest_streak if streak else 0,
            last_activity_date=streak.last_activity_date if streak else None,
        )

        return DashboardResponse(
            user=user_public,
            current_credit=current_credit_public,
            recent_activity=recent_activity,
            streak=streak_public,
            today_norm=today_norm,
            month_norm=month_norm,
        )
