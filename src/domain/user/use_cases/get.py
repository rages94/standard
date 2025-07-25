from uuid import UUID

from src.data.models import User
from src.data.uow import UnitOfWork


class GetUser:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, user_id: UUID) -> User:
        async with self.uow:
            return await self.uow.user_repo.get_one(dict(id=user_id))
