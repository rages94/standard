from src.domain.achievements.dto.enums import AchievementCategory
from src.domain.achievements.dto.schemas import AchievementCategorySchema


class GetAchievementCategories:
    """Получить список всех категорий достижений"""

    async def __call__(self) -> list[AchievementCategorySchema]:
        return [
            AchievementCategorySchema(value=cat.value, label=cat.name)
            for cat in AchievementCategory
        ]
