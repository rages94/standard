from src.data.models.completed_standard import CompletedStandardPublic
from src.data.uow import UnitOfWork
from src.domain.completed_standards.dto.filter import CompletedStandardFilterSchema


class ListCompletedStandards:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, params: CompletedStandardFilterSchema) -> list[CompletedStandardPublic]:
        async with self.uow:
            return await self.uow.completed_standard_repo.filter(params.model_dump(exclude_unset=True))
