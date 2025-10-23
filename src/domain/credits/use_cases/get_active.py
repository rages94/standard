from uuid import UUID

from sqlalchemy.exc import NoResultFound

from src.data.models.credit import CreditPublic
from src.data.uow import UnitOfWork
from src.domain.credits.dto.filter import CreditFilterSchema


class GetActiveCredit:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: UUID) -> CreditPublic | None:
        params = CreditFilterSchema(user_id=user_id, completed=None)
        async with self.uow:
            try:
                return await self.uow.credit_repo.get_one(params.model_dump())
            except NoResultFound:
                return None
