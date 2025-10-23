from uuid import UUID

from src.data.uow import UnitOfWork
from src.domain.completed_standards.dto.output import RatingGroupedCompletedStandard
from src.domain.ner.dto.enums import ParamType


class GetRatingFromText:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, text: str, user_id: UUID) -> list[RatingGroupedCompletedStandard]:
        period_days = 1
        for word in text.split():
            if word.isdigit():
                period_days = int(word)
                break
        async with self.uow:
            return await self.uow.completed_standard_repo.rating_list(period_days or None)
