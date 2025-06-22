from src.data.models import Standard, LiabilityTemplate
from src.data.uow import UnitOfWork
from src.domain.ner.dto.enums import ParamType
from src.domain.ner.use_cases.normalize_phrase import NormalizePhrase


class ParseLiabilityTemplates:
    def __init__(self, ner_model, normalize_phrase: NormalizePhrase, uow: UnitOfWork):
        self.ner_model = ner_model
        self.uow = uow
        self.normalize_phrase = normalize_phrase
        self.mapping_liability_templates: dict[str, LiabilityTemplate] = dict()

    async def __call__(self, text: str) -> list[tuple[LiabilityTemplate, int]]:
        if not self.mapping_liability_templates:
            await self._load_liability_templates()

        doc = self.ner_model(text)
        result: list[tuple[Standard, int]] = []
        last_qty = None
        lt_id = None

        for ent in doc.ents:
            if ent.label_ == ParamType.count.value:
                try:
                    last_qty = int(ent.text)
                except ValueError:
                    continue
            elif ent.label_ == ParamType.liability.value:
                normalized = self.normalize_phrase(ent.text.lower())
                if normalized in self.mapping_liability_templates:
                    lt_id = self.mapping_liability_templates[normalized]
            if last_qty and lt_id:
                result.append((lt_id, last_qty))
                last_qty = None
                lt_id = None
        return result

    async def _load_liability_templates(self) -> None:
        async with self.uow:
            liability_templates = await self.uow.liability_template_repo.filter(dict())
            self.mapping_liability_templates = {template.normal_form: template for template in liability_templates}
