from copy import copy
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.sql.schema import ColumnCollectionConstraint
from sqlmodel import SQLModel

from src.common.repository.mixins.bulk_operations_mixin import BulkOperationsMixin
from src.common.repository.mixins.create_update_mixin import CreateUpdateMixin
from src.common.repository.mixins.delete_mixin import DeleteMixin
from src.common.repository.mixins.list_mixin import ListMixin
from src.common.repository.mixins.retrieve_mixin import RetrieveMixin

IdType = int | UUID | str


class BaseRepository[ModelType, FilterSet, SessionType]:
    model: ModelType
    filter_set: FilterSet
    query: Select | None = None
    constraint: str | None = None

    def __init__(self, session: SessionType, uow: bool = True):
        self.session = session
        self.uow = uow

    def get_query(self) -> Select:
        query = self.query if self.query is not None else select(self.model)
        return copy(query)

    async def commit(self) -> None:
        if self.uow:
            return
        await self.session.commit()

    def get_constraint(self) -> str | ColumnCollectionConstraint:
        constraint: str | ColumnCollectionConstraint = (
            self.constraint if self.constraint is not None else self.model.__table__.primary_key  # type: ignore
        )
        return copy(constraint)

    def add(self, entity: SQLModel) -> None:
        self.session.add(entity)


class Repository[ModelType, FilterSet, SessionType](
    BaseRepository[ModelType, FilterSet, SessionType],
    RetrieveMixin[ModelType],
    ListMixin,
    CreateUpdateMixin[ModelType],
    DeleteMixin,
    BulkOperationsMixin,
): ...
