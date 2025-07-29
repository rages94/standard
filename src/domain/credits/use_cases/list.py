from src.data.models.credit import CreditPublic
from src.data.uow import UnitOfWork
from src.domain.credits.dto.filter import CreditFilterSchema


class ListCredits:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, params: CreditFilterSchema) -> list[CreditPublic]:
        async with self.uow:
            return await self.uow.credit_repo.filter(params.model_dump(exclude_unset=True))
