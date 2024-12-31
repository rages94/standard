from typing import Protocol

from sqlalchemy import Select
from sqlalchemy.sql.schema import ColumnCollectionConstraint

from src.common.repository.interfaces.mixins.bulk_operations_mixin import BulkOperationsMixinI
from src.common.repository.interfaces.mixins.create_update_mixin import CreateUpdateMixinI
from src.common.repository.interfaces.mixins.delete_mixin import DeleteMixinI
from src.common.repository.interfaces.mixins.list_mixin import ListMixinI
from src.common.repository.interfaces.mixins.retrieve_mixin import RetrieveMixinI


class BaseRepositoryI[ModelType, FilterSet, SessionType](Protocol):
    model: ModelType
    filter_set: FilterSet
    session: SessionType
    uow: bool
    query: Select | None = None
    constraint: str | None = None

    async def commit(self) -> None: ...

    def get_query(self) -> Select: ...

    def get_constraint(self) -> str | ColumnCollectionConstraint: ...


class RepositoryI[ModelType, FilterSet, SessionType, SchemaOutType, ListSchemaOutType](
    ListMixinI[ListSchemaOutType],
    RetrieveMixinI[SchemaOutType],
    CreateUpdateMixinI[SchemaOutType],
    DeleteMixinI,
    BulkOperationsMixinI,
    BaseRepositoryI[ModelType, FilterSet, SessionType],
    Protocol,
): ...
