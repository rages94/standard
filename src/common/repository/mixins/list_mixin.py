from copy import copy

from sqlalchemy import Select

from src.common.repository.interfaces.base import BaseRepositoryI


class ListMixin[ModelType](BaseRepositoryI):
    list_query: Select | None = None

    async def filter(self, params: dict) -> list[ModelType]:
        query = self.get_list_query()
        filtered_query = self.filter_set(query).filter_query(params)
        return (await self.session.execute(filtered_query)).unique().scalars().all()

    async def count(self, params: dict) -> int:
        query = self.get_list_query()
        count_query = self.filter_set(query).count_query(params)
        return (await self.session.execute(count_query)).scalar()

    def get_list_query(self) -> Select:
        if self.list_query is not None:
            return copy(self.list_query)
        return self.get_query()
