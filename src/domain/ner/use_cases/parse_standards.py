from src.data.models import Standard
from src.data.uow import UnitOfWork
from src.domain.ner.dto.enums import ParamType
from src.domain.ner.use_cases.normalize_phrase import NormalizePhrase


class ParseStandards:
    def __init__(self, ner_model, normalize_phrase: NormalizePhrase, uow: UnitOfWork):
        self.ner_model = ner_model
        self.uow = uow
        self.normalize_phrase = normalize_phrase
        self.mapping_standard: dict[str, Standard] = dict()

    async def __call__(self, text: str) -> list[tuple[Standard, int]]:
        if not self.mapping_standard:
            await self._load_standards()

        doc = self.ner_model(text)
        result: list[tuple[Standard, int]] = []
        last_qty = None
        ex_id = None

        for ent in doc.ents:
            if ent.label_ == ParamType.count.value:
                try:
                    last_qty = int(ent.text)
                except ValueError:
                    continue
            elif ent.label_ == ParamType.exercise.value:
                normalized = self.normalize_phrase(ent.text.lower())
                if normalized in self.mapping_standard:
                    ex_id = self.mapping_standard[normalized]
            if last_qty and ex_id:
                result.append((ex_id, last_qty))
                last_qty = None
                ex_id = None
        return result

    async def _load_standards(self) -> None:
        async with self.uow:
            standards = await self.uow.standard_repo.filter(dict())
            self.mapping_standard = {standard.normal_form: standard for standard in standards}
