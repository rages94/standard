from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.user_achievement import UserAchievement
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[UserAchievement]):
    async def save(self, data: UserAchievement) -> UserAchievement:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.user_achievement_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class UserAchievementFactory(ModelFactory[UserAchievement]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler

    is_viewed = False
    progress_at_earned = 0.0
