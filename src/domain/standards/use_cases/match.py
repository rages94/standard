import re

from rapidfuzz import process

from src.data.models import Standard
from src.data.uow import UnitOfWork
from src.domain.standards.dto.enums import ExerciseType
from src.domain.standards.dto.inner import StandardUserRecordSchema


class MatchStandards:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.mapping_standard: dict[str, Standard] = dict()
        self.digits_pattern = "\d+"
        self.float_pattern = "\d*\.\d+|\d+"

    async def __call__(self, text: str) -> StandardUserRecordSchema | None:
        if not self.mapping_standard:
            await self._load_standards()

        standard_normal_form = self._match_exercise(text)
        if not standard_normal_form or standard_normal_form not in self.mapping_standard:
            return

        standard = self.mapping_standard[standard_normal_form]
        if standard.count:
            repeats = self._parse_workout(text)
            weight = None
            type_ = ExerciseType.workout
        else:
            weight, repeats = self._parse_weightlifting(text)
            type_ = ExerciseType.weightlifting
        return StandardUserRecordSchema(standard=standard, count=repeats, weight=weight, type=type_)

    async def _load_standards(self) -> None:
        async with self.uow:
            standards = await self.uow.standard_repo.filter(dict())
            self.mapping_standard = {standard.normal_form: standard for standard in standards}

    def _match_exercise(self, text: str):
        result = process.extractOne(text, self.mapping_standard.keys(), score_cutoff=70)
        return result[0] if result else None

    def _cut_float(self, text: str) -> tuple[str, float | None]:
        weight_match = re.search(self.float_pattern, text)
        if not weight_match:
            return text, None

        text = text.replace(weight_match.group(0), " ").strip()
        return text, float(weight_match.group(0))

    def _cut_digits(self, text: str) -> tuple[str, int | None]:
        match = re.search(self.digits_pattern, text)
        if not match:
            return text, None

        text = text.replace(match.group(0), " ").strip()
        return text, int(match.group(0))

    def _parse_weightlifting(self, text: str) -> tuple[float | None, int | None]:
        text, weight = self._cut_float(text)
        _, repeats = self._cut_digits(text)
        return weight, repeats or 1

    def _parse_workout(self, text: str) -> int | None:
        _, repeats = self._cut_digits(text)
        return repeats