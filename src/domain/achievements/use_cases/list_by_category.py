from uuid import UUID

from src.data.uow import UnitOfWork
from src.domain.achievements.dto.schemas import AchievementProgressSchema
from src.domain.achievements.services.achievement_service import AchievementService


class ListAchievementsByCategory:
    """Получить достижения по категории с прогрессом"""

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(
        self, user_id: UUID, category: str
    ) -> list[AchievementProgressSchema]:
        async with self.uow:
            service = AchievementService(self.uow)
            return await service.get_user_progress_with_achievements(user_id, category)
