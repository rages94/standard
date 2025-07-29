from uuid import UUID

from src.data.models.completed_standard import CompletedStandardPublic
from src.domain.liabilities.dto.filter import LiabilityFilterSchema
from src.domain.liabilities.use_cases.list import ListLiabilities
from src.domain.ner.use_cases.get_count_from_text import GetCountFromText


class ListLiabilitiesFromText:
    def __init__(self, get_count_from_text: GetCountFromText, list_liabilities: ListLiabilities) -> None:
        self.get_count_from_text = get_count_from_text
        self.list_liabilities = list_liabilities

    async def __call__(self, text: str, user_id: UUID) -> list[CompletedStandardPublic]:
        count_items = self.get_count_from_text(text)
        return await self.list_liabilities(
            LiabilityFilterSchema(user_id=user_id, pagination=(count_items or 10, 0))
        )
