from uuid import UUID

from src.data.uow import UnitOfWork
from src.domain.achievements.dto.schemas import EarnedAchievementSchema
from src.domain.achievements.services.achievement_service import AchievementService


class GetUserEarnedAchievements:
    """Получить полученные достижения пользователя"""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: UUID) -> list[EarnedAchievementSchema]:
        async with self.uow:
            service = AchievementService(self.uow)
            return await service.get_user_earned_achievements(user_id)
