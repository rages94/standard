from src.domain.achievements.dto.enums import AchievementCategory


class GetAchievementCategories:
    """Получить список всех категорий достижений"""

    async def __call__(self) -> list[dict]:
        return [{"value": cat.value, "label": cat.name} for cat in AchievementCategory]
