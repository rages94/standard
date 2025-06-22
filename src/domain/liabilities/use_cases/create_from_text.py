from uuid import UUID

from src.data.models.liability import LiabilityCreate
from src.domain.liabilities.use_cases.create import CreateLiability
from src.domain.ner.use_cases.parse_liability_templates import ParseLiabilityTemplates


class CreateLiabilitiesFromText:
    def __init__(self, parse_liability_templates: ParseLiabilityTemplates, create_liability: CreateLiability) -> None:
        self.parse_liability_templates = parse_liability_templates
        self.create_liability = create_liability

    async def __call__(self, text: str, user_id: UUID) -> dict[str, int]:
        parsed_params = await self.parse_liability_templates(text)
        results: dict[str, int] = dict()
        for liability_template, count in parsed_params:
            results[liability_template.name] = count
            await self.create_liability(
                LiabilityCreate(
                    liability_template_id=liability_template.id,
                    count=count,
                ),
                user_id=user_id,
            )
        return results
