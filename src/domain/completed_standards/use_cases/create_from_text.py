from uuid import UUID

from src.domain.completed_standards.use_cases.create import CreateCompletedStandard
from src.domain.ner.use_cases.parse_standards import ParseStandards
from src.data.models.completed_standard import CompletedStandardCreate
from src.domain.user.dto.enums import CompletedType


class CreateCompletedStandardsFromText:
    def __init__(self, parse_standards: ParseStandards, create_completed_standard: CreateCompletedStandard) -> None:
        self.parse_standards = parse_standards
        self.create_completed_standard = create_completed_standard

    async def __call__(self, text: str, user_id: UUID, completed_type: CompletedType) -> dict[str, int]:
        parsed_params = await self.parse_standards(text)
        results: dict[str, int] = dict()
        for standard, count in parsed_params:
            results[standard.name] = count
            await self.create_completed_standard(
                CompletedStandardCreate(
                    standard_id=standard.id,
                    count=count,
                    completed_type=completed_type
                ),
                user_id=user_id,
            )
        return results
