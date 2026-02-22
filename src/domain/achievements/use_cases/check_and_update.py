from datetime import date
from uuid import UUID

from src.data.models import Achievement
from src.data.uow import UnitOfWork
from src.domain.achievements.services.achievement_service import AchievementService


class CheckAndUpdateAchievements:
    """Проверить и обновить достижения пользователя"""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(
        self,
        user_id: UUID,
        standard_id: UUID | None = None,
        activity_date: date | None = None,
    ) -> tuple[list[Achievement], list[Achievement]]:
        async with self.uow:
            service = AchievementService(self.uow)
            granted, revoked = await service.check_and_update_achievements(
                user_id=user_id,
                standard_id=standard_id,
                activity_date=activity_date,
            )
            await self.uow.commit()
            return (granted, revoked)
