from uuid import UUID

from src.data.uow import UnitOfWork
from src.domain.achievements.dto.schemas import UserStreakSchema
from src.domain.achievements.services.achievement_service import AchievementService


class GetUserStreak:
    """Получить текущую серию дней пользователя"""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: UUID) -> UserStreakSchema | None:
        async with self.uow:
            service = AchievementService(self.uow)
            return await service.get_user_streak(user_id)
