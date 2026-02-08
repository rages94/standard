import random

from polyfactory import AsyncPersistenceProtocol, Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.completed_standard import (
    CompletedStandard,
    CompletedStandardCreate,
)
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[CompletedStandard]):
    async def save(self, data: CompletedStandard) -> CompletedStandard:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.completed_standard_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class CompletedStandardFactory(ModelFactory[CompletedStandard]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler

    count = Use(lambda: round(random.uniform(0.1, 100.0), 2))
    weight = Use(lambda: round(random.uniform(0.0, 300.0), 2))
    user_weight = Use(lambda: round(random.uniform(0.0, 300.0), 2))
    total_norm = Use(lambda: round(random.uniform(0.0, 1000.0), 2))


class CompletedStandardCreateFactory(ModelFactory[CompletedStandardCreate]):
    __check_model__ = False
    __allow_none_optionals__ = False

    count = Use(lambda: round(random.uniform(0.1, 100.0), 2))
    weight = Use(lambda: round(random.uniform(0.0, 300.0), 2))
    user_weight = Use(lambda: round(random.uniform(0.0, 300.0), 2))
    total_norm = Use(lambda: round(random.uniform(0.0, 1000.0), 2))
