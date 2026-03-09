from polyfactory import AsyncPersistenceProtocol, Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.user import User, UserCreate, UserLogin
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[User]):
    async def save(self, data: User) -> User:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.user_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class UserCreateFactory(ModelFactory[UserCreate]):
    __check_model__ = False
    __allow_none_optionals__ = False


class UserLoginFactory(ModelFactory[UserLogin]):
    __check_model__ = False
    __allow_none_optionals__ = False


class UserFactory(ModelFactory[User]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler

    hashed_password = Use(lambda: User.get_password_hash("password"))
