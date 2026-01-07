from src.data.models import User
from src.domain.completed_standards.use_cases.create import CreateCompletedStandard
from src.data.models.completed_standard import CompletedStandardCreate, CompletedStandardPublic, CompletedStandard
from src.domain.math.services.normalization import ExerciseNormalizationService
from src.domain.ner.use_cases.normalize_phrase import NormalizePhrase
from src.domain.standards.dto.enums import ExerciseType
from src.domain.standards.use_cases.match import MatchStandards
from src.domain.user.dto.enums import CompletedType


class CreateCompletedStandardsFromText:  # TODO rename to singular
    def __init__(
        self,
        match_standards: MatchStandards,
        create_completed_standard: CreateCompletedStandard,
        exercise_normalization: ExerciseNormalizationService,
        normalize_phrase: NormalizePhrase,
    ) -> None:
        self.match_standards = match_standards
        self.create_completed_standard = create_completed_standard
        self.exercise_normalization = exercise_normalization
        self.normalize_phrase = normalize_phrase

    async def __call__(self, text: str, user: User, completed_type: CompletedType) -> CompletedStandard | None:
        user_record = await self.match_standards(self.normalize_phrase(text))
        if not user_record:
            return None

        total_norm = 0
        if user_record.type == ExerciseType.weightlifting:
            normalization = self.exercise_normalization.normalization(
                user.weight,
                user_record.weight,
                user_record.standard.name,
                user.sex,
            )
            total_norm = normalization * user_record.count
        elif user_record.type == ExerciseType.workout:
            total_norm = user_record.count * user_record.standard.count

        completed_standard = CompletedStandardCreate(
            standard_id=user_record.standard.id,
            count=user_record.count,
            weight=user_record.weight,
            user_weight=user.weight,
            total_norm=total_norm,
            completed_type=completed_type
        )
        return await self.create_completed_standard(completed_standard, user_id=user.id)
