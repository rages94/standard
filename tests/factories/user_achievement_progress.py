from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.user_achievement import (
    UserAchievementProgress,
    UserAchievementProgressPublic,
)
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[UserAchievementProgress]):
    async def save(self, data: UserAchievementProgress) -> UserAchievementProgress:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.user_achievement_progress_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class UserAchievementProgressFactory(ModelFactory[UserAchievementProgress]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler

    current_value = 0
    is_earned = False


class UserAchievementProgressPublicFactory(ModelFactory[UserAchievementProgressPublic]):
    __check_model__ = False
    __allow_none_optionals__ = False

    current_value = 0
    is_earned = False
