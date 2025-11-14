from uuid import UUID

from src.data.models import User
from src.data.uow import UnitOfWork
from src.domain.user.dto.filters import UserFilterSchema


class ListUsers:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, params: UserFilterSchema) -> list[User]:
        async with self.uow:
            return await self.uow.user_repo.filter(params.model_dump(exclude_unset=True))
