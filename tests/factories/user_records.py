from uuid import uuid4

from polyfactory import AsyncPersistenceProtocol, Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models import UserRecord
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[UserRecord]):
    async def save(self, data: UserRecord) -> UserRecord:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.user_record_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class UserRecordFactory(ModelFactory[UserRecord]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler
    id = Use(lambda: uuid4())
    user_id = Use(lambda: uuid4())
