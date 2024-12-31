from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import NoResultFound

from src.common.repository.interfaces.base import BaseRepositoryI

IdType = int | UUID | str


class DeleteMixin(BaseRepositoryI):
    async def delete(self, object_id: IdType) -> None:
        result: CursorResult = await self.session.execute(  # type: ignore
            delete(self.model).where(self.model.id == object_id)
        )
        if result.rowcount != 1:
            raise NoResultFound
        await self.commit()
