from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.user import User


class UserFactory(ModelFactory[User]):
    __async_persistence__ = True
    __check_model__ = False

    @classmethod
    async def create_async(cls, **kwargs):
        uow = container.repositories.uow()
        async with uow:
            user = cls.build(**kwargs)
            uow.user_repo.add(user)
            await uow.commit()
            await uow.refresh(user)
            return user
