import random

from polyfactory import AsyncPersistenceProtocol, Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.liability import Liability, LiabilityCreate
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[Liability]):
    async def save(self, data: Liability) -> Liability:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.liability_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class LiabilityFactory(ModelFactory[Liability]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler

    count = Use(lambda: round(random.uniform(0.1, 100.0), 2))


class LiabilityCreateFactory(ModelFactory[LiabilityCreate]):
    __check_model__ = False
    __allow_none_optionals__ = False

    count = Use(lambda: round(random.uniform(0.1, 100.0), 2))