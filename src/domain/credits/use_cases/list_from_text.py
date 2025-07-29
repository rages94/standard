from uuid import UUID

from src.data.models.credit import CreditPublic
from src.domain.credits.dto.filter import CreditFilterSchema
from src.domain.credits.use_cases.list import ListCredits
from src.domain.ner.use_cases.get_count_from_text import GetCountFromText


class ListCreditsFromText:
    def __init__(self, get_count_from_text: GetCountFromText, list_credits: ListCredits) -> None:
        self.get_count_from_text = get_count_from_text
        self.list_credits = list_credits

    async def __call__(self, text: str, user_id: UUID) -> list[CreditPublic]:
        count_items = self.get_count_from_text(text)
        return await self.list_credits(
            CreditFilterSchema(user_id=user_id, pagination=(count_items or 10, 0))
        )
