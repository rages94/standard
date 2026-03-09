from polyfactory import AsyncPersistenceProtocol, Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.achievement import (
    Achievement,
    AchievementCreate,
    AchievementUpdate,
)
from src.data.uow import UnitOfWork
from src.domain.achievements.dto.enums import (
    ConditionType,
    RarityType,
)


class AsyncPersistenceHandler(AsyncPersistenceProtocol[Achievement]):
    async def save(self, data: Achievement) -> Achievement:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.achievement_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class AchievementFactory(ModelFactory[Achievement]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler

    parent_meta_achievement_id = None
    meta_tier = None


class AchievementCreateFactory(ModelFactory[AchievementCreate]):
    __check_model__ = False
    __allow_none_optionals__ = False

    condition_type = ConditionType.COUNT
    rarity = RarityType.COMMON
    target_value = 100


class AchievementUpdateFactory(ModelFactory[AchievementUpdate]):
    __check_model__ = False
    __allow_none_optionals__ = False
