from uuid import UUID

from src.data.models.completed_standard import CompletedStandardPublic
from src.domain.completed_standards.dto.filter import CompletedStandardFilterSchema
from src.domain.completed_standards.use_cases.list import ListCompletedStandards
from src.domain.ner.use_cases.get_count_from_text import GetCountFromText


class ListCompletedStandardsFromText:
    def __init__(self, get_count_from_text: GetCountFromText, list_completed_standards: ListCompletedStandards) -> None:
        self.get_count_from_text = get_count_from_text
        self.list_completed_standards = list_completed_standards

    async def __call__(self, text: str, user_id: UUID) -> list[CompletedStandardPublic]:
        count_items = self.get_count_from_text(text)
        return await self.list_completed_standards(
            CompletedStandardFilterSchema(user_id=user_id, pagination=(count_items or 10, 0))
        )
