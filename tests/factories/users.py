from polyfactory import Use
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.user import User, UserCreate, UserLogin


class UserCreateFactory(ModelFactory[UserCreate]):
    __check_model__ = False
    __allow_none_optionals__ = False


class UserLoginFactory(ModelFactory[UserLogin]):
    __check_model__ = False
    __allow_none_optionals__ = False


class UserFactory(ModelFactory[User]):
    __async_persistence__ = True
    __check_model__ = False

    hashed_password = Use(lambda: User.get_password_hash("password"))

    @classmethod
    async def create_async(cls, **kwargs):
        uow = container.repositories.uow()
        async with uow:
            user = cls.build(**kwargs)
            uow.user_repo.add(user)
            await uow.commit()
            await uow.refresh(user)
            return user
