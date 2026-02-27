from polyfactory.factories.pydantic_factory import ModelFactory

from src.data.models.achievement import (
    Achievement,
    AchievementCreate,
    AchievementUpdate,
)
from src.domain.achievements.dto.enums import (
    ConditionType,
    RarityType,
)


class AchievementFactory(ModelFactory[Achievement]):
    __check_model__ = False
    __allow_none_optionals__ = False


class AchievementCreateFactory(ModelFactory[AchievementCreate]):
    __check_model__ = False
    __allow_none_optionals__ = False

    condition_type = ConditionType.COUNT
    rarity = RarityType.COMMON
    target_value = 100


class AchievementUpdateFactory(ModelFactory[AchievementUpdate]):
    __check_model__ = False
    __allow_none_optionals__ = False
