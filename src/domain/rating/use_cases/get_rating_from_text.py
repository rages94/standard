from uuid import UUID

from src.data.uow import UnitOfWork
from src.domain.completed_standards.dto.output import RatingGroupedCompletedStandard
from src.domain.ner.dto.enums import ParamType


class GetRatingFromText:
    def __init__(self, ner_model, uow: UnitOfWork) -> None:
        self.ner_model = ner_model
        self.uow = uow

    async def __call__(self, text: str, user_id: UUID) -> list[RatingGroupedCompletedStandard]:
        doc = self.ner_model(text)
        period_days = 1
        for ent in doc.ents:  # TODO fix parsing count (приходит 'рейтинг за N')
            if ent.label_ == ParamType.count.value:
                try:
                    period_days = int(ent.text)
                except ValueError:
                    continue
        async with self.uow:
            return await self.uow.completed_standard_repo.rating_list(period_days or None)
