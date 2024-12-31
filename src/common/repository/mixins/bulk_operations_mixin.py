from copy import copy
from sqlalchemy import bindparam, delete, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import BindParameter

from src.common.repository.interfaces.base import BaseRepositoryI


class BulkOperationsMixin(BaseRepositoryI):
    bulk_delete_query: Select | None = None

    async def bulk_create(self, data: list[dict]) -> None:
        await self.session.execute(insert(self.model).values(data))
        await self.commit()

    async def bulk_insert(self, data: list[dict]) -> None:
        ins = insert(self.model).values(data)
        constraint = self.get_constraint()
        query = ins.on_conflict_do_nothing(constraint=constraint)
        await self.session.execute(query)
        await self.commit()

    async def bulk_update(self, data: list[dict], by_field: str = "id") -> None:
        update_keys = set().union(*(d.keys() for d in data))
        values: dict[str, BindParameter] = {
            key: bindparam(key) for key in update_keys if key != by_field
        }
        query = (
            update(self.model)
            .where(getattr(self.model, by_field) == bindparam(by_field))
            .values(values)
        )
        await self.session.execute(query, data)
        await self.commit()

    async def bulk_update_by_pk(self, data: list[dict]) -> None:
        if not all("id" in d for d in data):
            raise ValueError("All dicts in data must contain the 'id' pk field.")
        await self.session.execute(update(self.model), data)
        await self.commit()

    async def bulk_delete(self, params: dict) -> None:
        query = self.get_bulk_delete_query()
        query = (
            self.filter_set(query).filter_query(params).with_only_columns(self.model.id)
        )
        smtp = delete(self.model).where(self.model.id.in_(query))
        await self.session.execute(
            smtp, execution_options={"synchronize_session": "fetch"}
        )
        await self.commit()

    async def bulk_upsert(
        self,
        data: list[dict],
        params: dict | None = None,
        exclude_from_update: list[str] | None = None,
    ) -> None:
        ins = insert(self.model)
        update_keys = set().union(*(d.keys() for d in data))
        if not exclude_from_update:
            exclude_from_update = []
        update_dict = {
            c.name: c
            for c in ins.excluded
            if not c.primary_key
            and c.name in update_keys
            and c.name not in exclude_from_update
        }
        constraint = self.get_constraint()
        query = ins.on_conflict_do_update(constraint=constraint, set_=update_dict)
        if params:
            base_query = self.get_query()
            where = self.filter_set(base_query).filter_query(params).whereclause
            query = ins.on_conflict_do_update(
                constraint=constraint, set_=update_dict, where=where
            )
        await self.session.execute(query, data)
        await self.commit()

    def get_bulk_delete_query(self) -> Select:
        if self.bulk_delete_query is not None:
            return copy(self.bulk_delete_query)
        return self.get_query()
