from src.common.repository.interfaces.base import BaseRepositoryI


class RetrieveMixin[ModelType](BaseRepositoryI):
    async def get_one(self, params: dict) -> ModelType:
        query = self.get_query()
        filtered_query = self.filter_set(query).filter_query(params)
        result = await self.session.execute(filtered_query)
        return result.unique().scalars().one()
