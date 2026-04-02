from uuid import UUID

from src.data.uow import UnitOfWork


class GetRecords:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: UUID) -> dict[str, float]:
        async with self.uow:
            return await self.uow.user_record_repo.get_records(user_id)
