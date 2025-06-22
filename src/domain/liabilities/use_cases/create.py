from uuid import UUID

from src.data.models import Liability
from src.data.models.liability import LiabilityCreate
from src.data.uow import UnitOfWork


class CreateLiability:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, body: LiabilityCreate, user_id: UUID):
        async with self.uow:
            liability = Liability(
                liability_template_id=body.liability_template_id,
                count=body.count,
                user_id=user_id
            )
            self.uow.liability_repo.add(liability)

            await self.uow.flush()
            await self.uow.user_repo.update_total_liabilities(user_id)
            await self.uow.commit()
            await self.uow.refresh(liability)
        return liability
