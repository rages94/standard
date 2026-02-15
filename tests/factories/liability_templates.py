from polyfactory import AsyncPersistenceProtocol
from polyfactory.factories.pydantic_factory import ModelFactory

from src.containers.container import container
from src.data.models.liability_template import (
    LiabilityTemplate,
    LiabilityTemplateCreate,
)
from src.data.uow import UnitOfWork


class AsyncPersistenceHandler(AsyncPersistenceProtocol[LiabilityTemplate]):
    async def save(self, data: LiabilityTemplate) -> LiabilityTemplate:
        uow: UnitOfWork = container.repositories.uow()
        async with uow:
            uow.liability_template_repo.add(data)
            await uow.commit()
            await uow.refresh(data)
        return data


class LiabilityTemplateFactory(ModelFactory[LiabilityTemplate]):
    __check_model__ = False
    __allow_none_optionals__ = False
    __async_persistence__ = AsyncPersistenceHandler


class LiabilityTemplateCreateFactory(ModelFactory[LiabilityTemplateCreate]):
    __model__ = LiabilityTemplateCreate
    __allow_none_optionals__ = False
