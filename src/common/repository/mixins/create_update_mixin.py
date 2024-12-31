from uuid import UUID

from sqlalchemy import update
from sqlalchemy.exc import NoResultFound

from src.common.repository.interfaces.base import BaseRepositoryI

IdType = int | UUID | str


class CreateUpdateMixin[ModelType](BaseRepositoryI):
    model: ModelType

    async def create(self, data: dict) -> ModelType:
        obj = self.model(**data)
        self.session.add(obj)
        await self.commit()
        return await self._get_object(obj.id)

    async def update(self, data: dict) -> None:
        object_id = data.pop("id")
        result = await self.session.execute(
            update(self.model).where(self.model.id == object_id).values(**data)
        )
        if result.rowcount != 1:
            raise NoResultFound

    async def _get_object(self, id: IdType) -> ModelType:
        query = (
            self.get_query()
            .where(self.model.id == id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(query)
        return result.unique().scalars().one()

    async def create_or_update(self, data: dict) -> ModelType:
        try:
            return await self.update(data)
        except NoResultFound:
            return await self.create(data)
