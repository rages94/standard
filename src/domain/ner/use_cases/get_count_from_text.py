from src.domain.ner.dto.enums import ParamType


class GetCountFromText:
    def __init__(self, ner_model):
        self.ner_model = ner_model

    def __call__(self, text: str) -> int | None:
        doc = self.ner_model(text)
        for ent in doc.ents:
            if ent.label_ == ParamType.count.value:
                try:
                    return int(ent.text)
                except ValueError:
                    continue
