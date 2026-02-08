from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.standard import Standard, StandardCreate, StandardUpdate
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[Standard]):
    async def save(self, data: Standard) -> Standard:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.standard_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class StandardFactory(ModelFactory[Standard]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler


class StandardCreateFactory(ModelFactory[StandardCreate]):
    __check_model__ = False
    __allow_none_optionals__ = False


class StandardUpdateFactory(ModelFactory[StandardUpdate]):
    __check_model__ = False
    __allow_none_optionals__ = False
