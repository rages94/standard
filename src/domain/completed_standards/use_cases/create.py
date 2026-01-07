from uuid import UUID

from sqlalchemy.exc import NoResultFound

from src.data.uow import UnitOfWork
from src.data.models.completed_standard import CompletedStandardCreate, CompletedStandard


class CreateCompletedStandard:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, body: CompletedStandardCreate, user_id: UUID) -> CompletedStandard:
        async with self.uow:
            standard = await self.uow.standard_repo.get_one(dict(id=body.standard_id))
            standard_count = body.total_norm
            if not standard_count:  # TODO выпилить нахрен completed_type
                standard_count = body.count if not body.completed_type_is_count() else body.count // standard.count
            count = body.count if body.completed_type_is_count() else body.count * standard.count
            completed_standard = CompletedStandard(
                standard_id=body.standard_id,
                count=count,
                user_id=user_id,
                weight=body.weight,
                total_norm=standard_count,
            )
            self.uow.completed_standard_repo.add(completed_standard)

            await self.uow.flush()
            await self.uow.user_repo.update_total_liabilities(user_id)
            try:
                await self.uow.credit_repo.update_completed_count(user_id, standard_count)
            except NoResultFound:
                pass
            await self.uow.commit()
            await self.uow.refresh(completed_standard)
        return completed_standard