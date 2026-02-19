from uuid import UUID

from src.data.uow import UnitOfWork
from src.domain.achievements.dto.schemas import (
    AchievementProgressSchema,
)
from src.domain.achievements.services.achievement_service import AchievementService


class ListAchievements:
    """Получить список всех активных достижений с прогрессом пользователя"""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: UUID) -> list[AchievementProgressSchema]:
        async with self.uow:
            service = AchievementService(self.uow)
            return await service.get_user_progress_with_achievements(user_id)
