from datetime import date
from uuid import uuid4

from polyfactory import AsyncPersistenceProtocol, Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models import DailyStats
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[DailyStats]):
    async def save(self, data: DailyStats) -> DailyStats:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.daily_stats_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class DailyStatsFactory(ModelFactory[DailyStats]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler
    id = Use(lambda: uuid4())
    total_count = Use(lambda: round(__import__("random").uniform(0.0, 1000.0), 2))
