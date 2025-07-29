from src.data.models.liability import LiabilityPublic
from src.data.uow import UnitOfWork
from src.domain.liabilities.dto.filter import LiabilityFilterSchema


class ListLiabilities:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, params: LiabilityFilterSchema) -> list[LiabilityPublic]:
        async with self.uow:
            return await self.uow.liability_repo.filter(params.model_dump(exclude_unset=True))
